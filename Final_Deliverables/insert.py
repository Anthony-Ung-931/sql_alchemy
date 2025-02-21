'''
Anthony Ung, Cory Lillis
ORM Project
Insert and Update

Demonstrates inserting and then updating records.
In addition to inserting and updating records, we have found ways to
    catch excptions in Python and to commit/rollback transactions.
'''

import sqlalchemy as a
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from mysql.connector.errors import IntegrityError


def DEBUG_PRINT(message):
    print(message)
    yes = input('\n' 'Enter any string to exit.' '\n')


try:
    import connect
except:
    DEBUG_PRINT('Error!\n'\
               'You do not have the appropriate\n'\
               'connect.py file in the right directory\n')

# login
engine = Engine = connect.connect()
Base = automap_base()
Base.prepare(engine)
Session = sessionmaker(bind=engine)
session = Session()

# grabbing tables
Order = Base.classes.orders
OrderDetail = Base.classes.orderdetails
Customer = Base.classes.customers
Product = Base.classes.products
ProductLine = Base.classes.productlines
Employee = Base.classes.employees

'''
I inserted myself into the table.
reportsTo is NULLable because the President does not report to anybody.
'''
try:
    add_employee = Employee( \
                        employeeNumber = 1950, \
                        lastName = 'Ung', \
                        firstName = 'Anthony', \
                        extension = 'x1950', \
                        email = 'ungant67@students.rowan.edu', \
                        officeCode = 4, \
                        reportsTo = None, \
                        jobTitle = 'Evaluation Assistant' \
                    )
    session.add(add_employee)
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
    print(f"Transaction rolled back due to error: {e}")
    print(f"\nThis block would be reached if the insertion was already completed.\n\n")

'''
I lost my job as an Evaluation Assistant because the course instructor
    no longer has the enrollment numbers to qualify for having me.
'''
print('Updating an Employee record. This is idempotent and has been done before.\n')
users = session.query(Employee).filter(Employee.lastName == 'Ung').filter(Employee.firstName == 'Anthony')
users.update({Employee.jobTitle: 'Research Assistant'})
session.commit()

print('Updated employee record after my job got eliminated:\n')
users = session.query(Employee).filter(Employee.lastName == 'Ung').filter(Employee.firstName == 'Anthony')
for row in users.all():
    print(row.__dict__)

# prompt user to close then close session and engine
yes = input("Press any key to close")

#cleanup
session.close()
engine.dispose()