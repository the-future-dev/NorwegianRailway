import os
import re
import sqlite3

db_path = 'railway.db'

def create_tables(file_path='dbDefinition.sql'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(file_path, 'r') as f:
        sql_script = f.read()

    c.executescript(sql_script)

    conn.commit()
    conn.close()

def insert_tables(file_path='dbInsertion.sql'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(file_path, 'r') as f:
        sql_script = f.read()

    c.executescript(sql_script)
    conn.commit()
    
    #Insertion of the Seats
    for carID in range(3, 7):
        for seatNo in range(1, 13):
            c.execute("""INSERT INTO Seat (carID, seatNo) SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Seat WHERE carID = ? AND seatNo = ?);""", (carID, seatNo, carID, seatNo))
    conn.commit()
    conn.close()

def get_train_routes():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    station_name = input('Insert the station name (ex. Trondheim): ')
    weekday = input('Insert the day (ex. Monday): ')
    query = """
        SELECT TR.routeID, tr.operator, tr.direction, tr.trackName
        FROM TrainRoute AS TR INNER JOIN TrackSection AS TS
            ON TR.trackName = TS.name
        WHERE EXISTS (
            SELECT Passes.stationName, Passes. cardinalNo
            FROM Passes INNER JOIN TrackSection ON (TrackSection.name = Passes.name)
            WHERE TS.name = TrackSection.name  
                AND ((Passes.cardinalNo <= TR.endStationCardinalNo AND Passes.cardinalNo >= TR.startStationCardinalNo AND TR.direction = 0)
                    OR
                    (Passes.cardinalNo <= TR.startStationCardinalNo AND Passes.cardinalNo >= TR.endStationCardinalNo  AND TR.direction = 1))
                AND Passes.stationName = ?
        ) AND EXISTS (
            SELECT *
            FROM TrainRoute INNER JOIN StartFromStationInDay ON (TrainRoute.routeID = StartFromStationInDay.routeID)
            WHERE TrainRoute.routeID = TR.routeID AND StartFromStationInDay.dayOfTheWeek = ?
        );
    """
    c.execute(query, (station_name, weekday))
    result = c.fetchall()
    for row in result:
        print(f'\n> Track Name: {row[3]} Route ID: {row[0]} Operator: {row[1]} Direction: {row[2]} \n')
    conn.close()

def register_customer():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #user input validation 
    name = input('> Enter your name: ')
    while True:
        email = input('> Enter your email: ')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        print("! Invalid email format. Please try again.")
    
    while True:
        phone = input('> Enter your phone number: ')
        if re.match(r"^\d{8}$", phone):
            break
        print("! Invalid phone number. Please enter a valid 8-digit phone number.")

    phone = input('> Enter your phone number: ')

    #Insertion of the new user, just if it doesn't exist already
    c.execute("SELECT * FROM Customer WHERE name=? AND email=? AND phone=?", (name, email, int(phone)))
    if c.fetchone() is None:
        c.execute("INSERT INTO Customer (name, email, phone) VALUES (?, ?, ?)", (name, email, int(phone)))
        print('Registration successful!')
        conn.commit()        
    else:
        print('User already exists!')
    
    conn.close()

def main(fileExists):
    if not fileExists: 
        create_tables()
        insert_tables()
    print('Welcome to NorwegianRailways!')
    funcUser = '' 
    while funcUser != '0':
        funcUser = input('MENU: \n [1] Get all train routes that stop at a particular station on a given weekday \n [2] Signup as a new customer \n [0] Exit \n > ')
        if funcUser == '1':
            get_train_routes()
        elif funcUser == '2':
            register_customer()

#Connect to the db
fileExists = True
if not os.path.exists(db_path):
    fileExists = False

main(fileExists)

