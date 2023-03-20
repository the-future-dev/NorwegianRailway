import os

from code.init          import create_tables, insert_tables                     #Opgave  A, B, F
from code.routeSearch   import get_train_routes, findRoutesDateTime             #Oppgave C, D
from code.customer      import register_customer, new_order, get_orders         #Oppgave E, G

db_path = 'database/railway.db'

def main(fileExists):
    if not fileExists: 
        create_tables(db_path)
        insert_tables(db_path)
    print('\nWelcome to Norwegian Railways!')
    funcUser = '' 
    while funcUser != '0':
        funcUser = input('\n MENU: \n [1] Get all train routes that stop at a particular station on a given weekday \n [2] Search Routes \n [3] Signup \n [4] Buy Tickets \n [5] Retrieve orders\n [0] Exit \n > ')
        if funcUser == '1':
            get_train_routes(db_path)
        elif funcUser == '2':
            findRoutesDateTime(db_path)
        elif funcUser == '3':
            register_customer(db_path)
        elif funcUser == '4':
            new_order(db_path)
        elif funcUser == '5':
            get_orders(db_path)
fileExists = True
if not os.path.exists(db_path):
    fileExists = False

main(fileExists)