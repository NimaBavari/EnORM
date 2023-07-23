import unittest

from EnORM.column import Column  # , VirtualColumn, Label
from EnORM.exceptions import OrphanColumn
from EnORM.fkey import CASCADE, ForeignKey
from EnORM.model import Model
from EnORM.query import Subquery
from EnORM.types import Float, Integer, Serial, String


class Human(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    age = Column(Integer)


class Pet(Model):
    name = Column(String, 40, nullable=False)
    age = Column(Integer, nullable=False)
    owner_id = Column(Serial, None, ForeignKey(Human, reverse_name="pets", on_delete=CASCADE))


MODEL_CLS = Pet
MODEL_INSTANCE = MODEL_CLS(name="Sakura", age=5, owner_id=Serial(21))

FOREIGN_MAPPED = Human
PERSON = FOREIGN_MAPPED(id=Serial(21), full_name="Nima Bavari Goudarzi", age=32)


class TestModel(unittest.TestCase):
    def test_model_type(self) -> None:
        self.assertIsInstance(MODEL_INSTANCE, Model)
        self.assertIsInstance(MODEL_INSTANCE, MODEL_CLS)

    def test_model_fields(self) -> None:
        self.assertDictEqual(
            MODEL_CLS.get_fields(), {"name": MODEL_CLS.name, "age": MODEL_CLS.age, "owner_id": MODEL_CLS.owner_id}
        )
        self.assertEqual(MODEL_CLS.name.type, String)
        self.assertEqual(MODEL_CLS.age.type, Integer)

    def test_model_table_name(self) -> None:
        self.assertEqual(MODEL_CLS.get_table_name(), "pets")

    def test_model_primary_key(self) -> None:
        self.assertIsNone(MODEL_CLS.get_primary_key_column())

    def test_model_connector_key(self) -> None:
        self.assertEqual(MODEL_CLS.get_connector_column(FOREIGN_MAPPED), MODEL_CLS.owner_id)
        self.assertIsNone(FOREIGN_MAPPED.get_connector_column(MODEL_CLS))

    def test_model_existing_compound_attr(self) -> None:
        self.assertIsInstance(PERSON.pets, Subquery)
        self.assertEqual(
            PERSON.pets.inner_sql,
            "SELECT pets.* FROM pets JOIN humans ON pets.owner_id = humans.id WHERE pets.owner_id = %s" % PERSON.id,
        )


class TestColumn(unittest.TestCase):
    def test_column_state_outside_model_context(self) -> None:
        c = Column(Float)
        with self.assertRaises(OrphanColumn):
            _ = c.model

    def test_column_attr_vals_with_model_context(self) -> None:
        self.assertEqual(MODEL_INSTANCE.name, "Sakura")
        self.assertEqual(MODEL_INSTANCE.age, 5)

        self.assertEqual(MODEL_CLS.name.model, Pet)
        self.assertEqual(MODEL_CLS.name.variable_name, "name")
        self.assertEqual(MODEL_CLS.name.view_name, "pets")

        self.assertEqual(MODEL_CLS.age.model, Pet)
        self.assertEqual(MODEL_CLS.age.variable_name, "age")
        self.assertEqual(MODEL_CLS.age.view_name, "pets")

        self.assertEqual(MODEL_CLS.owner_id.model, Pet)
        self.assertEqual(MODEL_CLS.owner_id.variable_name, "owner_id")
        self.assertEqual(MODEL_CLS.owner_id.view_name, "pets")

    def test_column_attr_types_with_model_context(self) -> None:
        self.assertEqual(MODEL_CLS.name.type, str)
        self.assertEqual(MODEL_CLS.age.type, int)
