import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evaluate import EVIDENCE, IDENTITY, MESSAGE, NOW, PROJECT
from handoff import evaluate


class HandoffRegressionTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.ledger = str(Path(self.folder.name) / 'ledger.db')

    def test_malformed_receiver_inputs(self):
        for project, evidence, identity in [([], EVIDENCE, IDENTITY), ({}, EVIDENCE, IDENTITY),
                                            (PROJECT, [], IDENTITY), (PROJECT, EVIDENCE, None),
                                            (dict(PROJECT, grants={'backend-agent': []}), EVIDENCE, IDENTITY)]:
            with self.subTest(project=project, identity=identity):
                result = evaluate(MESSAGE, project, evidence, identity, self.ledger, NOW)
                self.assertEqual(result['verdict'], 'blocked')
                self.assertEqual(result['checks'][0]['name'], 'Receiver inputs')

    def test_empty_required_tests_cannot_verify(self):
        result = evaluate(MESSAGE, dict(PROJECT, required_tests=[]), EVIDENCE, IDENTITY, self.ledger, NOW)
        self.assertEqual(result['verdict'], 'blocked')

    def test_malformed_test_outcomes(self):
        evidence = copy.deepcopy(EVIDENCE)
        evidence['run-419']['tests'] = []
        result = evaluate(MESSAGE, PROJECT, evidence, IDENTITY, self.ledger, NOW)
        self.assertEqual(result['verdict'], 'changes_required')

    def test_ledger_directory_error_is_structured(self):
        result = evaluate(MESSAGE, PROJECT, EVIDENCE, IDENTITY, self.folder.name, NOW)
        self.assertEqual(result['verdict'], 'blocked')
        self.assertEqual(result['checks'][0]['name'], 'Ledger access')

    def test_connection_released_after_success_and_failure(self):
        for project in [PROJECT, dict(PROJECT, available_agents=[])]:
            evaluate(MESSAGE, project, EVIDENCE, IDENTITY, self.ledger, NOW)
            Path(self.ledger).unlink()

    def test_corrected_evidence_recovers(self):
        stale = copy.deepcopy(EVIDENCE)
        stale['run-419']['revision'] = 'a19'
        first = evaluate(MESSAGE, PROJECT, stale, IDENTITY, self.ledger, NOW)
        updated = dict(MESSAGE, request_id='handoff-143', evidence_id='run-420')
        second = evaluate(updated, PROJECT, {'run-420': EVIDENCE['run-419']}, IDENTITY, self.ledger, NOW)
        self.assertEqual((first['verdict'], second['verdict']), ('blocked', 'verified'))

    def test_cli_invalid_json(self):
        invalid = Path(self.folder.name) / 'invalid.json'
        invalid.write_text('{', encoding='utf-8')
        command = [sys.executable, str(Path(__file__).with_name('handoff.py')),
                   '--ledger', self.ledger, '--now', NOW.isoformat()]
        for name in ['message', 'project', 'identity', 'evidence']:
            command.extend(['--' + name, str(invalid)])
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)['verdict'], 'blocked')
        self.assertNotIn('Traceback', run.stderr)

    def test_packaged_checker_matches_reference(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual((root / 'reference/handoff.py').read_bytes(),
                         (root / 'skill/scripts/handoff.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
