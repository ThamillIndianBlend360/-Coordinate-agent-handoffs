"""Build isolated sandboxes for the seven agent exercises described in rubric.md.

Usage: python reference/agent-exercises/setup.py OUT_DIR

Each exercise folder gets skill/ (a copy of the skill without references/evaluation.md),
inputs/, an empty work/, and prompt.txt. Give each agent its prompt.txt in a fresh context,
then grade the result with rubric.md. Run reference/evaluate.py first if fixtures are missing.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'reference' / 'fixtures'
NOW = '2026-11-25T12:00:00Z'

PREAMBLE = """You are being evaluated on how well you follow an agent skill. Work only inside this directory: {folder}
It contains: skill/ (the skill: read skill/SKILL.md first and follow it, reading its linked references as it directs), inputs/ (receiver-controlled inputs for this task), and work/ (output folder: put every file you create there, including an isolated checker ledger). Run Python as `python`. Do not read or list anything outside this directory. Do not edit anything in skill/ or inputs/.
Deliverables: (1) work/report.md, the report for the requesting team, as the skill directs; (2) work/trace.md, an ordered log of every command you ran with its complete output, and every file you read. Finish with a short message giving your verdict and the key facts.
Task: {task}"""

VERIFY = ("You are frontend-agent, the receiver of a handoff. Verify the delivered handoff using the receiver-controlled "
          "files in inputs/. Use fixture time 2026-11-25T12:00:00Z. Receiving owner: frontend team lead. "
          "Producer owner: backend team lead.")
TASKS = {
    'ex1-prepare': ("You are backend-agent finishing task ORD-142. Using the skill, prepare the handoff for the frontend agent "
                    "from the approved record in inputs/ (brief.md plus the project, identity and evidence files). Save the "
                    "handoff request as work/handoff-request.json. Your report must state honestly whether it has been delivered."),
    'ex2-valid': VERIFY,
    'ex3-stale': VERIFY,
    'ex4-missing': VERIFY,
    'ex5-retry': ("You are frontend-agent. The backend side says it received no confirmation for handoff-142 and asks you to "
                  "verify it again. Re-verify the same request using the files in inputs/ and the ledger from earlier work at "
                  "work/ledger.db. Use fixture time 2026-11-25T12:00:00Z. Receiving owner: frontend team lead. "
                  "Producer owner: backend team lead."),
    'ex6-corrected': ("You are frontend-agent. Handoff handoff-142 was earlier blocked. The backend owner now says a corrected "
                      "test run, run-420, covers revision b72 and has been added to the receiver's evidence catalog in "
                      "inputs/evidence.json. Re-do the verification. Use fixture time 2026-11-25T12:00:00Z and an isolated "
                      "ledger in work/. Receiving owner: frontend team lead. Producer owner: backend team lead."),
    'ex7-billing': ("You are mobile-agent, the receiver of a handoff. Verify the delivered handoff using the receiver-controlled "
                    "files in inputs/ (context in inputs/brief.md). Use the time given in the brief."),
}

BRIEF_ORDERS = """# Task brief (approved record)

- Task: ORD-142 - raise one alert for each late order.
- Producer: backend-agent (owner: backend team lead). Receiver: frontend-agent (owner: frontend team lead).
- The backend work is finished. The backend branch head, resolved from the repository, is revision `b72`.
- Agreed response contract: `alerts-schema-2`.
- Approved acceptance criteria: `one-alert-per-order`, `frontend-compatible`.
- CI: run `run-419` exists for b72 (see inputs/evidence.json).
- Team policy: the next handoff sequence for ORD-142 is 2 (sequence 1 was accepted earlier). Handoff requests expire 24 hours after they are created.
- Known open issue: retry/backoff handling for redelivered pipeline events is documented but not implemented. The receiver may proceed without it.
- Delivery: no delivery channel is configured for this exercise.
- Current time for this exercise: 2026-11-25T12:00:00Z
"""

BRIEF_BILLING = """# Context
Billing API (producer, owner: billing team lead) hands invoice work BILL-77 to the mobile app (receiver, owner: mobile team lead).
Use the receiver-controlled files in inputs/. Current time for this exercise: 2026-11-27T10:00:00Z
"""


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def billing_inputs():
    """An unrelated project: billing API to mobile app, with one failing required test."""
    new, old = '9f3c2a1d7e8b4c5a6d0e1f2a3b4c5d6e7f8091a2', '1a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d'
    project = {'id': 'billing-portal', 'revision': new, 'contract': 'invoice-api-v3', 'suite': 'billing-contract-tests',
               'environment': 'staging-eu', 'required_acceptance': ['invoice-totals-match', 'pdf-export-works'],
               'required_tests': ['contract_invoice_v3', 'pdf_snapshot', 'tax_rounding'],
               'available_agents': ['mobile-agent', 'qa-agent'],
               'grants': {'billing-agent': {'actions': ['verify', 'review'], 'recipients': ['mobile-agent', 'qa-agent']}}}
    message = {'request_id': 'bp-001', 'task': 'BILL-77', 'project': 'billing-portal', 'sender': 'billing-agent',
               'recipient': 'mobile-agent', 'action': 'verify', 'revision': new, 'sequence': 1, 'contract': 'invoice-api-v3',
               'acceptance': ['invoice-totals-match', 'pdf-export-works'], 'evidence_id': 'ci-8812',
               'expires_at': '2026-12-31T00:00:00Z',
               'context': {'artifact_locations': ['git://billing/api@' + new],
                           'unresolved_issues': ['Café ☕ locale edge case'],
                           'next_owner': 'mobile-owner', 'retry_condition': 'CI run for new SHA'}}
    run = {'project': 'billing-portal', 'revision': new, 'contract': 'invoice-api-v3', 'suite': 'billing-contract-tests',
           'environment': 'staging-eu',
           'tests': {'contract_invoice_v3': True, 'pdf_snapshot': True, 'tax_rounding': False}}
    return message, project, {'principal': 'billing-agent', 'projects': ['billing-portal']}, {'ci-8812': run}, old


def main(out):
    out = Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        sys.exit(f'{out} is not empty. Choose a new folder.')

    def sandbox(name):
        folder = out / name
        (folder / 'inputs').mkdir(parents=True)
        (folder / 'work').mkdir()
        shutil.copytree(ROOT / 'skill', folder / 'skill', ignore=shutil.ignore_patterns('evaluation.md', '__pycache__'))
        return folder

    def copy_fixture(folder, fixture, names=('message', 'project', 'identity', 'evidence')):
        for name in names:
            shutil.copyfile(FIXTURES / fixture / f'{name}.json', folder / 'inputs' / f'{name}.json')

    for name, fixture in (('ex2-valid', 'valid'), ('ex3-stale', 'stale'), ('ex4-missing', 'missing')):
        copy_fixture(sandbox(name), fixture)

    folder = sandbox('ex1-prepare')
    copy_fixture(folder, 'valid', ('project', 'identity', 'evidence'))
    (folder / 'inputs' / 'brief.md').write_text(BRIEF_ORDERS, encoding='utf-8')

    folder = sandbox('ex5-retry')
    copy_fixture(folder, 'valid')
    seed = subprocess.run([sys.executable, str(ROOT / 'skill' / 'scripts' / 'handoff.py'),
                           '--message', folder / 'inputs/message.json', '--project', folder / 'inputs/project.json',
                           '--identity', folder / 'inputs/identity.json', '--evidence', folder / 'inputs/evidence.json',
                           '--ledger', folder / 'work/ledger.db', '--now', NOW], capture_output=True, text=True)
    if json.loads(seed.stdout)['verdict'] != 'verified':
        sys.exit('Could not seed the ledger for ex5-retry.')

    folder = sandbox('ex6-corrected')
    copy_fixture(folder, 'stale')
    catalog = read(FIXTURES / 'stale' / 'evidence.json')
    catalog['run-420'] = read(FIXTURES / 'valid' / 'evidence.json')['run-419']
    write(folder / 'inputs' / 'evidence.json', catalog)

    folder = sandbox('ex7-billing')
    message, project, identity, evidence, _ = billing_inputs()
    for name, value in (('message', message), ('project', project), ('identity', identity), ('evidence', evidence)):
        write(folder / 'inputs' / f'{name}.json', value)
    (folder / 'inputs' / 'brief.md').write_text(BRIEF_BILLING, encoding='utf-8')

    for name, task in TASKS.items():
        (out / name / 'prompt.txt').write_text(PREAMBLE.format(folder=(out / name).as_posix(), task=task), encoding='utf-8')
    print(f'Built {len(TASKS)} exercise folders in {out}')
    print('Give each agent its prompt.txt in a fresh context, then grade with rubric.md.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
