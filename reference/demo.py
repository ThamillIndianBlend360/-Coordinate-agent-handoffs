"""Reproduce verification, replay, stale evidence, and corrected-evidence recovery."""
import copy
import tempfile
from pathlib import Path

from evaluate import EVIDENCE, IDENTITY, MESSAGE, NOW, PROJECT
from handoff import evaluate


def main():
    with tempfile.TemporaryDirectory() as folder:
        valid_ledger = str(Path(folder) / 'valid.db')
        recovery_ledger = str(Path(folder) / 'recovery.db')
        stale = copy.deepcopy(EVIDENCE)
        stale['run-419']['revision'] = 'a19'
        repaired_message = dict(MESSAGE, request_id='handoff-143', evidence_id='run-420')
        repaired_evidence = {'run-420': EVIDENCE['run-419']}
        cases = [
            ('Successful handoff', MESSAGE, EVIDENCE, valid_ledger, 'verified'),
            ('Unchanged retry', MESSAGE, EVIDENCE, valid_ledger, 'duplicate'),
            ('Older test evidence', MESSAGE, stale, recovery_ledger, 'blocked'),
            ('Corrected evidence', repaired_message, repaired_evidence, recovery_ledger, 'verified'),
        ]
        for title, message, evidence, ledger, expected in cases:
            result = evaluate(message, PROJECT, evidence, IDENTITY, ledger, NOW)
            print(f"{title}: {result['verdict']} ({result['checks'][-1]['name']})")
            if result['verdict'] != expected:
                raise SystemExit(1)


if __name__ == '__main__':
    main()
