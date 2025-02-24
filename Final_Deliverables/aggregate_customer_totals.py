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
Order = Base.classes.orders
OrderDetail = Base.classes.orderdetails
Customer = Base.classes.customers
Product = Base.classes.products
ProductLine = Base.classes.productlines
Employee = Base.classes.employees


try:
    stmt = alch.select(Customer.customerName, \
                            alch.func.sum(OrderDetail.quantityOrdered * OrderDetail.priceEach).label('Total Purchases'))\
                    .join(Order, Customer.customerNumber == Order.customerNumber)\
                    .join(OrderDetail, Order.orderNumber == OrderDetail.orderNumber)\
                    .group_by(Customer.customerNumber)\
                    .order_by(alch.desc('Total Purchases'))\
                    .limit(10)
    for row in session.execute(stmt):
        print(row)
except SQLAlchemyError as e:
    print(f"Transaction rolled back due to error: {e}")



# prompt user to close then close session and engine
yes = input("Press any key to close")

#cleanup
session.close()
engine.dispose()