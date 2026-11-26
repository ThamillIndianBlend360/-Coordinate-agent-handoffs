import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from order_alerts import AlertService, late_order, render_alert


class OrderAlertTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.service = AlertService(str(Path(self.folder.name) / 'alerts.db'))

    def test_duplicate_delivery(self):
        event = late_order('ORD-142')
        self.service.receive(event)
        self.service.receive(event)
        self.assertEqual(len(self.service.response()), 1)

    def test_concurrent_delivery(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(self.service.receive, [late_order('ORD-142')] * 12))
        self.assertEqual(len(self.service.response()), 1)

    def test_consumer_contract(self):
        self.service.receive(late_order('ORD-142'))
        self.assertEqual(render_alert(self.service.response()[0]), 'Order ORD-142 is late')

    def test_broken_contract_is_detected(self):
        with self.assertRaises(ValueError):
            render_alert({'order_reference': 'ORD-142', 'status': 'late'})

    def test_on_time_order(self):
        self.service.receive(late_order('ORD-143', False))
        self.assertEqual(self.service.response(), [])

    def test_restart_preserves_deduplication(self):
        self.service.receive(late_order('ORD-142'))
        restarted = AlertService(self.service.database)
        restarted.receive(late_order('ORD-142'))
        self.assertEqual(len(restarted.response()), 1)

    def test_invalid_identifier(self):
        with self.assertRaises(ValueError):
            self.service.receive(late_order(''))


if __name__ == '__main__':
    unittest.main(verbosity=2)
