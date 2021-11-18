# EnORM

EnORM - EnDATA Object Relational Mapper.
Get ready for an EnORMous database experience!

## Example Usage

```python
from EnORM import DBSession, Column, ForeignKey, Float, Integer, Model, Serial, String


class Employee(Model):
    id = Column(Serial, primary_key=True)
    full_name = Column(String, 100, nullable=False)
    salary = Column(Float)
    age = Column(Integer)
    role = Column(String, 20, default='entry')
    company = Column(Serial, ForeignKey(Company, reverse_name='employees', on_delete=CASCADE))


class Company(Model):
    id = Column(Serial, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, 40)

with DBSession('postgresql://user:secret@localhost:5432/my_db') as session:
    the_company = session.query(Company).filter(country == 'United Kingdom').first()

    new_employee = Employee(full_name='Nima Bavari Goudarzi', salary=64320.00, role='engineer', company=the_company)
    session.save(new_employee)
    
    sharks = session.query(Employee, 'full_name', 'company_id').filter(salary > 90000.00).all()
```