import unittest

from EnORM import CASCADE, Column, Float, ForeignKey, Integer, Model, Serial, String
from EnORM.exceptions import FieldNotExist, OrphanColumn
from EnORM.query import Subquery

from .defs import Human, Pet

MODEL_CLS = Pet
FOREIGN_MAPPED = Human

MODEL_INSTANCE = MODEL_CLS(name="Sakura", age=5, owner_id=Serial(21))
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
        FOREIGN_MAPPED.alias = None
        self.assertEqual(MODEL_CLS.get_connector_column(FOREIGN_MAPPED), MODEL_CLS.owner_id)
        self.assertIsNone(FOREIGN_MAPPED.get_connector_column(MODEL_CLS))

    def test_model_existing_compound_attr(self) -> None:
        FOREIGN_MAPPED.alias = None
        self.assertIsInstance(PERSON.pets, Subquery)
        self.assertEqual(
            PERSON.pets.inner_sql,
            "SELECT pets.* FROM pets JOIN humans ON pets.owner_id = humans.id WHERE pets.owner_id = %s" % PERSON.id,
        )

    def test_model_nonexisting_compound_attr(self) -> None:
        with self.assertRaises(FieldNotExist):
            _ = PERSON.tots

    def test_model_label(self) -> None:
        FOREIGN_MAPPED.alias = None
        table_as = FOREIGN_MAPPED.label("h")
        self.assertIsInstance(table_as, type)
        self.assertEqual(table_as, FOREIGN_MAPPED)
        self.assertEqual(table_as.alias, "h")


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

    def test_column_label(self) -> None:
        column_as = MODEL_CLS.age.label("pet_age")
        self.assertIsInstance(column_as, Column)
        self.assertEqual(column_as, MODEL_CLS.age)
        self.assertEqual(column_as.alias, "pet_age")


class TestForeignKey(unittest.TestCase):
    def test_foreign_key(self):
        FOREIGN_MAPPED.alias = None
        self.assertIsInstance(MODEL_CLS.owner_id.rel, ForeignKey)
        self.assertIs(MODEL_CLS.owner_id.rel.foreign_model, FOREIGN_MAPPED)
        self.assertIs(MODEL_CLS.owner_id.rel.reverse_name, "pets")
        self.assertIs(MODEL_CLS.owner_id.rel.on_delete, CASCADE)
