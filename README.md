# EnORM

EnORM - EnDATA Object Relational Mapper. Get ready for an EnORMous database experience!

- [EnORM](#enorm)
  - [Example Usage](#example-usage)
  - [Documentation](#documentation)
    - [API Reference](#api-reference)
      - [`const .fkey.CASCADE` \[source\]](#const-fkeycascade-source)
      - [`class .column.Column(type_, length=None, rel=None, *, primary_key=False, default=None, nullable=True)` \[source\]](#class-columncolumntype_-lengthnone-relnone--primary_keyfalse-defaultnone-nullabletrue-source)
      - [`class .types.Date` \[source\]](#class-typesdate-source)
      - [`class .types.DateTime` \[source\]](#class-typesdatetime-source)
      - [`class .db_engine.DBEngine(conn_str)` \[source\]](#class-db_enginedbengineconn_str-source)
      - [`class .db_session.DBSession(engine)` \[source\]](#class-db_sessiondbsessionengine-source)
      - [`class .fkey.ForeignKey(foreign_model, *, reverse_name, on_delete, on_update)` \[source\]](#class-fkeyforeignkeyforeign_model--reverse_name-on_delete-on_update-source)
      - [`class .model.Model(**attrs)` \[source\]](#class-modelmodelattrs-source)
      - [`class .types.Float` \[source\]](#class-typesfloat-source)
      - [`class .types.Integer` \[source\]](#class-typesinteger-source)
      - [`class .types.Serial` \[source\]](#class-typesserial-source)
      - [`class .types.String` \[source\]](#class-typesstring-source)
      - [`class .types.Time` \[source\]](#class-typestime-source)

## Example Usage

``` python
from EnORM import CASCADE, Column, DBEngine, DBSession, Float, ForeignKey, Integer, Model, Serial, String


class Company(Model):
    __table__ = "companies"

    id = Column(Serial, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, 40)


class Employee(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    salary = Column(Float)
    age = Column(Integer)
    role = Column(String, 20, default="entry")
    company_id = Column(Serial, None, ForeignKey(Company, reverse_name="employees", on_delete=CASCADE))


eng = DBEngine("postgresql://user:secret@localhost:5432/my_db")

with DBSession(eng) as session:
    the_company = session.query(Company).filter(Company.country == "United Kingdom").first()

    new_employee = Employee(full_name="Nima Bavari Goudarzi", salary=64320.00, role="engineer", company_id=the_company.id)
    session.add(new_employee)
    
    sharks = session.query(Employee, Employee.full_name, Employee.company_id).filter(Employee.salary > 90000.00).all()
```

## Documentation

### API Reference

Reference for the EnORM public API.

#### `const .fkey.CASCADE` [[source]](EnORM/fkey.py#L7)

String literal "cascade".

#### `class .column.Column(type_, length=None, rel=None, *, primary_key=False, default=None, nullable=True)` [[source]](EnORM/column.py#L88-L160)

Abstraction of a real table column in a database.

*Parameters*

> **type_** : `typing.Type`
> 
> The type of the column as represented in SQL.
>
> **length** : `int | None` (default `None`)
>
> Max length of the value. Provided only when the type of the column is `.types.String`.
>
> **rel** : `.fkey.ForeignKey | None` (default `None`)
>
> Marker of a relationship. Provided only when a foreign relation exists.
>
> **primary_key** : `bool` (default `False`)
>
> Whether or not the column is a primary key. Keyword-only.
>
> **default** : `typing.Any` (default `None`)
>
> Default value for cells of the column to take. Keyword-only.
>
> **nullable** : `bool` (default `True`)
>
> Whether or not the cells of the column are nullable. Keyword-only.

*Attributes*

> **model** : `typing.Type`
>
> Relational model that the column belongs to.
>
> **variable_name** : `str`
>
> Name with which the column is defined.
>
> **view_name** : `str`
>
> Name of the SQL table that the column belongs to.

#### `class .types.Date` [[source]](EnORM/types.py#L8)

ORM representation of `datetime.date` objects.

#### `class .types.DateTime` [[source]](EnORM/types.py#L9)

ORM representation of `datetime.datetime` objects.

#### `class .db_engine.DBEngine(conn_str)` [[source]](EnORM/db_engine.py#L12-L24)

Connection adapter for the `.db_session.DBSession` object.

*Parameters*

> **conn_str** : `str`
>
> Database resource location, along with auth params.

*Attributes*

> **conn** : `pyodbc.Connection`
>
> DB API connection object.
>
> **cursor** : `pyodbc.Cursor`
>
> DB API cursor object.

#### `class .db_session.DBSession(engine)` [[source]](EnORM/db_session.py#L16-L103)

Singleton DB session to access the database across all uses.

*Parameters*

> **engine** : `.db_engine.AbstractEngine`
>
> DB engine that the session uses.

*Attributes*

> **engine** : `.db_engine.AbstractEngine`
>
> DB engine that the session uses.
>
> **queue** : `list`
>
> List of newly created instances of DB objects not yet persisted.
>
> **accumulator** : `list`
>
> List of ORM queries not yet executed.

*Methods*

> **query(\*fields)** -> `.query.Query`
>
> Starts a query and returns the query object.
>
> **add(obj)** -> `None`
>
> Adds a new record to the DB session.
>
> **save()** -> `None`
>
> Persists all started queries.
>
> **commit_adds()** -> `None`
>
> Persists all added records on the DB session.

#### `class .fkey.ForeignKey(foreign_model, *, reverse_name, on_delete, on_update)` [[source]](EnORM/fkey.py#L10-L36)

Representer of foreign key relations.

*Parameters*

> **foreign_model** : `typing.Type`
>
> `MappedClass` that represents a foreign model.
>
> **reverse_name** : `str`
>
> Relation name on the related class tied to this class. Keyword-only.
>
> **on_delete** : `str | None` (default `None`)
>
> Whether to delete cascade style or not. Keyword-only.
>
> **on_update** : `str | None` (default `None`)
>
> Whether to update cascade style or not. Keyword-only.

#### `class .model.Model(**attrs)` [[source]](EnORM/model.py#L13-L161)

Abstract representer of an ORM database model in Python.

*Parameters*

> **attrs** : `typing.Any`
>
> Initialization attributes.

*Attributes*

> **sql** : `str`
>
> SQL statement for new object creation.

*Methods*

> **label(alias)** -> `.column.Label`
>
> Returns the ORM representation for SQL table aliasing.

#### `class .types.Float` [[source]](EnORM/types.py#L10)

ORM representation of `float` objects.

#### `class .types.Integer` [[source]](EnORM/types.py#L7)

ORM representation of `int` objects.

#### `class .types.Serial` [[source]](EnORM/types.py#L15-L26)

ORM representation of serial types in SQL variants.

*Parameters*

> **val** : `int`
>
> Underlying integer value.

*Attributes*

> **val** : `int`
>
> Underlying integer value.

#### `class .types.String` [[source]](EnORM/types.py#L11)

ORM representation of `str` objects.

#### `class .types.Time` [[source]](EnORM/types.py#L12)

ORM representation of `datetime.time` objects.
