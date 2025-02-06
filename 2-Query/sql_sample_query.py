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
database   = 'sakila'
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

class Film(Base):
        __tablename__ = 'film'
        film_id = Column(SMALLINT, primary_key=True)
        title = Column(String(255), nullable=False, index=True)
        description = Column(Text()) 

#execute query and print results to screen
try:
    print(session.query(Film.film_id, Film.title, Film.description).first())
except Exception as Error:
    print(Error)


# prompt user ready to close then close session and engine
yes = input("ready to close")
session.close()
engine.dispose()
