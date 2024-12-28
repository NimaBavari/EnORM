import unittest

from EnORM.column import Scalar
from EnORM.functions import (
    char_length,
    concat,
    current_date,
    current_time,
    current_timestamp,
    current_user,
    local_time,
    local_timestamp,
    now,
    random,
    session_user,
    user,
)
from EnORM.query import Query

from .defs import Human


class TestFunctions(unittest.TestCase):
    def test_char_length(self) -> None:
        Human.alias = None
        long_names_query = Query(Human).filter(char_length(Human.full_name) > 15)
        self.assertEqual(str(long_names_query), "SELECT humans.* FROM humans WHERE CHAR_LENGTH(humans.full_name) > 15")
        bare_ex = char_length("example")
        self.assertIsInstance(bare_ex, Scalar)
        self.assertEqual(bare_ex.compound_variable_name, "CHAR_LENGTH(example)")

    def test_concat(self) -> None:
        res = concat("this", " is just", " a test", ".")
        self.assertEqual(res, "this is just a test.")

    def test_current_date(self) -> None:
        res = current_date()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "CURRENT_DATE")

    def test_current_time(self) -> None:
        res_wo_prec = current_time()
        res_w_prec = current_time(6)
        self.assertIsInstance(res_wo_prec, Scalar)
        self.assertIsInstance(res_w_prec, Scalar)
        self.assertEqual(res_wo_prec.compound_variable_name, "CURRENT_TIME")
        self.assertEqual(res_w_prec.compound_variable_name, "CURRENT_TIME(6)")

    def test_current_timestamp(self) -> None:
        res_wo_prec = current_timestamp()
        res_w_prec = current_timestamp(6)
        self.assertIsInstance(res_wo_prec, Scalar)
        self.assertIsInstance(res_w_prec, Scalar)
        self.assertEqual(res_wo_prec.compound_variable_name, "CURRENT_TIMESTAMP")
        self.assertEqual(res_w_prec.compound_variable_name, "CURRENT_TIMESTAMP(6)")

    def test_current_user(self) -> None:
        res = current_user()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "CURRENT_USER")

    def test_local_time(self) -> None:
        res_wo_prec = local_time()
        res_w_prec = local_time(4)
        self.assertIsInstance(res_wo_prec, Scalar)
        self.assertIsInstance(res_w_prec, Scalar)
        self.assertEqual(res_wo_prec.compound_variable_name, "LOCALTIME")
        self.assertEqual(res_w_prec.compound_variable_name, "LOCALTIME(4)")

    def test_local_timestamp(self) -> None:
        res = local_timestamp()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "LOCALTIMESTAMP")

    def test_now(self) -> None:
        res = now()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "NOW()")

    def test_random(self) -> None:
        res = random()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "RANDOM()")

    def test_session_user(self) -> None:
        res = session_user()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "SESSION_USER")

    def test_user(self) -> None:
        res = user()
        self.assertIsInstance(res, Scalar)
        self.assertEqual(res.compound_variable_name, "USER()")
