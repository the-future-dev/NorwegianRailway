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
def buy_bed_ticket(occurrence, c, conn, orderID):
    routeID = int(occurrence[0])
    direction = int(occurrence[1])
    nChairCars = int(occurrence[2])
    nSleepCars = int(occurrence[3])
    routeName = occurrence[4]
    startingStationName = occurrence[5]
    sNo = int(occurrence[6])
    endingStationName = occurrence[7]
    eNo = int(occurrence[8])
    date = occurrence[12]

    query = """
                SELECT routeID, SleepingCar.carID AS carID, cardinalNo, compartmentNo, bedNo
                FROM SleepingCar INNER JOIN CarInRoute USING (carID)INNER JOIN Bed USING (carID)
                WHERE routeID = ? AND (routeID, carID, compartmentNo) NOT IN (
                    SELECT routeID, carID, compartmentNo
                    FROM BedTicket
                    WHERE dateOfOccurrence = ?
                );
            """
    c.execute(query, (routeID, date))
    beds = c.fetchall()

    if beds is None:
        console.log("No bed available", style='red')
    else:
        for i in range(nChairCars, nChairCars+nSleepCars+1):
            bedsForChair = []
            for j in range(1, 5):
                for k in range(1, 3):
                    bed = 'NA'
                    for el in beds:
                        if el[1] == i and el[2] == j and el[3] == k:
                            bed = 'AV'
                    bedsForChair.append(bed)
            print(f"Car #{i}:")
            print(f"Compartment #1 | Bed 1: {GREEN if bedsForChair[0] == 'AV' else RED}{bedsForChair[0]}{RESET} | Bed 2: {GREEN if bedsForChair[1] == 'AV' else RED}{bedsForChair[1]}{RESET}")
            print(f"Compartment #2 | Bed 1: {GREEN if bedsForChair[2] == 'AV' else RED}{bedsForChair[2]}{RESET} | Bed 2: {GREEN if bedsForChair[3] == 'AV' else RED}{bedsForChair[3]}{RESET}")
            print(f"Compartment #3 | Bed 1: {GREEN if bedsForChair[4] == 'AV' else RED}{bedsForChair[4]}{RESET} | Bed 2: {GREEN if bedsForChair[5] == 'AV' else RED}{bedsForChair[5]}{RESET}")
            print(f"Compartment #4 | Bed 1: {GREEN if bedsForChair[6] == 'AV' else RED}{bedsForChair[6]}{RESET} | Bed 2: {GREEN if bedsForChair[7] == 'AV' else RED}{bedsForChair[7]}{RESET}")
    
    carID = input("Select the car: ")
    bed   = input("Select the bed: ")


def buy_chair_ticket(occurrence, c, conn, orderID):
    # [0]: routeID [1]: direction [2]: nChairCars [3]: nSleepCars [4]: routeName
    # [5]: startingStation [6]: startNo [7]: endingStation [8]: endNo
    # [9]:: timeDeparture [10]: timeArrival [11]: DayOfTheWeek [12]: date
    routeID = int(occurrence[0])
    direction = int(occurrence[1])
    nChairCars = int(occurrence[2])
    nSleepCars = int(occurrence[3])
    routeName = occurrence[4]
    startingStationName = occurrence[5]
    sNo = int(occurrence[6])
    endingStationName = occurrence[7]
    eNo = int(occurrence[8])
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
    chairs = c.fetchall() # [0] routeID, [1] carID, [2] cardinalNo, [3] seatNo
    if chairs is None:
        console.print("No seats available", style='red')
    else:
        for i in range(1, nChairCars+1):
            seatsForCar = []
            for j in range(1, 13):
                seat = 'NA'
                for el in chairs:
                    if el[2] == i and el[3] == j:
                        seat = 'AV'
                seatsForCar.append(seat)
            print(f"Car #{i}: ")
            print("__________________________________________")
            print(f"[] 1 {GREEN if seatsForCar[0] == 'AV' else RED}{seatsForCar[0]}{RESET} | 2  {GREEN if seatsForCar[1] == 'AV' else RED}{seatsForCar[1]}{RESET}|\t| 3  {GREEN if seatsForCar[2] == 'AV' else RED}{seatsForCar[2]}{RESET} | 4  {GREEN if seatsForCar[3] == 'AV' else RED}{seatsForCar[3]}{RESET} []")
            print(f"[] 5 {GREEN if seatsForCar[4] == 'AV' else RED}{seatsForCar[4]}{RESET} | 6  {GREEN if seatsForCar[5] == 'AV' else RED}{seatsForCar[5]}{RESET}|\t| 7  {GREEN if seatsForCar[6] == 'AV' else RED}{seatsForCar[6]}{RESET} | 8  { GREEN if seatsForCar[7] == 'AV' else RED}{seatsForCar[7]}{RESET} []")
            print(f"[] 9 {GREEN if seatsForCar[8] == 'AV' else RED}{seatsForCar[8]}{RESET} | 10 {GREEN if seatsForCar[9] == 'AV' else RED}{seatsForCar[9]}{RESET}|\t| 11 {GREEN if seatsForCar[10] == 'AV' else RED}{seatsForCar[10]}{RESET} | 12 {GREEN if seatsForCar[11] == 'AV' else RED}{seatsForCar[11]}{RESET} []")
            print("__________________________________________\n\n")
    
    #############################
    ##SELECTION
    #############################
    carNo = int(input("Select the car: "))
    seat = int(input("Select the seat: "))
    
    query = "SELECT DISTINCT carID FROM CarInRoute WHERE routeID = ? AND cardinalNo = ?;"
    c.execute(query, (routeID, carNo))
    carID = c.fetchone()[0]
    if carID is not None:
        #############################
        ##INSERTION
        #############################
        query = "INSERT INTO ChairTicket (carID, seatNo, dateOfOccurrence, routeID, startingStationName, endingStationName, orderID) VALUES (?,?,?,?,?,?,?);"
        try:
            c.execute(query, (carID, seat, date, routeID, startingStationName, endingStationName, orderID))
            conn.commit()
            console.print("Purchase Successful", style="green")
        except Exception as e:
            console.print(f"! Unsuccessful Purchase: {e}", style="red")
    else:
        console.print(f"! Unsuccessful Selection")
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

        query = "select orderID from CustomerOrder WHERE purchaseTime = ? AND purchaseDate = ? AND customerID = ?"
        c.execute(query, (purchaseTime, purchaseDate, customerID))
        orderID = int(c.fetchone()[0])

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
                if not (0 <= idx < len(occurrenceExists)):
                    idx = int(input(f'Choose your route by inserting the index [0, {len(occurrenceExists)-1}]: '))
                
                funcUser = input('\n Ticket Shop: \n [1] Buy a Ticket for a Chair \n [2] Buy a ticket for a Bed \n \t>')
                if funcUser == '1':
                    buy_chair_ticket(occurrenceExists[idx], c, conn, orderID)
                elif funcUser == '2':
                    # buy_bed_ticket(occurrenceExists[idx])
                    break
                else:
                    break
            else:
                console.print("! All the routes are sheduled but it's too early to book them, come back later", style='red')

    conn.close()
