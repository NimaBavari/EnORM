# EnORM

EnORM - EnDATA Object Relational Mapper.
Get ready for an EnORMous database experience!

## Usage

```python
from EnORM import DBSession, Model, Column, ForeignKey, Integer, String


class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    salary = Column(Float)
    role = Column(String(20), default='entry')
    company = ForeignKey()


class Company(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

with DBSession('postgresql://user:secret@localhost:5432/my_db') as session:
    new_employee = Employee(full_name='Nima Bavari Goudarzi', salary=64320.00, role='Senior', company=the_company)
    session.save(new_employee)
    
    session.query(Person, )
```