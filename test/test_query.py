import unittest

from EnORM import CASCADE, Column, ForeignKey, Integer, Model, Serial, String
from EnORM.exceptions import EntityError
from EnORM.query import Query  # , QuerySet, Record


class Human(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    age = Column(Integer)


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
            "SELECT pets.name, pets.age FROM pets JOIN (SELECT humans.id, humans.full_name FROM humans) AS %s ON %s.full_name = pets.name"
            % (sq_view_name, sq_view_name),
        )
