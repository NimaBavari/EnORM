# EnORM

EnORM—EnDATA Object Relational Mapper.

<!-- TOC -->

- [EnORM](#enorm)
    - [Example Usage](#example-usage)
    - [Dev Scripts](#dev-scripts)
        - [Set Up Dev Environment](#set-up-dev-environment)
        - [Linting and Formatting](#linting-and-formatting)
        - [Testing](#testing)
    - [Documentation](#documentation)
        - [API Reference](#api-reference)
            - [const .fkey.CASCADE [source]](#const-fkeycascade-source)
            - [class .column.Columntype_, length=None, rel=None, *, primary_key=False, default=None, nullable=True [source]](#class-columncolumntype_-lengthnone-relnone--primary_keyfalse-defaultnone-nullabletrue-source)
            - [class .types.Date [source]](#class-typesdate-source)
            - [class .types.DateTime [source]](#class-typesdatetime-source)
            - [class .db_engine.DBEngineconn_str [source]](#class-db_enginedbengineconn_str-source)
            - [class .db_session.DBSessionengine [source]](#class-db_sessiondbsessionengine-source)
            - [class .fkey.ForeignKeyforeign_model, *, reverse_name, on_delete, on_update [source]](#class-fkeyforeignkeyforeign_model--reverse_name-on_delete-on_update-source)
            - [class .model.Model**attrs [source]](#class-modelmodelattrs-source)
            - [class .types.Float [source]](#class-typesfloat-source)
            - [class .types.Integer [source]](#class-typesinteger-source)
            - [class .types.Serial [source]](#class-typesserial-source)
            - [class .types.String [source]](#class-typesstring-source)
            - [class .types.Time [source]](#class-typestime-source)
            - [func aggfield, name_in_sql -> .column.BaseColumn [source]](#func-aggfield-name_in_sql---columnbasecolumn-source)
            - [func countfield -> .column.BaseColumn [source]](#func-countfield---columnbasecolumn-source)
            - [func sum_field -> .column.BaseColumn [source]](#func-sum_field---columnbasecolumn-source)
            - [func avgfield -> .column.BaseColumn [source]](#func-avgfield---columnbasecolumn-source)
            - [func min_field -> .column.BaseColumn [source]](#func-min_field---columnbasecolumn-source)
            - [func max_field -> .column.BaseColumn [source]](#func-max_field---columnbasecolumn-source)
            - [func char_lengthc -> .column.Scalar [source]](#func-char_lengthc---columnscalar-source)
            - [func concat*parts -> str [source]](#func-concatparts---str-source)
            - [func current_date -> .column.Scalar [source]](#func-current_date---columnscalar-source)
            - [func current_timeprecision=None -> .column.Scalar [source]](#func-current_timeprecisionnone---columnscalar-source)
            - [func current_timestampprecision=None -> .column.Scalar [source]](#func-current_timestampprecisionnone---columnscalar-source)
            - [func current_user -> .column.Scalar [source]](#func-current_user---columnscalar-source)
            - [func local_timeprecision=None -> .column.Scalar [source]](#func-local_timeprecisionnone---columnscalar-source)
            - [func local_timestamp -> .column.Scalar [source]](#func-local_timestamp---columnscalar-source)
            - [func now -> .column.Scalar [source]](#func-now---columnscalar-source)
            - [func random -> .column.Scalar [source]](#func-random---columnscalar-source)
            - [func session_user -> .column.Scalar [source]](#func-session_user---columnscalar-source)
            - [func user -> .column.Scalar [source]](#func-user---columnscalar-source)

<!-- /TOC -->

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

## Dev Scripts

### Set Up Dev Environment

Run:

```sh
make set_dev_env
```

to set up the dev environment.

This sets:
- git pre-commit hook

If you intend to touch the code, set up dev environment first.

### Linting and Formatting

Run:

```sh
make cleanup
```

to run linting and formatting.

### Testing

Run:

```sh
make test
```

to start the tests.

## Documentation

### API Reference

Reference for the EnORM public API.

#### `const .fkey.CASCADE` [[source]](EnORM/fkey.py#L7)

String literal "cascade".

#### `class .column.Column(type_, length=None, rel=None, *, primary_key=False, default=None, nullable=True)` [[source]](EnORM/column.py#L99-L172)

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

*Methods*

> **label(alias)** -> `.column.BaseColumn`
>
> Returns the ORM representation for SQL column aliasing.

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

#### `class .db_session.DBSession(engine)` [[source]](EnORM/db_session.py#L95-L169)

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
> **transaction_manager** : `.db_session.TransactionManager`
>
> Transaction manager.
>
> **persistence_manager** : `.db_session.PersistenceManager`
>
> Persistence manager.
>
> **query_executor** : `.db_session.QueryExecutor`
>
> Query executor.

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

#### `class .model.Model(**attrs)` [[source]](EnORM/model.py#L30-L178)

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

> **label(alias)** -> `Type[.model.Model]`
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

#### `func agg(field, name_in_sql)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L8-L11)

Describes the basis for all aggregate functions.

*Parameters*

> **field** : `.column.BaseColumn`
>
> Argument.
>
> **name_in_sql** : `str`
>
> Name of the function in SQL.

#### `func count(field)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L14-L16)

Describes the SQL aggregate function `COUNT`.

#### `func sum_(field)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L19-L21)

Describes the SQL aggregate function `SUM`.

#### `func avg(field)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L24-L26)

Describes the SQL aggregate function `AVG`.

#### `func min_(field)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L29-L31)

Describes the SQL aggregate function `MIN`.

#### `func max_(field)` -> `.column.BaseColumn` [[source]](EnORM/functions.py#L34-L36)

Describes the SQL aggregate function `MAX`.

#### `func char_length(c)` -> `.column.Scalar` [[source]](EnORM/functions.py#L39-L44)

Describes the SQL function `CHAR_LENGTH`.

*Parameters*

> **c** : `.column.BaseColumn | str`
>
> Generic column or its string value.

#### `func concat(*parts)` -> `str` [[source]](EnORM/functions.py#L47-L49)

Concatenates multiple strings into one.

*Parameters*

> **parts** : list of `str`
>
> Separate parts.

#### `func current_date()` -> `.column.Scalar` [[source]](EnORM/functions.py#L52-L54)

Describes the SQL function `CURRENT_DATE`.

#### `func current_time(precision=None)` -> `.column.Scalar` [[source]](EnORM/functions.py#L57-L62)

Describes the SQL function `CURRENT_TIME`.

*Parameters*

> **precision** : `int | None` (default `None`)
>
> Number of significant decimal digits.

#### `func current_timestamp(precision=None)` -> `.column.Scalar` [[source]](EnORM/functions.py#L65-L70)

Describes the SQL function `CURRENT_TIMESTAMP`.

*Parameters*

> **precision** : `int | None` (default `None`)
>
> Number of significant decimal digits.

#### `func current_user()` -> `.column.Scalar` [[source]](EnORM/functions.py#L73-L75)

Describes the SQL function `CURRENT_USER`.

#### `func local_time(precision=None)` -> `.column.Scalar` [[source]](EnORM/functions.py#L78-L83)

Describes the SQL function `LOCALTIME`.

*Parameters*

> **precision** : `int | None` (default `None`)
>
> Number of significant decimal digits.

#### `func local_timestamp()` -> `.column.Scalar` [[source]](EnORM/functions.py#L86-L88)

Describes the SQL function `LOCALTIMESTAMP`.

#### `func now()` -> `.column.Scalar` [[source]](EnORM/functions.py#L91-L93)

Describes the SQL function `NOW`.

#### `func random()` -> `.column.Scalar` [[source]](EnORM/functions.py#L96-L98)

Describes the SQL function `RANDOM`.

#### `func session_user()` -> `.column.Scalar` [[source]](EnORM/functions.py#L101-L103)

Describes the SQL function `SESSION_USER`.

#### `func user()` -> `.column.Scalar` [[source]](EnORM/functions.py#L106-L108)

Describes the SQL function `USER`.
