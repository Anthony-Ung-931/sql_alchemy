# invoke functions we need
from login_creds_au import LoginCreds

import sqlalchemy
import mysql.connector
import getpass

# assemble variables for create_engine connection, use input variables when running at command prompt
servername = LoginCreds.servername
database   = LoginCreds.database
port       = None
username   = LoginCreds.username
password   = LoginCreds.password
#password = 'your mysql password'


# create database connection
engine = sqlalchemy.create_engine(sqlalchemy.URL.create('mysql+mysqlconnector', username, password, servername, port, database))
conn   = engine.connect()

# execute query to check connection
query  = sqlalchemy.text('select title, release_year from sakila.film limit 10')
cr     = conn.execute(query)
for row in cr:
        year=row[0]
        print(year)
yes = input("ready to close")

#close and dispose
conn.close()
engine.dispose()