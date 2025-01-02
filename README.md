# EnORM

EnORM---EnDATA Object Relational Mapper.

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

## Documentation

See full [documentation](docs/api_docs.md).
