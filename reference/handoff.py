"""Deterministic handoff checker. Trust inputs must be obtained by the receiver."""
import argparse
import hashlib
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def text_list(value):
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def failure(name, detail):
    return {'verdict': 'blocked', 'checks': [{'name': name, 'status': 'fail', 'detail': detail}], 'side_effects': 0}


def evaluate(message, project, evidence, identity, ledger_path, now):
    """Validate receiver snapshots and report operational failures."""
    try:
        fields = ('id', 'revision', 'contract', 'suite', 'environment')
        valid_project = isinstance(project, dict) and all(
            isinstance(project.get(key), str) and project[key].strip() for key in fields)
        valid_project = valid_project and all(
            text_list(project.get(key)) for key in ('required_acceptance', 'required_tests', 'available_agents'))
        valid_project = valid_project and bool(project['required_acceptance']) and bool(project['required_tests'])
        valid_project = valid_project and isinstance(project.get('grants'), dict)
        valid_project = valid_project and all(
            isinstance(grant, dict) and text_list(grant.get('actions')) and text_list(grant.get('recipients'))
            for grant in project['grants'].values())
        valid_identity = (isinstance(identity, dict) and isinstance(identity.get('principal'), str)
                          and bool(identity['principal'].strip()) and text_list(identity.get('projects')))
        if not valid_project or not valid_identity or not isinstance(evidence, dict):
            return failure('Receiver inputs', 'Supply valid project, identity and evidence snapshots. Required acceptance and tests must be non-empty.')
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            return failure('Clock', 'Supply a timezone-aware verification time.')
        return evaluate_request(message, project, evidence, identity, ledger_path, now)
    except (OSError, sqlite3.Error) as error:
        return failure('Ledger access', str(error))


def evaluate_request(message, project, evidence, identity, ledger_path, now):
    """Evaluate a handoff without executing commands or requesting remote URLs.

    project, evidence and identity are receiver-controlled snapshots. The CLI is a
    local reference, not an authentication service. A production adapter must
    authenticate the caller and independently retrieve immutable CI evidence.
    """
    checks = []

    def check(name, passed, detail, verdict='blocked'):
        checks.append({'name': name, 'status': 'pass' if passed else 'fail', 'detail': detail})
        if not passed:
            return {'verdict': verdict, 'checks': checks, 'side_effects': 0}
        return None

    required = ('request_id', 'task', 'project', 'sender', 'recipient', 'action', 'revision',
                'sequence', 'contract', 'acceptance', 'evidence_id', 'expires_at')
    valid = isinstance(message, dict) and all(key in message for key in required)
    if valid:
        valid = all(isinstance(message[key], str) and message[key].strip() for key in required if key not in ('sequence', 'acceptance'))
        valid = valid and type(message['sequence']) is int and message['sequence'] > 0
        valid = valid and isinstance(message['acceptance'], list) and all(isinstance(x, str) for x in message['acceptance'])
    result = check('Message structure', valid, 'Required typed handoff fields checked.')
    if result:
        return result
    result = check('Authenticated sender', identity.get('principal') == message['sender'],
                   'Sender must match the receiver-provided authenticated principal.')
    if result:
        return result
    grant = project['grants'].get(identity['principal'], {})
    allowed = (message['project'] == project['id'] and message['project'] in identity.get('projects', [])
               and message['action'] in grant.get('actions', []) and message['recipient'] in grant.get('recipients', []))
    result = check('Scope and permission', allowed, 'Project, action and destination checked against receiver-owned policy.')
    if result:
        return result
    try:
        expiry = datetime.fromisoformat(message['expires_at'].replace('Z', '+00:00'))
        valid_time = expiry.tzinfo is not None and expiry > now
    except (ValueError, TypeError):
        valid_time = False
    result = check('Request expiry', valid_time, 'Request must have a future, timezone-aware expiry.')
    if result:
        return result
    result = check('Acceptance coverage', set(project['required_acceptance']).issubset(message['acceptance']),
                   'Required acceptance identifiers must be included.')
    if result:
        return result
    result = check('Current revision', message['revision'] == project['revision'],
                   'Submitted revision must match the receiver project snapshot.')
    if result:
        return result
    Path(ledger_path).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(ledger_path, timeout=10, isolation_level=None)) as db, db:
        db.execute('CREATE TABLE IF NOT EXISTS accepted (request_id TEXT PRIMARY KEY, fingerprint TEXT, task TEXT, sequence INTEGER, result TEXT)')
        db.execute('BEGIN IMMEDIATE')
        fingerprint = digest(message)
        previous = db.execute('SELECT fingerprint, result FROM accepted WHERE request_id=?', (message['request_id'],)).fetchone()
        if previous:
            if previous[0] != fingerprint:
                return {'verdict': 'blocked', 'checks': checks + [{'name': 'Request identity', 'status': 'fail', 'detail': 'Request ID reused with a different payload.'}], 'side_effects': 0}
            return {'verdict': 'duplicate', 'checks': checks + [{'name': 'Replay handling', 'status': 'pass', 'detail': 'Already recorded. Prior result returned without another write.'}], 'side_effects': 0, 'prior_result': json.loads(previous[1])}
        latest = db.execute('SELECT MAX(sequence) FROM accepted WHERE task=?', (message['task'],)).fetchone()[0]
        result = check('Request ordering', latest is None or message['sequence'] > latest, 'Sequence must advance the accepted task state.')
        if result:
            return result
        result = check('Recipient availability', message['recipient'] in project['available_agents'],
                       'Retain the request and retry with the same ID when the recipient recovers.')
        if result:
            return result
        run = evidence.get(message['evidence_id'])
        result = check('Evidence exists', isinstance(run, dict), 'Evidence resolved from the receiver-controlled catalog.')
        if result:
            return result
        matching = (run.get('revision') == message['revision'] and run.get('project') == message['project']
                    and run.get('suite') == project['suite'] and run.get('environment') == project['environment'])
        result = check('Evidence binding', matching, 'Project, revision, suite and environment must all match.')
        if result:
            return result
        result = check('Contract compatibility', message['contract'] == project['contract'] and run.get('contract') == project['contract'],
                       'Producer and consumer must use the approved interface contract.', 'changes_required')
        if result:
            return result
        tests = run.get('tests', {})
        passed = isinstance(tests, dict) and all(tests.get(name) is True for name in project['required_tests'])
        result = check('Required test outcomes', passed, 'Every required check must be present and passing.', 'changes_required')
        if result:
            return result
        output = {'verdict': 'verified', 'checks': checks, 'side_effects': 1,
                  'revision': message['revision'], 'evidence_id': message['evidence_id'],
                  'note': 'One local verification record written. No merge, deployment or notification executed.'}
        db.execute('INSERT INTO accepted VALUES (?,?,?,?,?)', (message['request_id'], fingerprint, message['task'], message['sequence'], json.dumps(output)))
        db.commit()
        return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('message', 'project', 'evidence', 'identity', 'ledger'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--now', help='Explicit ISO timestamp for reproducing fixtures. Omit for current UTC.')
    args = parser.parse_args()
    try:
        now = datetime.fromisoformat(args.now.replace('Z', '+00:00')) if args.now else datetime.now(timezone.utc)
    except ValueError:
        parser.error('--now must be an ISO timestamp with a timezone')
    if now.tzinfo is None:
        parser.error('--now must include a timezone')
    try:
        values = [json.loads(Path(getattr(args, name)).read_text(encoding='utf-8-sig')) for name in ('message', 'project', 'evidence', 'identity')]
    except (OSError, ValueError) as error:
        print(json.dumps(failure('Input files', str(error)), indent=2))
        raise SystemExit(2)
    print(json.dumps(evaluate(*values, args.ledger, now), indent=2))


if __name__ == '__main__':
    main()
