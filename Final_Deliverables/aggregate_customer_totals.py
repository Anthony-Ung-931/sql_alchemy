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


class globals:
    engine = None
    Base = None
    session = None


class tables:
    Order = None
    OrderDetail = None
    Customer = None


def init_connection():
    try:
        import connect
    except:
        DEBUG_PRINT('Error!\n'\
                'You do not have the appropriate\n'\
                'connect.py file in the right directory\n')

    # Prepare the engine and session
    globals.engine = connect.connect()
    globals.Base = automap_base()
    globals.Base.prepare(globals.engine)
    Session = sessionmaker(bind=globals.engine)
    globals.session = Session()


def init_tables():
    Base = globals.Base

    # Grabbing tables
    tables.Order = Base.classes.orders
    tables.OrderDetail = Base.classes.orderdetails
    tables.Customer = Base.classes.customers


def query():
    session = globals.session

    Order = tables.Order
    OrderDetail = tables.OrderDetail
    Customer = tables.Customer

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


def close_connection():
    session = globals.session
    engine = globals.engine

    # prompt user to close then close session and engine
    yes = input("Press any key to close" "\n")

    #cleanup
    session.close()
    engine.dispose()


def run():
    init_connection()
    init_tables()
    query()
    close_connection()


run()