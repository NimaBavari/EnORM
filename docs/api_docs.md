# Table of Contents

* [column](#column)
  * [BaseColumn](#column.BaseColumn)
    * [binary\_ops](#column.BaseColumn.binary_ops)
    * [label](#column.BaseColumn.label)
  * [Scalar](#column.Scalar)
  * [Field](#column.Field)
  * [Column](#column.Column)
    * [model](#column.Column.model)
    * [variable\_name](#column.Column.variable_name)
    * [view\_name](#column.Column.view_name)
  * [VirtualField](#column.VirtualField)
* [functions](#functions)
  * [agg](#functions.agg)
  * [count](#functions.count)
  * [sum\_](#functions.sum_)
  * [avg](#functions.avg)
  * [min\_](#functions.min_)
  * [max\_](#functions.max_)
  * [char\_length](#functions.char_length)
  * [concat](#functions.concat)
  * [current\_date](#functions.current_date)
  * [current\_time](#functions.current_time)
  * [current\_timestamp](#functions.current_timestamp)
  * [current\_user](#functions.current_user)
  * [local\_time](#functions.local_time)
  * [local\_timestamp](#functions.local_timestamp)
  * [now](#functions.now)
  * [random](#functions.random)
  * [session\_user](#functions.session_user)
  * [user](#functions.user)
* [constants](#constants)
* [fkey](#fkey)
  * [ForeignKey](#fkey.ForeignKey)
* [pool](#pool)
  * [ConnectionPool](#pool.ConnectionPool)
    * [acquire](#pool.ConnectionPool.acquire)
    * [release](#pool.ConnectionPool.release)
    * [close\_all](#pool.ConnectionPool.close_all)
* [exceptions](#exceptions)
  * [IncompatibleArgument](#exceptions.IncompatibleArgument)
  * [EntityError](#exceptions.EntityError)
  * [MethodChainingError](#exceptions.MethodChainingError)
  * [BackendSupportError](#exceptions.BackendSupportError)
  * [Fixed](#exceptions.Fixed)
  * [ValueOutOfBound](#exceptions.ValueOutOfBound)
  * [FieldNotExist](#exceptions.FieldNotExist)
  * [WrongFieldType](#exceptions.WrongFieldType)
  * [MissingRequiredField](#exceptions.MissingRequiredField)
  * [QueryFormatError](#exceptions.QueryFormatError)
  * [MultipleResultsFound](#exceptions.MultipleResultsFound)
  * [OrphanColumn](#exceptions.OrphanColumn)
* [subquery](#subquery)
  * [Subquery](#subquery.Subquery)
* [custom\_types](#custom_types)
* [query](#query)
  * [Record](#query.Record)
    * [is\_complete\_row](#query.Record.is_complete_row)
  * [QuerySet](#query.QuerySet)
  * [QueryBuilder](#query.QueryBuilder)
    * [add\_to\_data](#query.QueryBuilder.add_to_data)
    * [build](#query.QueryBuilder.build)
  * [Query](#query.Query)
    * [join](#query.Query.join)
    * [filter](#query.Query.filter)
    * [filter\_by](#query.Query.filter_by)
    * [group\_by](#query.Query.group_by)
    * [having](#query.Query.having)
    * [order\_by](#query.Query.order_by)
    * [limit](#query.Query.limit)
    * [offset](#query.Query.offset)
    * [slice](#query.Query.slice)
    * [desc](#query.Query.desc)
    * [distinct](#query.Query.distinct)
    * [subquery](#query.Query.subquery)
    * [get](#query.Query.get)
    * [all](#query.Query.all)
    * [first](#query.Query.first)
    * [one\_or\_none](#query.Query.one_or_none)
    * [exists](#query.Query.exists)
    * [count](#query.Query.count)
    * [update](#query.Query.update)
    * [delete](#query.Query.delete)
* [db\_session](#db_session)
  * [TransactionManager](#db_session.TransactionManager)
    * [commit](#db_session.TransactionManager.commit)
    * [rollback](#db_session.TransactionManager.rollback)
    * [close](#db_session.TransactionManager.close)
  * [PersistenceManager](#db_session.PersistenceManager)
    * [add](#db_session.PersistenceManager.add)
    * [auto\_commit\_adds](#db_session.PersistenceManager.auto_commit_adds)
  * [QueryExecutor](#db_session.QueryExecutor)
    * [query](#db_session.QueryExecutor.query)
    * [execute\_queries](#db_session.QueryExecutor.execute_queries)
  * [SQLTypeResolver](#db_session.SQLTypeResolver)
    * [get\_native\_type\_name](#db_session.SQLTypeResolver.get_native_type_name)
  * [DBSession](#db_session.DBSession)
    * [query](#db_session.DBSession.query)
    * [add](#db_session.DBSession.add)
    * [save](#db_session.DBSession.save)
* [model](#model)
  * [SchemaDefinition](#model.SchemaDefinition)
    * [generate\_sql](#model.SchemaDefinition.generate_sql)
  * [Model](#model.Model)
    * [label](#model.Model.label)
    * [sql](#model.Model.sql)
* [\_\_init\_\_](#__init__)
* [db\_engine](#db_engine)
  * [DialectInferrer](#db_engine.DialectInferrer)
    * [sql\_dialect](#db_engine.DialectInferrer.sql_dialect)
  * [AbstractEngine](#db_engine.AbstractEngine)
  * [DBEngine](#db_engine.DBEngine)
    * [get\_connection](#db_engine.DBEngine.get_connection)
    * [release\_connection](#db_engine.DBEngine.release_connection)
* [backends](#backends)
  * [Serial](#backends.Serial)
* [backends.oracle](#backends.oracle)
* [backends.postgresql](#backends.postgresql)
* [backends.mysql](#backends.mysql)
* [backends.sql\_server](#backends.sql_server)

<a id="column"></a>

# column

Contains column-like classes.

<a id="column.BaseColumn"></a>

## BaseColumn Objects

```python
class BaseColumn()
```

Base class for representing a column-like value in a database.

<a id="column.BaseColumn.binary_ops"></a>

#### binary\_ops

```python
def binary_ops(other: Any, operator: str) -> str
```

String representation for direct Python binary operations between :class:`column.BaseColumn` objects.

E.g.::

    Order.price <= 200.00

or

    u = User(fullname="Abigail Smith", age=30)
    User.age > u.age

Has the following:

**Arguments**:

- `other`: a literal or a :class:`column.BaseColumn` object, to compare with this object
- `operator`: SQL operator, represented as a string.

<a id="column.BaseColumn.label"></a>

#### label

```python
def label(alias: str) -> BaseColumn
```

Returns the ORM representation for SQL column aliasing.

**Arguments**:

- `alias`: alias as a string.

<a id="column.Scalar"></a>

## Scalar Objects

```python
class Scalar(BaseColumn)
```

Scalar value as a column.

**Arguments**:

- `repr_`: SQL representation of the scalar name.

<a id="column.Field"></a>

## Field Objects

```python
class Field(BaseColumn)
```

Representer of all real and virtual fields.

<a id="column.Column"></a>

## Column Objects

```python
class Column(Field)
```

Abstraction of a real table column in a database.

**Arguments**:

- `type_`: type of value that this column expects. Must be one of the types defined in :module:`.backends`
- `length`: max length of the expected value. Only works with :class:`.backends.String`. Optional
- `rel`: marker of a relationship -- a foreign key. Optional
- `primary_key`: keyword-only. Whether or not the column is a primary key. Optional
- `default`: keyword-only. Default value for cells of the column to take. Optional
- `nullable`: keyword-only. Whether or not the cells of the column are nullable. Optional.

<a id="column.Column.model"></a>

#### model

```python
@property
def model() -> Type
```

Relational model that the column belongs to.

<a id="column.Column.variable_name"></a>

#### variable\_name

```python
@property
def variable_name() -> str
```

Name with which the column is defined.

<a id="column.Column.view_name"></a>

#### view\_name

```python
@property
def view_name() -> str
```

Name of the SQL table that the column belongs to.

<a id="column.VirtualField"></a>

## VirtualField Objects

```python
class VirtualField(Field)
```

Abstraction of a virtual table column in a database.

Never instantiated directly but is derived from actual columns, e.g. by accessing a field of a

**Arguments**:

- `variable_name`: name, as a string, of the column as it is defined in the source
- `view_name`: name of the view in which the column belongs.

<a id="functions"></a>

# functions

Contains ORM functions, both aggregate and non-aggregate ones.

<a id="functions.agg"></a>

#### agg

```python
def agg(field: BaseColumn, name_in_sql: str) -> BaseColumn
```

Describes the basis for all aggregate functions.

<a id="functions.count"></a>

#### count

```python
def count(field: BaseColumn) -> BaseColumn
```

Describes the SQL aggregate function `COUNT`.

<a id="functions.sum_"></a>

#### sum\_

```python
def sum_(field: BaseColumn) -> BaseColumn
```

Describes the SQL aggregate function `SUM`.

<a id="functions.avg"></a>

#### avg

```python
def avg(field: BaseColumn) -> BaseColumn
```

Describes the SQL aggregate function `AVG`.

<a id="functions.min_"></a>

#### min\_

```python
def min_(field: BaseColumn) -> BaseColumn
```

Describes the SQL aggregate function `MIN`.

<a id="functions.max_"></a>

#### max\_

```python
def max_(field: BaseColumn) -> BaseColumn
```

Describes the SQL aggregate function `MAX`.

<a id="functions.char_length"></a>

#### char\_length

```python
def char_length(c: BaseColumnRef) -> Scalar
```

Describes the SQL function `CHAR_LENGTH`.

<a id="functions.concat"></a>

#### concat

```python
def concat(*parts: str) -> str
```

Concatenates multiple strings into one.

<a id="functions.current_date"></a>

#### current\_date

```python
def current_date() -> Scalar
```

Describes the SQL function `CURRENT_DATE`.

<a id="functions.current_time"></a>

#### current\_time

```python
def current_time(precision: Optional[int] = None) -> Scalar
```

Describes the SQL function `CURRENT_TIME`.

<a id="functions.current_timestamp"></a>

#### current\_timestamp

```python
def current_timestamp(precision: Optional[int] = None) -> Scalar
```

Describes the SQL function `CURRENT_TIMESTAMP`.

<a id="functions.current_user"></a>

#### current\_user

```python
def current_user() -> Scalar
```

Describes the SQL function `CURRENT_USER`.

<a id="functions.local_time"></a>

#### local\_time

```python
def local_time(precision: Optional[int] = None) -> Scalar
```

Describes the SQL function `LOCALTIME`.

<a id="functions.local_timestamp"></a>

#### local\_timestamp

```python
def local_timestamp() -> Scalar
```

Describes the SQL function `LOCALTIMESTAMP`.

<a id="functions.now"></a>

#### now

```python
def now() -> Scalar
```

Describes the SQL function `NOW`.

<a id="functions.random"></a>

#### random

```python
def random() -> Scalar
```

Describes the SQL function `RANDOM`.

<a id="functions.session_user"></a>

#### session\_user

```python
def session_user() -> Scalar
```

Describes the SQL function `SESSION_USER`.

<a id="functions.user"></a>

#### user

```python
def user() -> Scalar
```

Describes the SQL function `USER`.

<a id="constants"></a>

# constants

Contains library-wide constants.

<a id="fkey"></a>

# fkey

Contains :class:`.fkey.ForeignKey`.

<a id="fkey.ForeignKey"></a>

## ForeignKey Objects

```python
class ForeignKey()
```

Representer of foreign key relations.

This class implements logic handling relations across tables through connector columns.

**Arguments**:

- `foreign_model`: `MappedClass` that represents a foreign model
- `reverse_name`: keyword-only. Relation name on the related class tied to this class
- `on_delete`: keyword-only. Whether to delete cascade style or not. Optional
- `on_update`: keyword-only. Whether to update cascade style or not. Optional.

<a id="pool"></a>

# pool

Contains :class:`.pool.ConnectionPool`.

<a id="pool.ConnectionPool"></a>

## ConnectionPool Objects

```python
class ConnectionPool()
```

Thread-safe connection pool for managing database connections.

Uses a FIFO queue to manage connections. Implements lazy initialization of connections.

**Arguments**:

- `conn_str`: database location, along with auth params
- `pool_size`: size of the connection pool.

<a id="pool.ConnectionPool.acquire"></a>

#### acquire

```python
def acquire(timeout: Optional[float] = None) -> pyodbc.Connection
```

Acquires a connection from the pool.

<a id="pool.ConnectionPool.release"></a>

#### release

```python
def release(conn: pyodbc.Connection) -> None
```

Releases a connection back to the pool.

<a id="pool.ConnectionPool.close_all"></a>

#### close\_all

```python
def close_all() -> None
```

Closes all connections in the pool.

<a id="exceptions"></a>

# exceptions

Contains definitions for custom exceptions.

<a id="exceptions.IncompatibleArgument"></a>

## IncompatibleArgument Objects

```python
class IncompatibleArgument(TypeError)
```

Raised when parameters of incompatible values or incompatible types are used together.

<a id="exceptions.EntityError"></a>

## EntityError Objects

```python
class EntityError(ValueError)
```

Raised when entities (column-like objects) are not used correctly.

<a id="exceptions.MethodChainingError"></a>

## MethodChainingError Objects

```python
class MethodChainingError(ValueError)
```

Raised when a wrong sequence of methods are chained together on :class:`.query.Query`.

<a id="exceptions.BackendSupportError"></a>

## BackendSupportError Objects

```python
class BackendSupportError(ValueError)
```

Raised when a backend or backend-specific type is not supported.

<a id="exceptions.Fixed"></a>

## Fixed Objects

```python
class Fixed(Exception)
```

Base class for all messaged exceptions.

<a id="exceptions.ValueOutOfBound"></a>

## ValueOutOfBound Objects

```python
class ValueOutOfBound(Fixed)
```

Raised when a value of an EnORM type is out of bounds.

<a id="exceptions.FieldNotExist"></a>

## FieldNotExist Objects

```python
class FieldNotExist(Fixed)
```

Raised when the inquired field does not exist in a multi-field object.

<a id="exceptions.WrongFieldType"></a>

## WrongFieldType Objects

```python
class WrongFieldType(Fixed)
```

Raised when the value of a column is of another type than is declared.

<a id="exceptions.MissingRequiredField"></a>

## MissingRequiredField Objects

```python
class MissingRequiredField(Fixed)
```

Raised when a new row is instantiated without a required field.

<a id="exceptions.QueryFormatError"></a>

## QueryFormatError Objects

```python
class QueryFormatError(Fixed)
```

Raised when a query is formatted incorrectly.

<a id="exceptions.MultipleResultsFound"></a>

## MultipleResultsFound Objects

```python
class MultipleResultsFound(Fixed)
```

Raised when multiple results are found while a single result is expected.

<a id="exceptions.OrphanColumn"></a>

## OrphanColumn Objects

```python
class OrphanColumn(Fixed)
```

Raised when a column is instantiated outside a model definition.

<a id="subquery"></a>

# subquery

Contains :class:`.subquery.Subquery` and its helpers.

<a id="subquery.Subquery"></a>

## Subquery Objects

```python
class Subquery()
```

Representer of an SQL subquery.

A subquery is a nested SELECT statement that is used within another SQL statement.

Never directly instantiated, but rather initialised by invoking :meth:`.query.Query.subquery()`.

**Arguments**:

- `inner_sql`: SQL string of the view represented by the subquery
- `column_names`: original names of the columns in that view.

<a id="custom_types"></a>

# custom\_types

Contains definitions for frequently used composite types.

<a id="query"></a>

# query

Contains :class:`.query.Query` and its helpers.

Also contains the class for complete and incomplete row-like objects, namely, :class:`.query.Record`, and the class for
any collection of them :class:`.query.QuerySet`.

<a id="query.Record"></a>

## Record Objects

```python
class Record()
```

Representer of each of a database fetch results.

This can be a complete or an incomplete table row.

Proxy class, never directly instantiated.

**Arguments**:

- `dct`: data that the record is based on
- `query`: query that fetched this record, among possibly others.

<a id="query.Record.is_complete_row"></a>

#### is\_complete\_row

```python
@property
def is_complete_row() -> bool
```

Whether or not this record is a complete row.

<a id="query.QuerySet"></a>

## QuerySet Objects

```python
class QuerySet()
```

A class that represents database fetch results.

Immutable, ordered. Indexable, iterable, subscriptable.

NOTE that this is terminal: no any query methods can be applied to the instance anymore.

**Arguments**:

- `lst`: underlying list of records.

<a id="query.QueryBuilder"></a>

## QueryBuilder Objects

```python
class QueryBuilder()
```

Builder of an SQL query.

<a id="query.QueryBuilder.add_to_data"></a>

#### add\_to\_data

```python
def add_to_data(key: str, val: str) -> None
```

Appends a value to the list `self.data[key]`.

If `key` does not exist in `self.data`, instantiates it as an empty list and append to it.

<a id="query.QueryBuilder.build"></a>

#### build

```python
def build() -> str
```

Builds and returns the final SQL query.

<a id="query.Query"></a>

## Query Objects

```python
class Query()
```

Main abstraction for querying for the whole ORM.

There are two ways to generate :class:`.query.Query` objects: either by calling the
`.db_session.DBSession.query` method, which is the most usual way, or, less commonly, by instantiating
`.query.Query` directly.

Gets as an argument:

**Arguments**:

- `entities`: -- which correspond to the "columns" of the matched results. May contain at most one `MappedClass`
instance.

NOTE that `MappedClass` is any subclass of :class:`.model.Model`.

<a id="query.Query.join"></a>

#### join

```python
def join(mapped: JoinEntity, *exprs: Any) -> Query
```

Joins the mapped to the the current instance.

:param mapped:  joined entity
:param exprs:   list of expressions on which to join.

:return:        resulting :class:`.query.Query` object.

:param:`mapped` is either another model or a subquery instance. In the first case, one can join with or without
expressions. And if the other model is joined without expressions, an expression is constructed via its primary
key. Note that this is only possible when the other model is a parent model to this one.

E.g.::

    session.query(User, email_address, last_visited).join(Organisation).all()

    SELECT users.email_address, users.last_visited FROM users
    JOIN organisations ON users.org_id = organisations.id;

If the other model is joined with expressions, those expressions are used.

E.g.::

    session.query(Sale, category_name, quantity)
        .join(Category, Category.id == Sales.category_id, Sale.quantity > 100, Category.is_current == 1)
        .all()

    SELECT sales.category_name, sales.quantity FROM sales
    JOIN categories
        ON categories.id = sales.category_id AND sales.quantity > 100 AND categories.is_current = 1;

In case :param:`mapped` is a subquery object, one can only join with expressions.

E.g.::

    sq = session.query(Human, Human.id, Human.full_name).subquery()
    session.query(Pet, Pet.name, Pet.age).join(sq, sq.full_name == Pet.name)

    SELECT pets.name, pets.age FROM pets
    JOIN
        (SELECT humans.id, humans.full_name FROM humans) AS anon_27
        ON anon_27.full_name = pets.name;


<a id="query.Query.filter"></a>

#### filter

```python
def filter(*exprs: Any) -> Query
```

Exerts a series of valid comparison expressions as filtering criteria to the current instance.

E.g.::

    session.query(User, email_address, last_visited)
        .filter(User.first_name == "Nima", User.age > 28)
        .first()

Any number of criteria may be specified as separated by a comma.

.. seealso::

    :meth:`.query.Query.filter_by` - filter on keyword arguments as criteria.

<a id="query.Query.filter_by"></a>

#### filter\_by

```python
def filter_by(**kwcrts: Any) -> Query
```

Exerts a series of keyword arguments as filtering criteria to the current instance.

E.g.::

    session.query(Employee, full_name, salary, tenure)
        .filter_by(department="Information Technologies", status="active")
        .all()

Any number of criteria may be specified as separated by a comma.

.. seealso::

    :meth:`.query.Query.filter` - filter on valid comparison expressions as criteria.

<a id="query.Query.group_by"></a>

#### group\_by

```python
def group_by(*columns: BaseColumnRef) -> Query
```

Adds SQL `GROUP BY` constraint on the current query with the given columns.

<a id="query.Query.having"></a>

#### having

```python
def having(expr: Any) -> Query
```

Adds SQL `HAVING` constraint on the current query with the given direct Python expression.

<a id="query.Query.order_by"></a>

#### order\_by

```python
def order_by(*columns: BaseColumnRef) -> Query
```

Adds SQL `ORDER BY` constraint on the current query with the given columns.

<a id="query.Query.limit"></a>

#### limit

```python
def limit(value: int) -> Query
```

Adds SQL `LIMIT` constraint on the current query with the given limit value.

<a id="query.Query.offset"></a>

#### offset

```python
def offset(value: int) -> Query
```

Adds SQL `OFFSET` constraint on the current query with the given offset value.

<a id="query.Query.slice"></a>

#### slice

```python
def slice(start: int, stop: int) -> Query
```

Adds slice dampers on the current query, i.e. `start` and `stop`.

<a id="query.Query.desc"></a>

#### desc

```python
def desc() -> Query
```

Adds SQL `DESC` constraint to the current query. Raises an exception if the query is not ordered.

<a id="query.Query.distinct"></a>

#### distinct

```python
def distinct() -> Query
```

Adds SQL `DISTINCT` constraint to the current query.

<a id="query.Query.subquery"></a>

#### subquery

```python
def subquery() -> Subquery
```

Gets a subquery whose inner SQL is that of the current query with the selected column names.

<a id="query.Query.get"></a>

#### get

```python
def get(**kwargs: Any) -> Optional[Record]
```

Gets the result by given criteria, e.g. by primary key. Raises an exception if more than one result is
found.

<a id="query.Query.all"></a>

#### all

```python
def all() -> QuerySet
```

Gets all results.

<a id="query.Query.first"></a>

#### first

```python
def first() -> Optional[Record]
```

Gets the first result.

<a id="query.Query.one_or_none"></a>

#### one\_or\_none

```python
def one_or_none() -> Optional[Record]
```

Gets the result or nothing if does not exist. Raises an exception if more than one result is found.

<a id="query.Query.exists"></a>

#### exists

```python
def exists() -> bool
```

Whether or not there are any results.

<a id="query.Query.count"></a>

#### count

```python
def count() -> int
```

Gets the number of rows in the current queryset.

<a id="query.Query.update"></a>

#### update

```python
def update(**fields_values) -> None
```

Two ways of updates:

    1. user = session.query(User).filter(User.username == "nbavari").first()
    user.age += 1

    2. session.query(User).filter(User.username == "nbavari").update(**field_values)
You have to put `session.save()` after both to persist it.

<a id="query.Query.delete"></a>

#### delete

```python
def delete() -> None
```

Example usage:

    session.query(User).filter(User.username == "nbavari").delete()
    session.save()
This will delete the user with the username "nbavari".

<a id="db_session"></a>

# db\_session

Contains :class:`.db_session.DBSession` and its helpers.

<a id="db_session.TransactionManager"></a>

## TransactionManager Objects

```python
class TransactionManager()
```

Used within repository pattern in :class:`.db_session.DBSession` to manage transactions.

**Arguments**:

- `engine`: DB engine that the transaction manager uses.

<a id="db_session.TransactionManager.commit"></a>

#### commit

```python
def commit() -> None
```

Commits the current transaction.

<a id="db_session.TransactionManager.rollback"></a>

#### rollback

```python
def rollback() -> None
```

Rolls back the current transaction.

<a id="db_session.TransactionManager.close"></a>

#### close

```python
def close() -> None
```

Closes the connection.

<a id="db_session.PersistenceManager"></a>

## PersistenceManager Objects

```python
class PersistenceManager()
```

Used within repository pattern in :class:`.db_session.DBSession` to manage persistence.

**Arguments**:

- `engine`: DB engine that the persistence manager uses.

<a id="db_session.PersistenceManager.add"></a>

#### add

```python
def add(obj: Model) -> None
```

Adds an object to the queue for persistence.

<a id="db_session.PersistenceManager.auto_commit_adds"></a>

#### auto\_commit\_adds

```python
def auto_commit_adds() -> None
```

Persists all added objects.

<a id="db_session.QueryExecutor"></a>

## QueryExecutor Objects

```python
class QueryExecutor()
```

Used within repository pattern in :class:`.db_session.DBSession` to execute queries.

**Arguments**:

- `engine`: DB engine that the query executor uses.

<a id="db_session.QueryExecutor.query"></a>

#### query

```python
def query(*fields: QueryEntity) -> Query
```

Starts a query and returns the query object.

<a id="db_session.QueryExecutor.execute_queries"></a>

#### execute\_queries

```python
def execute_queries() -> None
```

Executes accumulated queries.

<a id="db_session.SQLTypeResolver"></a>

## SQLTypeResolver Objects

```python
class SQLTypeResolver()
```

Used within repository pattern in :class:`.db_session.DBSession` to resolve native SQL types in the dialect

that the given DB engine uses.

**Arguments**:

- `engine`: DB engine that the type resolver uses.

<a id="db_session.SQLTypeResolver.get_native_type_name"></a>

#### get\_native\_type\_name

```python
def get_native_type_name(type_name: str) -> str
```

Resolves the native SQL type for the given type name.

<a id="db_session.DBSession"></a>

## DBSession Objects

```python
class DBSession()
```

A singleton DB session class.

This class implements a singleton DB session to be used to access the database.

Implements a context manager for a more secure session. The following is an idiomatic usage::

    eng = DBEngine("postgresql://user:secret@localhost:5432/my_db")
    with DBSession(eng) as session:
        pass  # do something with session

**Arguments**:

- `engine`: DB engine that the session uses.

<a id="db_session.DBSession.query"></a>

#### query

```python
def query(*fields: QueryEntity) -> Query
```

Starts a query and returns the query object.

<a id="db_session.DBSession.add"></a>

#### add

```python
def add(obj: Model) -> None
```

Adds a new record to the DB session.

<a id="db_session.DBSession.save"></a>

#### save

```python
def save() -> None
```

Persists all started queries.

<a id="model"></a>

# model

Contains :class:`.model.Model` and its helpers.

<a id="model.SchemaDefinition"></a>

## SchemaDefinition Objects

```python
class SchemaDefinition()
```

SQL schema definition for a user defined model.

<a id="model.SchemaDefinition.generate_sql"></a>

#### generate\_sql

```python
def generate_sql() -> str
```

Generates SQL for creating the associated table.

<a id="model.Model"></a>

## Model Objects

```python
class Model()
```

Abstract representer of the database model in Python.

This class provides the base for defining the structure and behavior of data objects that will be stored in a
database. The :class:`.model.Model` class can be inherited and used to create custom models with fields, methods,
and attributes. It supports relationships between different models, enabling data retrieval and manipulation across
tables.

<a id="model.Model.label"></a>

#### label

```python
@classmethod
def label(cls, alias: str) -> Type
```

Returns the ORM representation for SQL table aliasing.

<a id="model.Model.sql"></a>

#### sql

```python
@property
def sql() -> str
```

SQL statement for new object creation.

<a id="__init__"></a>

# \_\_init\_\_

<a id="db_engine"></a>

# db\_engine

Contains abstract and concrete database engine classes, as well as the dialect inferrer class.

<a id="db_engine.DialectInferrer"></a>

## DialectInferrer Objects

```python
class DialectInferrer()
```

Delegatee class concerning with encapsulation of the sql dialect inferrence functionality.

**Arguments**:

- `conn_str`: The database connection string used to infer the SQL dialect.

<a id="db_engine.DialectInferrer.sql_dialect"></a>

#### sql\_dialect

```python
@property
def sql_dialect() -> str
```

Infers the SQL dialect from the connection string.

<a id="db_engine.AbstractEngine"></a>

## AbstractEngine Objects

```python
class AbstractEngine()
```

Abstract database engine class.

<a id="db_engine.DBEngine"></a>

## DBEngine Objects

```python
class DBEngine(AbstractEngine)
```

Connection adapter for the :class:`.db_session.DBSession` object.

Downstream from a thread-safe connection pool. This connection pool uses lazy loading.

The class keeps record of the most recent active instance as an inner state.

**Arguments**:

- `conn_str`: database location, along with auth params
- `pool_size`: keyword-only. Size of the connection pool.

<a id="db_engine.DBEngine.get_connection"></a>

#### get\_connection

```python
def get_connection() -> pyodbc.Connection
```

Gets a connection from the pool.

<a id="db_engine.DBEngine.release_connection"></a>

#### release\_connection

```python
def release_connection(conn: pyodbc.Connection) -> None
```

Releases a connection back to the pool.

<a id="backends"></a>

# backends

Contains basic datatypes.

<a id="backends.Serial"></a>

## Serial Objects

```python
class Serial(Integer)
```

ORM representation of serial types in SQL variants. Inherits from :class:`.backends.Integer`.


<a id="backends.oracle"></a>

# backends.oracle

Contains datatypes to support Oracle DB backend.

<a id="backends.postgresql"></a>

# backends.postgresql

Contains datatypes to support PostgreSQL backend.

<a id="backends.mysql"></a>

# backends.mysql

Contains datatypes to support MySQL backend.

<a id="backends.sql_server"></a>

# backends.sql\_server

Contains datatypes to support SQL Server backend.

