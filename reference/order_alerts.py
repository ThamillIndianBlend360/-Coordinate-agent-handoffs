"""Minimal order event producer, alert service and consumer contract."""
import sqlite3
from contextlib import closing


def late_order(order_id, late=True):
    return {'order_id': order_id, 'late': late}


class AlertService:
    def __init__(self, database):
        self.database = database
        with closing(sqlite3.connect(database)) as connection, connection:
            connection.execute('CREATE TABLE IF NOT EXISTS alerts (order_id TEXT PRIMARY KEY, status TEXT NOT NULL)')

    def receive(self, event):
        if not isinstance(event.get('order_id'), str) or not event['order_id'].strip():
            raise ValueError('A non-empty order_id is required')
        if event.get('late') is not True:
            return
        with closing(sqlite3.connect(self.database, timeout=10)) as connection, connection:
            connection.execute('INSERT OR IGNORE INTO alerts VALUES (?, ?)', (event['order_id'], 'late'))

    def response(self):
        with closing(sqlite3.connect(self.database)) as connection, connection:
            return [{'order_id': order_id, 'status': status} for order_id, status in connection.execute('SELECT order_id, status FROM alerts ORDER BY order_id')]


def render_alert(response):
    """Consumer projection used by the example frontend contract test."""
    if set(response) != {'order_id', 'status'} or response['status'] != 'late':
        raise ValueError('Consumer requires order_id and late status')
    return f"Order {response['order_id']} is late"
