'''
Anthony Ung, Cory Lillis
ORM Project
Insert and Update

Demonstrates inserting and then updating records.
In addition to inserting and updating records, we have found ways to
    catch excptions in Python and to commit/rollback transactions.
'''

# Necessary import statements
import sqlalchemy as alch
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError

# A helpful debug method 
def DEBUG_PRINT(message):
    print(message)
    yes = input('\n' 'Enter any string to exit.' '\n')

'''
    The code examples have straight-line code with no helper functions.
    We would not ship straight-line code with no helper functions to a real client
        because that is very hard to read.
    Helper functions that lack code comments 
        imply that the functions do exactly what their names imply.
'''
class globals:
    engine = None
    Base = None
    session = None
    Employee = None


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

    # Get the class to table mapping
    globals.Employee = globals.Base.classes.employees


'''
I delete myself from the table so I can insert myself again.
'''
def delete_record():
    Employee = globals.Employee
    session = globals.session

    try:
        print('Deleting Employee so I can insert him again.' '\n')
        employee = session.query(Employee).filter(Employee.employeeNumber == 1950).first()
        session.delete(employee)
        session.commit()
    except SQLAlchemyError as e:
        print('Target employee does not exist.')

    
'''
I inserted myself into the table.
reportsTo is NULLable because the President does not report to anybody.
In addition to the parts of SQLAlchemy that were discussed in class,
	Cory implemented rollback for when an error is raised.
'''
def insert_record():
    session = globals.session
    Employee = globals.Employee

    try:
        add_employee = Employee( \
                            employeeNumber = 1950, \
                            lastName = 'Ung', \
                            firstName = 'Anthony', \
                            extension = 'x1950', \
                            email = 'ungant67@students.rowan.edu', \
                            officeCode = 4, \
                            reportsTo = None, \
                            jobTitle = 'Evaluation Assistant' \
                        )
        session.add(add_employee)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")
        print(f"\n" "This block would be reached if the insertion was already completed." "\n\n")

    '''
        Unfortunately, there is no equivalent to SELECT *
            so I have to unwrap all the fields.
    '''
    try:
        employee = session.query(Employee.employeeNumber, \
                                Employee.lastName, \
                                Employee.firstName, \
                                Employee.extension, \
                                Employee.email, \
                                Employee.officeCode, \
                                Employee.reportsTo, \
                                Employee.jobTitle \
                                ).filter(Employee.employeeNumber == 1950).first()
        
        print('Employee after insertion')
        print(employee)
    except SQLAlchemyError as e:
        print(e)


def update_record():
    session = globals.session
    Employee = globals.Employee

    try:
        users = session.query(Employee).filter(Employee.lastName == 'Ung').filter(Employee.firstName == 'Anthony')
        users.update({Employee.jobTitle: 'Research Assistant'})
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")
        print(f"\n" "Rollback is not supposed to happen in this case." "\n\n")

    try:
        print('\n' 'Updated employee record after my job got eliminated:')
        employee = session.query(Employee.employeeNumber, \
                                    Employee.lastName, \
                                    Employee.firstName, \
                                    Employee.extension, \
                                    Employee.email, \
                                    Employee.officeCode, \
                                    Employee.reportsTo, \
                                    Employee.jobTitle \
                                    ).filter(Employee.employeeNumber == 1950).first()
        print(employee)
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")
        print(f"\n" "Rollback is not supposed to happen in this case." "\n\n")


def close_connection():
    engine = globals.engine
    session = globals.session

    yes = input('\n' "Press any key to close")

    #cleanup
    session.close()
    engine.dispose()


def run():
    init_connection()
    delete_record()
    insert_record()
    update_record()
    close_connection()


run()