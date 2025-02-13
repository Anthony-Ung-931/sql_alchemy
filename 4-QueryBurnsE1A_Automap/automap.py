def hang():
    print('Hang called')
    while True:
        continue

def run():
    from login_creds_au import LoginCreds
    import sqlalchemy as alch
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.automap import automap_base
    
    servername = LoginCreds.servername
    database = 'ungant67'
    port = None
    username = LoginCreds.username
    password = LoginCreds.password

    engine = alch.create_engine(alch.URL.create('mysql+mysqlconnector', username, password, servername, port, database))
    Base = automap_base()
    Base.prepare(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Customer = Base.classes.customers
    
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
    
    # prompt user ready to close then close session and engine
    yes = input("ready to close")
    session.close()
    engine.dispose()

   
try:
	run()
except Exception as Error:
	print(Error)
	hang()