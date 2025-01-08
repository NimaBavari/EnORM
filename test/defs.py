from __future__ import annotations

from typing import Any, List, Tuple

from EnORM import CASCADE, Column, ForeignKey, Integer, Model, Serial, String
from EnORM.db_engine import AbstractEngine, DialectInferrer

POSTGRESQL_CONN_STR = "postgresql://user:secret@localhost:5432/mydatabase"
MYSQL_CONN_STR = "mysql://user:secret@localhost:3306/mydatabase"
SQLITE_CONN_STR = "sqlite:///:memory:"
SQL_SERVER_CONN_STR = "mssql://user:secret@localhost:1433/mydatabase"
ORACLE_CONN_STR = "oracle://user:secret@localhost:1521?sid=ORCL"


class FakeCursor:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection
        self.open = True
        self.description = []

    def execute(self, sql: str, *args: Any) -> Any:
        self.connection.executions.append([sql, *args])
        self.description = (("id", "col"), ("full_name", "col"), ("age", "col"))

    def close(self) -> None:
        self.open = False

    def fetchall(self) -> List[Tuple[int, str]]:
        return [(17, "Jacques Trate", 30), (34, "Joanna Males", 30)]


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


class FakeEngine(AbstractEngine):
    def __init__(self, conn_str: str) -> None:
        self.dialect_inferrer = DialectInferrer(conn_str)
        self.dialect = self.dialect_inferrer.sql_dialect
        self.conn = FakeConnection(conn_str)
        self.cursor = self.conn.cursor()

    def release_connection(self, conn: FakeConnection) -> None:
        conn.close()


class Human(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    age = Column(Integer)
    gender = Column(String, 1)


class Pet(Model):
    name = Column(String, 40, nullable=False)
    age = Column(Integer, nullable=False)
    owner_id = Column(Serial, None, ForeignKey(Human, reverse_name="pets", on_delete=CASCADE))
