'''
Anthony Ung, Cory Lillis
Python Connect

This script provides the application to interface with the database.
'''

import sys

def DEBUG_PRINT(message):
    print(message)
    
    yes = input('\n' 'Enter any string to exit.' '\n')


try:
    import connect
except:
    DEBUG_PRINT('Error!\n'\
               'You do not have the appropriate\n'\
               'connect.py file in the right directory\n')


def run():
    '''
    Pseudocode
    
    1. Establish Database Connection
    
    Repeat until User Exits
        Display a list of menu options
        Take input from User
        Validate Input is of appropriate type
        Run the query indicated by the menu options
        Display the results (or generate the visualization files)
        
    Print a nice goodbye message
    '''
    DEBUG_PRINT('Hello World!')


run()