import re
import sqlite3
from datetime import datetime
from rich.console import Console

console = Console()

##############################################################################################################
## User Story: e
## The user should be able to register in the customer registry.
##############################################################################################################
def register_customer(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #user input validation 
    name = input('> Enter your name: ')
    while True:
        email = input('> Enter your email: ')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        console.print("! Invalid email format. Please try again.", style= 'red')
    
    while True:
        phone = input('> Enter your phone number: ')
        if re.match(r"^\d{8}$", phone):
            break
        console.print("! Invalid phone number. Please enter a valid 8-digit phone number.", style='red')
    #Insertion of the new user, just if it doesn't exist already
    c.execute("SELECT * FROM Customer WHERE name=? AND email=? AND phone=?", (name, email, int(phone)))
    if c.fetchone() is None:
        c.execute("INSERT INTO Customer (name, email, phone) VALUES (?, ?, ?)", (name, email, int(phone)))
        console.print("! Registration successful", style='green')
        conn.commit()        
    else:
        
        console.print("! User already exists", style='red')

    conn.close()

##############################################################################################################
## User Story: g
## The user should be able to register in the customer registry.
## Registered customers should be able to find available tickets for a desired train route and
## purchase the tickets they would like.
## ! Only sell available seats.
##############################################################################################################
def new_order(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print('You can buy tickets for the three main routes:')
    
    name = input('Enter your name: ')
    email = input('Enter your email: ')
    phone = int(input('Enter your phone number: '))

    # Check if the user exists
    query = "SELECT customerID FROM Customer WHERE name=? AND email=? AND phone=?"
    c.execute(query, (name, email, phone))
    result = c.fetchone()
    
    if not result:
        console.print(f'\nNo matching customer found.', style='red')
    else:
        customerID = result[0]
        now = datetime.now()
        purchaseDate = now.strftime('%Y-%m-%d')
        purchaseTime = now.strftime('%H:%M:%S')

        #New CustomerOrder
        query = "INSERT INTO CustomerOrder (purchaseTime, purchaseDate, customerID) VALUES (?, ?, ?)"
        c.execute(query, (purchaseTime, purchaseDate, customerID))
        conn.commit()

        #TO comment
        console.print(f'\nLogged In !', style='green')
            
    
    conn.close()
