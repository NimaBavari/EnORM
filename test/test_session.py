from __future__ import annotations

import unittest
from typing import Any

from EnORM import Column, DBEngine, DBSession, Model, Serial, String
from EnORM.query import Query


class FakeCursor:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection
        self.open = True

    def execute(self, sql: str, *args: Any) -> Any:
        self.connection.executions.append([sql, *args])

    def close(self) -> None:
        self.open = False


class FakeConnection:
    def __init__(self, conn_str: str) -> None:
        self.conn_str = conn_str
        self.executions = []
        self.open = True

    def cursor(self) -> FakeCursor:
        return FakeCursor(self)

    def commit(self) -> None:
        self.executions = []

    def rollback(self) -> None:
        _ = self.executions.pop()

    def close(self) -> None:
        self.open = False


class FakeEngine(DBEngine):
    def __init__(self, conn_str: str) -> None:
        self.conn = FakeConnection(conn_str)
        self.cursor = self.conn.cursor()


class Order(Model):
    id = Column(Serial, primary_key=True)
    country = Column(String, 30, nullable=False)
    province = Column(String)
    city = Column(String, 30, nullable=False)


e1 = FakeEngine("remote DB connection string")
e2 = FakeEngine("another DB connection string")
sess1 = DBSession(e1)
sess2 = DBSession(e2)


class TestDBSession(unittest.TestCase):
    def test_pending_model_definitions_without_session(self) -> None:
        self.assertListEqual(
            Model.model_definition_sqls,
            [
                """DROP TABLE humans IF EXISTS; CREATE TABLE humans (id SERIAL AUTOINCREMENT PRIMARY KEY, full_name VARCHAR (100) NOT NULL, age INTEGER);""",
            ],
        )

    def test_session_singularity(self) -> None:
        self.assertIs(sess1, sess2)
        self.assertIs(DBSession._instance, sess1)
        self.assertIs(DBSession._instance, sess2)

    def test_session_engine_active_instance(self) -> None:
        self.assertIs(FakeEngine.active_instance, e2)

    def test_pending_model_definitions_with_session(self) -> None:
        self.assertListEqual(sess1.engine.conn.executions, [])

    def test_session_context_manager_exit(self) -> None:
        with DBSession(e2) as _:
            pass
        self.assertFalse(e2.cursor.open)
        self.assertFalse(e2.conn.open)

    def test_session_add_and_commit_adds(self) -> None:
        with DBSession(e2) as sess:
            order = Order(country="Germany", city="Hamburg")
            sess.add(order)
            self.assertListEqual(sess.queue, [order])
            self.assertListEqual(list(sess), [order])
            sess.commit_adds()
            self.assertListEqual(sess.engine.conn.executions, [])
            self.assertListEqual(sess.accumulator, [])

    def test_session_query(self) -> None:
        q = sess2.query(Order, Order.country).filter(Order.id == 12)
        self.assertIsInstance(q, Query)
        self.assertEqual(str(q), "SELECT orders.country FROM orders WHERE orders.id = 12")
        self.assertListEqual(sess2.accumulator, [q])

    def test_session_save(self) -> None:
        sess2.save()
        self.assertListEqual(sess2.engine.conn.executions, [])
        self.assertListEqual(sess2.accumulator, [])
