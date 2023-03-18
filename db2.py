import os
import re
import sqlite3
from termcolor import colored
from datetime import datetime
from rich.console import Console

from helpers import dateToWeekday, inputWithFormat, next_day

console = Console()

db_path = 'database/railway.db'

def create_tables(file_path='database/dbDefinition.sql'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(file_path, 'r') as f:
        sql_script = f.read()

    c.executescript(sql_script)

    conn.commit()
    conn.close()

def insert_tables(file_path='database/dbInsertion.sql'):
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
    
    if not result:
        console.print(f"! No Tracks were found to pass at {station_name} during {weekday}.", style='red')
    
    # row: [0] routeID | [1] operator | [2] direction | [3] trackName
    for row in result:
        timeQuery = """
                        SELECT arrivalTime, departureTime 
                        FROM Timetable
                        WHERE routeID = ? AND stationName = ?
                    """
        c.execute(timeQuery, (row[0], station_name))
        time = c.fetchone()
        if time is None:
            console.print(f"! Bad db implementation", style='red')
        else:
            if time[0] is None:
                console.print(f"\n >> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  will end its journey at {station_name} during {weekday} at {time[1]}\n", style='green')
            elif time[1] is None:
                console.print(f"\n >> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  will start its journey at {station_name} during {weekday} at {time[0]}\n", style='green')
            else:
                console.print(f"\n >> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  will be at {station_name} during {weekday} from {time[0]} to {time[1]}\n", style='green')

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

####################################################
#New Order
def new_order():
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
        
        #TO comment
        console.print(f'\nNew order created for {name} with order ID {c.lastrowid}.', style='green')
        
        conn.commit()
    
    conn.close()

def findRoutesDateTime():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print('Search for train routes going between a starting station and an ending station based on date and starting time.')

    staStation = input('Starting Station (ex. Trondheim): ')
    endStation = input('Starting Station (ex. Mo i Rana): ')
    date = inputWithFormat('Date (format YYYY-MM-DD): ', '%Y-%m-%d')
    time = inputWithFormat('Starting Time (format HH:MM): ', '%H:%M')

    dayOfTheWeek = dateToWeekday(date)
    nextDay = next_day(dayOfTheWeek)

    queryDay1 = """
                SELECT routeID, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyEndStationName, departureTime, arrivalTime, dayOfTheWeek
                FROM (
                    SELECT routeID AS routeID_, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyEndStationName, departureTime, arrivalTime
                    FROM TimeTable INNER JOIN (
                        SELECT routeID AS routeID_, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndStationName, journeyEndNo
                        FROM TrainRoute INNER JOIN (
                                SELECT TS1.name AS trackName_, P1.stationName AS journeyStartStationName, P1.cardinalNo AS journeyStartNo, P2.stationName AS journeyEndStationName, P2.cardinalNo AS journeyEndNo
                                FROM TrackSection AS TS1 INNER JOIN Passes AS P1 ON (TS1.name = P1.name) JOIN TrackSection AS TS2 INNER JOIN Passes AS P2 ON (TS2.name = P2.name)
                                WHERE P1.stationName = ? AND P2.stationName = ? AND TS1.name = TS2.name
                            ) ON TrainRoute.trackName = trackName_
                        WHERE	(journeyStartNo < journeyEndNo AND direction = 0 AND journeyStartNo >= startStationCardinalNo AND journeyEndNo <= endStationCardinalNo) OR (journeyStartNo > journeyEndNo AND direction = 1 AND journeyStartNo <= startStationCardinalNo AND journeyEndNo >= endStationCardinalNo)
                        ) ON (routeID_ = TimeTable.routeID)
                    WHERE TimeTable.stationName = ? AND (TIME(?) <= TIME(departureTime)) --Selection from starting time
                ) INNER JOIN StartFromStationInDay ON (routeID_ = StartFromStationInDay.routeID)
                WHERE (dayOfTheWeek = ?)
                """
    result = c.execute(queryDay1, (staStation, endStation, staStation,time, dayOfTheWeek)).fetchall()
    if len(result) == 0:
        console.print(f"! No Result for {dayOfTheWeek}", style='red')
    else:
        for row in result:
            print(row)
    queryDay2 = """
                SELECT routeID, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, departureTime, arrivalTime, dayOfTheWeek
                FROM (
                    SELECT routeID AS routeID_, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, departureTime, arrivalTime
                    FROM TimeTable INNER JOIN (
                        SELECT routeID AS routeID_, operator, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndNo
                        FROM TrainRoute INNER JOIN (
                                SELECT TS1.name AS trackName_, P1.stationName AS journeyStartStationName, P1.cardinalNo AS journeyStartNo, P2.stationName AS journeyEndStationName, P2.cardinalNo AS journeyEndNo
                                FROM TrackSection AS TS1 INNER JOIN Passes AS P1 ON (TS1.name = P1.name) JOIN TrackSection AS TS2 INNER JOIN Passes AS P2 ON (TS2.name = P2.name)
                                WHERE P1.stationName = ? AND P2.stationName = ? AND TS1.name = TS2.name
                            ) ON TrainRoute.trackName = trackName_
                        WHERE	(journeyStartNo < journeyEndNo AND direction = 0 AND journeyStartNo >= startStationCardinalNo AND journeyEndNo <= endStationCardinalNo) OR (journeyStartNo > journeyEndNo AND direction = 1 AND journeyStartNo <= startStationCardinalNo AND journeyEndNo >= endStationCardinalNo)
                        ) ON (routeID_ = TimeTable.routeID)
                    WHERE TimeTable.stationName = ?
                ) INNER JOIN StartFromStationInDay ON (routeID_ = StartFromStationInDay.routeID)
                WHERE (dayOfTheWeek = ?);
                """
    result = c.execute(queryDay2, (staStation, endStation, staStation, nextDay)).fetchall()
    if len(result) == 0:
        console.print(f"! No Result for {nexDay}", style='red')
    else:
        for row in result:
            print(row)
    conn.close()

def main(fileExists):
    if not fileExists: 
        create_tables()
        insert_tables()
    print('\nWelcome to Norwegian Railways!')
    funcUser = '' 
    while funcUser != '0':
        funcUser = input('\n MENU: \n [1] Get all train routes that stop at a particular station on a given weekday \n [2] Search Routes \n [3] Signup \n [4] Buy Tickets \n [0] Exit \n > ')
        if funcUser == '1':
            get_train_routes()
        elif funcUser == '2':
            findRoutesDateTime()
        elif funcUser == '3':
            register_customer()
        elif funcUser == '4':
            new_order()

#Connect to the db
fileExists = True
if not os.path.exists(db_path):
    fileExists = False

main(fileExists)

