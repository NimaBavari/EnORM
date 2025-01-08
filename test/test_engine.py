import unittest

from .defs import MYSQL_CONN_STR, ORACLE_CONN_STR, POSTGRESQL_CONN_STR, SQL_SERVER_CONN_STR, SQLITE_CONN_STR, FakeEngine


class TestEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.postgresql_engine = FakeEngine(POSTGRESQL_CONN_STR)
        self.mysql_engine = FakeEngine(MYSQL_CONN_STR)
        self.sqlite_engine = FakeEngine(SQLITE_CONN_STR)
        self.sql_server_engine = FakeEngine(SQL_SERVER_CONN_STR)
        self.oracle_engine = FakeEngine(ORACLE_CONN_STR)
        self.no_dialect_engine = FakeEngine("yeeee://haaaaa")

    def test_postgresql_conn_str(self) -> None:
        self.assertEqual(self.postgresql_engine.dialect, "postgresql")

    def test_mysql_conn_str(self) -> None:
        self.assertEqual(self.mysql_engine.dialect, "mysql")

    def test_sqlite_conn_str(self) -> None:
        self.assertEqual(self.sqlite_engine.dialect, "sqlite")

    def test_sql_server_conn_str(self) -> None:
        self.assertEqual(self.sql_server_engine.dialect, "sql_server")

    def test_oracle_conn_str(self) -> None:
        self.assertEqual(self.oracle_engine.dialect, "oracle")

    def test_no_dialect_conn_str(self) -> None:
        self.assertEqual(self.no_dialect_engine.dialect, "yeeee")

    def test_no_schema_conn_str(self) -> None:
        with self.assertRaises(ValueError):
            _ = FakeEngine("djksjjkjdskdjdj")
