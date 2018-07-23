"""EnORM - EnDATA Object Relational Mapper.
Get ready for an EnORMous database experience!

Example usage:

from EnORM import Column, DBConnection, Table


c1 = Column(
    col_name='ID',
    vartype='integer',
    max_l=None,
    default=None,
    null=False,
    unique=True,
    p_key=True,
    autoinc=True
)

c2 = Column(
    col_name='fname',
    vartype='varchar',
    max_l=20
)

c3 = Column(
    col_name='lname',
    vartype='varchar',
    max_l=20
)

c4 = Column('age', 'integer')

users_table = Table('users', c1, c2, c3, c4)

with DBConnection('operations.db') as db:
    db.create_table(users_table)
    db.insert('users', ['Nima', 'Bavari', 27], ['fname', 'lname', 'age'])
    db.insert('users', ['Omid', 'Armagar', 32], ['fname', 'lname', 'age'])
    db.update('users', ['age'], [35], ['fname'], ['Omid'])
    db.get_all('users', ['fname', 'lname'], ['age'], [35],
               order_by=[{'name': 'lname', 'desc': False}])
"""

from EnORM.column import Column
from EnORM.database import DBConnection
from EnORM.table import Table
