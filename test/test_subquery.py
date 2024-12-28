import unittest

from EnORM.column import VirtualField
from EnORM.exceptions import EntityError
from EnORM.query import Query, Subquery

from .defs import Human

Human.alias = None
sq = Query(Human, Human.full_name, Human.age).filter(Human.age >= 30).subquery()


class TestSubquery(unittest.TestCase):
    def test_subquery_type(self) -> None:
        self.assertIsInstance(sq, Subquery)

    def test_subquery_existing_fields(self) -> None:
        virtual_fld = sq.full_name
        self.assertIsInstance(virtual_fld, VirtualField)
        self.assertEqual(virtual_fld.variable_name, "full_name")
        self.assertEqual(virtual_fld.view_name, sq.view_name)

    def test_subquery_nonexisting_fields(self) -> None:
        with self.assertRaises(EntityError):
            _ = sq.id

    def test_subquery_sql(self) -> None:
        self.assertEqual(sq.inner_sql, "SELECT humans.full_name, humans.age FROM humans WHERE humans.age >= 30")
        self.assertEqual(
            sq.full_sql, "(SELECT humans.full_name, humans.age FROM humans WHERE humans.age >= 30) AS %s" % sq.view_name
        )
