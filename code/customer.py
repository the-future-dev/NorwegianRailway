import re
import sqlite3
from datetime import datetime
from rich.console import Console
from code.routeSearch import findRoutesDateTime

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

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def buy_chair_ticket(occurrence, c):
    # [0]: routeID [1]: direction [2]: nChairCars [3]: nSleepCars [4]: routeName
    # [5]: startingStation [6]: startNo [7]: endingStation [8]: endNo
    # [9]:: timeDeparture [10]: timeArrival [11]: DayOfTheWeek [12]: date
    routeID = occurrence[0]
    direction = occurrence[1]
    nChairCars = occurrence[2]
    nSleepCars = occurrence[3]
    routeName = occurrence[4]
    sNo = occurrence[6]
    eNo = occurrence[8]
    date = occurrence[12]

    #fetching the Available Seats in the route
    
    query = """
                SELECT routeID, ChairCar.carID AS carID, cardinalNo, seatNo
                FROM ChairCar INNER JOIN CarInRoute USING (carID)INNER JOIN Seat USING (carID)
                WHERE CarInRoute.routeID = ?  AND (routeID, carID, seatNo) NOT IN (
                    SELECT routeID, carID, seatNO
                    FROM ChairTicket INNER JOIN Passes AS P1 ON (ChairTicket.startingStationName = P1.stationName) INNER JOIN Passes AS P2 ON (ChairTicket.endingStationName = P2.stationName)
                    WHERE dateOfOccurrence= ? AND (? = 0 AND ((? >= P1.cardinalNo AND ? <= P2.cardinalNo) OR (? >= P1.cardinalNo AND ? <= P2.cardinalNo) OR (? <= P1.cardinalNo AND ? >= P2.cardinalNo)))
                        OR 
                        (? = 1) AND ((? >= P2.cardinalNo AND ? <= P1.cardinalNo ) OR (? >= P2.cardinalNo AND ? <= P1.cardinalNo) OR (? <= P2.cardinalNo AND ? >= P1.cardinalNo))
                );
            """
    c.execute(query, (routeID, date, direction, sNo, sNo, eNo, eNo,sNo, eNo, direction, sNo, sNo, eNo, eNo, eNo, sNo))
    result = c.fetchall() # [0] routeID, [1] carID, [2] cardinalNo, [3] seatNo
    if result is None:
        console.print("No seats available", style='red')
    else:
        for i in range(1, nChairCars+1):
            seatsForCar = []
            for j in range(1, 13):
                seat = 'NA'
                for el in result:
                    if el[2] == i and el[3] == j:
                        seat = 'AV'
                seatsForCar.append(seat)
            print(f"Car [{i}]:")
            print("__________________________________")
            print(f"[] 1 {GREEN if seatsForCar[0] == 'AV' else RED}{seatsForCar[0]}{RESET} | 2 {GREEN if seatsForCar[1] == 'AV' else RED}{seatsForCar[1]}{RESET}|\t| 3 {GREEN if seatsForCar[2] == 'AV' else RED}{seatsForCar[2]}{RESET} | 4 {GREEN if seatsForCar[3] == 'AV' else RED}{seatsForCar[3]}{RESET} []")
            print(f"[] 5 {GREEN if seatsForCar[4] == 'AV' else RED}{seatsForCar[4]}{RESET} | 6 {GREEN if seatsForCar[5] == 'AV' else RED}{seatsForCar[5]}{RESET}|\t| 7 {GREEN if seatsForCar[6] == 'AV' else RED}{seatsForCar[6]}{RESET} | 8 {GREEN if seatsForCar[7] == 'AV' else RED}{seatsForCar[7]}{RESET} []")
            print(f"[] 9 {GREEN if seatsForCar[8] == 'AV' else RED}{seatsForCar[8]}{RESET} | 10 {GREEN if seatsForCar[9] == 'AV' else RED}{seatsForCar[9]}{RESET}|\t| 11 {GREEN if seatsForCar[10] == 'AV' else RED}{seatsForCar[10]}{RESET} | 12 {GREEN if seatsForCar[11] == 'AV' else RED}{seatsForCar[11]}{RESET} []\n\n")
            print("__________________________________")

    #############################
    ##SELECTION
    #############################
    ##INSERTION
    #############################

    return 'ciao'

def new_order(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print('You can buy tickets for the three main routes:')
    
    name = input('Enter your name: ')
    email = input('Enter your email: ')
    phone = int(input('Enter your phone number: '))

    # Check if the user exists
    query = "SELECT customerID FROM Customer WHERE name=? AND email=? AND phone=?;"
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
        query = "INSERT INTO CustomerOrder (purchaseTime, purchaseDate, customerID) VALUES (?, ?, ?);"
        c.execute(query, (purchaseTime, purchaseDate, customerID))
        conn.commit()

        #TO comment
        console.print(f'\nLogged In !', style='green')
        funcUser = ''
        while True:
            funcUser = input('\n Ticket Shop: \n [1] Buy a Ticket \n [0] Exit Ticket Shop \n \t>')
            if funcUser == '0':
                break
            possibleRoutes = findRoutesDateTime(db_path)
            occurrenceExists = []
            for index, route in enumerate(possibleRoutes):
                query = "SELECT * FROM TrainOccurrence WHERE dateOfOccurrence = ? AND routeID = ?;"
                c.execute(query, (route[-1], route[0]))
                aResult = c.fetchone()
                if aResult is not None:
                    occurrenceExists.append(route)
            
            if len(occurrenceExists) != 0:
                if (len(occurrenceExists) == len(possibleRoutes)):
                    console.print(" All the routes are available to be booked", style='green')
                else:
                    console.print("\n! Not all the routes are available\n", style='yellow')
                    console.print("\nAvailable routes", style='green')
                    for index, row in enumerate(occurrenceExists):
                        print(f'[{index}]: {row}')
                
                idx = int(input(f'Choose your route by inserting the index [0, {len(occurrenceExists)-1}]: '))
                # if not (0 <= idx < len(occurrenceExists)):
                #     idx = int(input(f'Choose your route by inserting the index [0, {len(occurrenceExists)-1}]: '))
                
                funcUser = input('\n Ticket Shop: \n [1] Buy a Ticket for a Chair \n [2] Buy a ticket for a Bed \n \t>')
                if funcUser == '1':
                    buy_chair_ticket(occurrenceExists[idx], c)
                elif funcUser == '2':
                    # buy_bed_ticket(occurrenceExists[idx])
                    break
                else:
                    break
            else:
                console.print("! All the routes are sheduled but it's too early to book them, come back later", style='red')

    conn.close()
