'''
Anthony Ung, Cory Lillis
ORM Project
Sort Customers By Credit Limit

This query sorts customers by credit limit.
This could be valuable to a business in order to inform marketing decisions.
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

# Checks for the connect script being in the same directory.
# Separate becasue I do not want bots and scrapers to grab my login credentials from Github.
try:
    import connect
except:
    DEBUG_PRINT('Error!\n'\
               'You do not have the appropriate\n'\
               'connect.py file in the right directory\n')

# Prepare the engine and session
engine = Engine = connect.connect()
Session = sessionmaker(bind=engine)
session = Session()

'''
Grabbing tables
I need the {'extend_existing': True} option so I do not get errors
    because this metadata instance is already defined.
https://stackoverflow.com/questions/37908767/table-roles-users-is-already-defined-for-this-metadata-instance
'''
Base = alch.orm.declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customerNumber = Column(Integer, primary_key=True)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    creditLimit = Column(Numeric(10, 2))


#execute query and print results to screen
try:
    query = session.query(\
            Customer.customerNumber, \
            Customer.contactLastName, \
            Customer.contactFirstName, \
            Customer.phone,\
            Customer.creditLimit)\
        .order_by(Customer.creditLimit.desc())

    results = query.all()
    for row in results:
        print(row)

    print(f"{query.count()} rows returned")

except Exception as Error:
    print(Error)


# prompt user to close then close session and engine
yes = input("Press any key to close")

#cleanup
session.close()
engine.dispose()