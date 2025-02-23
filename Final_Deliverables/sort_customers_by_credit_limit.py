'''
Anthony Ung, Cory Lillis
ORM Project
Aggregate

In addition to the functionality discussed in class, 
    we demonstrate aggregation in Python's ORM.

Our business would want to know which customers 
    are making the biggest.
'''

# Necessary import statements
import sqlalchemy as alch
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from mysql.connector.errors import IntegrityError

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
Base = automap_base()
Base.prepare(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Grabbing tables
Base = automap_base()

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