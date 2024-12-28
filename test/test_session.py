import unittest

from EnORM import Column, DBSession, Model, Serial, String
from EnORM.query import Query

from .defs import FakeEngine


class Order(Model):
    id = Column(Serial, primary_key=True)
    country = Column(String, 30, nullable=False)
    province = Column(String)
    city = Column(String, 30, nullable=False)


class TestDBSession(unittest.TestCase):
    def setUp(self) -> None:
        self.e1 = FakeEngine("remote DB connection string")
        self.e2 = FakeEngine("another DB connection string")
        self.sess1 = DBSession(self.e1)
        self.sess2 = DBSession(self.e2)

    def test_pending_model_definitions_without_session(self) -> None:
        self.assertListEqual(Model.model_definition_sqls, [])

    def test_session_singularity(self) -> None:
        self.assertIs(self.sess1, self.sess2)
        self.assertIs(DBSession._instance, self.sess1)
        self.assertIs(DBSession._instance, self.sess2)

    def test_session_engine_active_instance(self) -> None:
        self.assertIs(FakeEngine.active_instance, self.e2)

    def test_pending_model_definitions_with_session(self) -> None:
        self.assertListEqual(self.sess1.engine.conn.executions, [])

    def test_session_context_manager_exit(self) -> None:
        with DBSession(self.e2) as _:
            pass
        self.assertFalse(self.e2.cursor.open)
        self.assertFalse(self.e2.conn.open)

    def test_session_add_and_commit_adds(self) -> None:
        with DBSession(self.e2) as sess:
            order = Order(country="Germany", city="Hamburg")
            sess.add(order)
            self.assertListEqual(sess.persistence_manager.queue, [order])
            self.assertListEqual(list(sess), [order])
            sess.persistence_manager.auto_commit_adds()
            self.assertListEqual(sess.engine.conn.executions, [])
            self.assertListEqual(sess.query_executor.accumulator, [])

    def test_session_query(self) -> None:
        q = self.sess2.query(Order, Order.country).filter(Order.id == 12)
        self.assertIsInstance(q, Query)
        self.assertEqual(str(q), "SELECT orders.country FROM orders WHERE orders.id = 12")
        self.assertListEqual(self.sess2.query_executor.accumulator, [q])

    def test_session_save(self) -> None:
        self.sess2.save()
        self.assertListEqual(self.sess2.engine.conn.executions, [])
        self.assertListEqual(self.sess2.query_executor.accumulator, [])
