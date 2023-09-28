# EnORM

EnORM - EnDATA Object Relational Mapper. Get ready for an EnORMous database experience!

- [EnORM](#enorm)
  - [Example Usage](#example-usage)
  - [API Documentation](#api-documentation)
    - [`const .fkey.CASCADE`](#const-fkeycascade)
    - [`class .column.Column(type_, length=None, rel=None, *, primary_key=False, default=None, nullable=True)`](#class-columncolumntype_-lengthnone-relnone--primary_keyfalse-defaultnone-nullabletrue)
      - [Parameters](#parameters)
      - [Attributes](#attributes)
    - [`class .types.Date`](#class-typesdate)
    - [`class .types.DateTime`](#class-typesdatetime)
    - [`class .db_engine.DBEngine`](#class-db_enginedbengine)
      - [Parameters](#parameters-1)
      - [Attributes](#attributes-1)

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

## API Documentation

### `const .fkey.CASCADE`

[[source]](EnORM/fkey.py#L7)

String literal "cascade".

### `class .column.Column(type_, length=None, rel=None, *, primary_key=False, default=None, nullable=True)`

[[source]](EnORM/column.py#L88-L158)

Abstraction of a real table column in a database.

#### Parameters

> **type_** : `typing.Type`
> 
> The type of the column as represented in SQL.
>
> **length** : `int | None` (default `None`)
>
> Max length of the value. Provided only when the type of the column is `String`.
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

#### Attributes

> **model** : `typing.Type`
>
> Relational model that the column belongs to.
>
> **variable_name** : `str`
>
> The name with which the column is defined.
>
> **view_name** : `str`
>
> The name of the SQL table that the column belongs to.

### `class .types.Date`

[[source]](EnORM/types.py#L8)

ORM representation of `datetime.date` objects.

### `class .types.DateTime`

[[source]](EnORM/types.py#L9)

ORM representation of `datetime.datetime` objects.

### `class .db_engine.DBEngine`

[[source]](EnORM/db_engine.py#L12-L24)

Connection adapter for the `.db_session.DBSession` object.

#### Parameters

> **conn_str** : `str`
>
> Database resource location, along with auth params.

#### Attributes

> **conn** : `pyodbc.Connection`
>
> DB API connection object.
>
> **cursor** : `pyodbc.Cursor`
>
> DB API cursor object.
