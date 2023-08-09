import unittest

from EnORM import CASCADE, Column, ForeignKey, Integer, Model, Serial, String
from EnORM.db_engine import AbstractEngine
from EnORM.exceptions import EntityError, MethodChainingError
from EnORM.functions import count
from EnORM.query import Query, Subquery  # , QuerySet, Record

from .defs import FakeEngine


class Human(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    age = Column(Integer)
    gender = Column(String, 1)


class Pet(Model):
    name = Column(String, 40, nullable=False)
    age = Column(Integer, nullable=False)
    owner_id = Column(Serial, None, ForeignKey(Human, reverse_name="pets", on_delete=CASCADE))


class TestQuery(unittest.TestCase):
    def test_query_init(self) -> None:
        q = Query(Human, Human.id, Human.full_name)
        self.assertSequenceEqual(q.entities, (Human, Human.id, Human.full_name))
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans")

    def test_query_join_model_without_connector(self) -> None:
        with self.assertRaises(EntityError):
            _ = Query(Human, Human.id, Human.full_name).join(Pet)

    def test_query_join_model_with_connector_without_exprs(self) -> None:
        q = Query(Pet, Pet.age).join(Human)
        self.assertEqual(str(q), "SELECT pets.age FROM pets JOIN humans ON pets.owner_id = humans.id")

    def test_query_join_model_with_connector_with_exprs(self) -> None:
        q = Query(Pet, Pet.age).join(Human, Human.id == Pet.owner_id)
        self.assertEqual(str(q), "SELECT pets.age FROM pets JOIN humans ON humans.id = pets.owner_id")

    def test_query_join_subquery_without_exprs(self) -> None:
        sq = Query(Human, Human.id, Human.full_name).subquery()
        with self.assertRaises(EntityError):
            _ = Query(Pet, Pet.name, Pet.age).join(sq)

    def test_query_join_subquery_with_exprs(self) -> None:
        sq = Query(Human, Human.id, Human.full_name).subquery()
        q = Query(Pet, Pet.name, Pet.age).join(sq, sq.full_name == Pet.name)
        sq_view_name = sq.view_name
        self.assertEqual(
            str(q),
            "SELECT pets.name, pets.age FROM pets JOIN (SELECT humans.id, humans.full_name FROM humans) AS %s ON "
            "%s.full_name = pets.name" % (sq_view_name, sq_view_name),
        )

    def test_query_filter(self) -> None:
        q = Query(Human, Human.full_name).filter(Human.age == 44, Human.id > 15)
        self.assertEqual(str(q), "SELECT humans.full_name FROM humans WHERE humans.age = 44 AND humans.id > 15")

    def test_query_filter_by(self) -> None:
        q = Query(Human, Human.full_name).filter_by(age=24, gender="M")
        self.assertEqual(str(q), "SELECT humans.full_name FROM humans WHERE humans.age = 24 AND humans.gender = M")

    def test_query_group_by(self) -> None:
        q = Query(Human, Human.id, Human.full_name).group_by(Human.age)
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans GROUP BY humans.age")

    def test_query_group_by_agg(self) -> None:
        q = Query(Human, Human.id, count(Human.age).label("age_count")).group_by("age_count")
        self.assertEqual(str(q), "SELECT humans.id, COUNT(humans.age) AS age_count FROM humans GROUP BY age_count")
        q2 = Query(Human, Human.id, count(Human.age).label("age_count")).group_by(Human.age)
        self.assertEqual(str(q2), "SELECT humans.id, COUNT(humans.age) AS age_count FROM humans GROUP BY humans.age")

    def test_query_having(self) -> None:
        q = Query(Human, Human.id, count(Human.age).label("age_count")).having(count(Human.age) > 5)
        self.assertEqual(str(q), "SELECT humans.id, COUNT(humans.age) AS age_count FROM humans HAVING humans.age > 5")

    def test_query_order_by_labelless(self) -> None:
        q = Query(Human, Human.id, Human.full_name).order_by(Human.age)
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans ORDER BY humans.age")

    def test_query_order_by_labeled(self) -> None:
        Human.full_name.aggs = []
        q = Query(Human, Human.id, Human.full_name.label("fname")).order_by("fname")
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name AS fname FROM humans ORDER BY fname")

    def test_query_limit(self) -> None:
        q = Query(Human, Human.id, Human.full_name).limit(20)
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans LIMIT 20")

    def test_query_offset(self) -> None:
        q = Query(Human, Human.id, Human.full_name).offset(10)
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans OFFSET 10")

    def test_query_slice(self) -> None:
        q = Query(Human, Human.id, Human.full_name).slice(12, 16)
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans LIMIT 4 OFFSET 12")

    def test_query_desc(self) -> None:
        with self.assertRaises(MethodChainingError):
            _ = Query(Human, Human.id, Human.full_name).desc()
        q = Query(Human, Human.id, Human.full_name).order_by(Human.age).desc()
        self.assertEqual(str(q), "SELECT humans.id, humans.full_name FROM humans ORDER BY humans.age DESC")

    def test_query_distinct(self) -> None:
        q = Query(Human, Human.id, Human.full_name).distinct()
        self.assertEqual(str(q), "SELECT DISTINCT humans.id, humans.full_name FROM humans")

    def test_query_subquery(self) -> None:
        q = Query(Human, Human.id, Human.full_name).filter(Human.age == 30)
        sq = q.subquery()
        self.assertIsInstance(sq, Subquery)
        self.assertEqual(str(sq), str(q))
        self.assertListEqual(sq.column_names, ["*", "id", "full_name"])

    def test_query_update_direct(self) -> None:
        q = Query(Human, Human.id, Human.full_name).filter(Human.age == 30)
        q.update(age=20)
        self.assertEqual(str(q), "UPDATE humans SET humans.age = 20 WHERE humans.age = 30")

    def test_query_update_indirect(self) -> None:
        AbstractEngine.active_instance = FakeEngine("blah blah blah")
        q = Query(Human, Human.id, Human.full_name).filter(Human.age == 30)
        result = q.first()
        result.age += 1
        self.assertEqual(
            str(q),
            "UPDATE humans SET humans.age = 31 WHERE humans.age = 30 AND humans.id = 17 AND "
            "humans.full_name = Jacques Trate AND humans.age = 30",
        )
        AbstractEngine.active_instance = None

    def test_query_delete(self) -> None:
        q = Query(Human, Human.id, Human.full_name).filter(Human.age == 30)
        q.delete()
        self.assertEqual(str(q), "DELETE FROM humans WHERE humans.age = 30")

    def test_query_execs(self) -> None:
        AbstractEngine.active_instance = FakeEngine("blah blah blah")
        q = Query(Human, Human.id, Human.full_name).filter(Human.age == 30)
        self.assertEqual(q.count(), 2)
        self.assertTrue(q.exists())
        AbstractEngine.active_instance = FakeEngine("blah blah blah")
