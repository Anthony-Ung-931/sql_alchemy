# invoke functions we need
from login_creds_au import LoginCreds

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, Text,
ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint)
from sqlalchemy.dialects.mysql import YEAR, SMALLINT, TINYINT, SET, TIMESTAMP
from sqlalchemy.orm import declarative_base 
from sqlalchemy.orm import relationship, backref

# assemble variables for create_engine connection, use input variables when running at command prompt
servername = LoginCreds.servername
database   = 'ungant67'
port       = None
username   = LoginCreds.username
password   = LoginCreds.password

def hang():
    print('Hang called')
    while True:
        continue


# establish connection engine to connect to db and establish session
engine = sqlalchemy.create_engine(sqlalchemy.URL.create('mysql+mysqlconnector', username, password, servername, port, database))
Session = sessionmaker(bind=engine)
session = Session()


#define classes
Base    = declarative_base()

try:
    class Customer(Base):
        __tablename__ = 'customers'
        customerNumber = Column(Integer, primary_key=True)
        contactLastName = Column(String(50), nullable=False)
        contactFirstName = Column(String(50), nullable=False)
        phone = Column(String(50), nullable=False)
        creditLimit = Column(Numeric(10, 2))
except Exception as Error:
    print(Error)
    hang()


#execute query and print results to screen
try:
    query = session.query(\
            Customer.customerNumber, \
            Customer.contactLastName, \
            Customer.contactFirstName, \
            Customer.phone,\
            Customer.creditLimit)\
        .order_by(Customer.creditLimit)

    results = query.all()
    for row in results:
        print(row)

    print(f"{query.count()} rows returned")

except Exception as Error:
    print(Error)
    hang()


# prompt user ready to close then close session and engine
yes = input("ready to close")
session.close()
engine.dispose()
