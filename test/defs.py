from __future__ import annotations

from typing import Any, List, Tuple

from EnORM.db_engine import AbstractEngine


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
        self.conn = FakeConnection(conn_str)
        self.cursor = self.conn.cursor()
