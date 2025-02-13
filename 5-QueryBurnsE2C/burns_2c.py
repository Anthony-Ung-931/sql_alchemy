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
    
    Order = Base.classes.orders
    OrderDetail = Base.classes.orderdetails
    Customer = Base.classes.customers
    Product = Base.classes.products
    ProductLine = Base.classes.productlines
    Employee = Base.classes.employees
    
    query = session.execute(alch.select(\
                Order.orderNumber,\
                Order.orderDate,\
                Customer.customerNumber,
                Customer.customerName,
                Product.productCode,
                Product.productName,\
                ProductLine.productLine,\
                Employee.lastName)\
            .join(Customer, Order.customerNumber == Customer.customerNumber)\
            .join(OrderDetail, Order.orderNumber == OrderDetail.orderNumber)\
            .join(Product, OrderDetail.productCode == Product.productCode)\
            .join(ProductLine, Product.productLine == ProductLine.productLine)\
            .join(Employee, Customer.salesRepEmployeeNumber == Employee.employeeNumber)\
        .order_by(Order.orderNumber))
    
    results = query.all()
    for row in results:
        print(row)

    print(f"{query.rowcount} rows returned")
    
    # prompt user ready to close then close session and engine
    yes = input("ready to close")
    session.close()
    engine.dispose()

   
try:
	run()
except Exception as Error:
	print(Error)
	hang()