# EnORM

![PyPI Version](https://img.shields.io/pypi/v/enorm)
[![PyPI Downloads](https://static.pepy.tech/badge/enorm)](https://pepy.tech/projects/enorm)
![License](https://img.shields.io/github/license/NimaBavari/EnORM)
![Dependencies](https://img.shields.io/librariesio/release/pypi/enorm)
![GitHub Stars](https://img.shields.io/github/stars/NimaBavari/EnORM)

EnORM---EnDATA Object Relational Mapper.

## Features

- **Model Definition:**
    - Define database tables using Python classes.
    - Support for primary keys, foreign keys, constraints, and default values.
- **Type System:**
    - Use Python-native types for columns with support for custom SQL-compatible types.
    - Full support for PostgreSQL, MySQL, SQLite, Oracle, and SQL Server backends with in-house types.
- **Query Building:**
    - Pythonic API for constructing queries.
    - Filtering, joining, grouping, ordering, and aggregation.
    - Ability to use Python expressions directly in queries.
- **Subquerying:**
    - Full support for subqueries as nested or derived tables.
    - Essential for advanced query composition and reusable query fragments.
- **Relationships:**
    - Define one-to-many and many-to-many relationships.
    - Cascading updates and deletes for referential integrity.
- **Transactions:**
    - Transaction management with commit and rollback control.
- **Database Session:**
    - Manage database interactions with a session.
    - Context manager support for secure and efficient operations.
- **Connection Pooling:**
    - Thread-safe connection management with pooling for performance.
- **Schema Management:**
    - Automatic SQL generation for table creation.
- **Custom Functions and Aggregates:**
    - Built-in support for SQL functions and aggregates, extensible for complex operations.
- **Data Validation:**
    - Automatic enforcement of field types and constraints during record creation and updates.
- **Custom Exceptions:**
    - Comprehensive exceptions for debugging and error reporting.

## Installation

EnORM is a PyPI-indexed library. You can install it by running:

```sh
pip install EnORM
```

EnORM supports Python 3.10+.

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


eng = DBEngine("postgresql://user:secret@localhost:5432/my_db", pool_size=64)
with DBSession(eng) as session:
    the_company = session.query(Company).filter(Company.country == "United Kingdom").first()

    new_employee = Employee(full_name="Nima Bavari Goudarzi", salary=64320.00, role="engineer", company_id=the_company.id)
    session.add(new_employee)
    
    sharks = session.query(Employee, Employee.full_name, Employee.company_id).filter(Employee.salary > 90000.00).all()
```

## Documentation

See full [documentation](docs/api_docs.md).

## Dev Scripts

### Set Up Dev Environment

Run:

``` sh
make set_dev_env
```

to set up the dev environment.

This sets:
- git pre-commit hook

If you intend to touch the code, set up dev environment first.

### Linting and Formatting

Run:

``` sh
make cleanup
```

to run linting, formatting, typechecking, and automatically updating the documentation.

### Testing

Run:

``` sh
make test
```

to start the tests.
