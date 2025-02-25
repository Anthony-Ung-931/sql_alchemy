'''
Anthony Ung, Cory Lillis
ORM Project
Customer Interactions Per Employee

This query returns the number of customers an employee interacts with
    and who they report to.

Prints out the job titles to help explain why some employees interact with 0 customers.
'''

# Necessary import statements
import sqlalchemy as alch
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, Text,
ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint)


# A helpful debug method 
def DEBUG_PRINT(message):
    print(message)
    yes = input('\n' 'Enter any string to exit.' '\n')


class globals:
    engine = None
    Base = None
    session = None


def init_connection():
    # Checks for the connect script being in the same directory.
    # Separate becasue I do not want bots and scrapers to grab my login credentials from Github.
    try:
        import connect
    except:
        DEBUG_PRINT('Error!\n'\
                'You do not have the appropriate\n'\
                'connect.py file in the right directory\n')

    # Prepare the engine and session
    globals.engine = connect.connect()
    Session = sessionmaker(bind=globals.engine)
    globals.session = Session()

def query():
    session = globals.session

    Base = alch.orm.declarative_base()

    class Customer(Base):
        __tablename__ = 'customers'

        customerNumber = Column(Integer, primary_key=True)
        salesRepEmployeeNumber = Column(Integer)
        

    class Employee(Base):
        __tablename__ = 'employees'

        employeeNumber = Column(Integer, primary_key=True)
        lastName = Column(String(50), nullable=False)
        firstName = Column(String(50), nullable=False)
        reportsTo = Column(Integer, nullable=True)
        jobTitle = Column(String(50), nullable=False)

    manager = alch.orm.aliased(Employee)

    #execute query and print results to screen
    try:
        query = session.query(\
                Employee.lastName, \
                Employee.firstName, \
                Employee.jobTitle, \
                alch.func.coalesce(alch.func.count(Customer.salesRepEmployeeNumber), 0).label('Number of Employees'), \
                manager.lastName, \
                manager.firstName) \
            .join(Customer, Customer.salesRepEmployeeNumber == Employee.employeeNumber, isouter = True)\
            .outerjoin(manager, Employee.reportsTo == manager.employeeNumber)\
            .group_by(Employee.employeeNumber)\
            .order_by(alch.desc('Number of Employees'))

        results = query.all()
        for row in results:
            print(row)

        print(f"{query.count()} rows returned")

    except Exception as Error:
        print(Error)


def close_connection():
    session = globals.session
    engine = globals.engine

    # prompt user to close then close session and engine
    yes = input("Press any key to close")

    #cleanup
    session.close()
    engine.dispose()

def run():
    init_connection()
    query()
    close_connection()

run()