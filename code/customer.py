import re
import sqlite3
from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from code.routeSearch import findRoutesDateTime

console = Console(color_system="256")

##############################################################################################################
## User Story: e
## The user should be able to register in the customer registry.
##############################################################################################################
def register_customer(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #user input validation 
    while True:
        name = input('> Enter your name: ')
        if (re.match(r"^[a-zA-Z\s]*$", name)):
            break
        console.print("! Invalid name. Only letters and spaces are allowed. No special letters. Please try again.", style= 'red')

    while True:
        email = input('> Enter your email: ')
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
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

def bedAvailable(beds, compartmentNo, bedNo):
    found = False
    for b in beds:
        if b[-1] == bedNo and b[-2] == compartmentNo:
            found = True
            break
    return found

def coloredPrintBed(beds, compartment, bedNo):
    if bedAvailable(beds, compartment, bedNo):
        return f'{GREEN}AV{RESET}'
    else:
        return f'{RED}NA{RESET}'
    
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
                SELECT routeID, SleepingCar.carID AS carID, compartmentNo, bedNo
                FROM SleepingCar INNER JOIN CarInRoute USING (carID)INNER JOIN Bed USING (carID)
                WHERE routeID = ? AND (routeID, carID, compartmentNo) NOT IN (
                    SELECT routeID, carID, compartmentNo
                    FROM BedTicket
                    WHERE dateOfOccurrence = ?
                );
            """
    c.execute(query, (routeID, date))
    beds = c.fetchall() # [0] routeID, [1] carID, [2] cardinalNo, [3] compartmentNo, [4] bedNo
    if beds is not None:
        # As the implemenattion just has one car that's with bed the function is simplified
        print(f"Car #1:")
        print(f"Compartment #{1} | Bed 1: {coloredPrintBed(beds, 1, 1)} | Bed 2: {coloredPrintBed(beds, 1, 2)}")
        print(f"Compartment #{2} | Bed 1: {coloredPrintBed(beds, 2, 1)} | Bed 2: {coloredPrintBed(beds, 2, 2)}")
        print(f"Compartment #{3} | Bed 1: {coloredPrintBed(beds, 3, 1)} | Bed 2: {coloredPrintBed(beds, 3, 2)}")
        print(f"Compartment #{4} | Bed 1: {coloredPrintBed(beds, 4, 1)} | Bed 2: {coloredPrintBed(beds, 4, 2)}")
    
        while True:
            #carNo           = int(input("Select the car: "))
            compartmentNo   = int(input("Select the compartment: "))
            bedNo             = int(input("Select the number of beds (1 or 2): "))
            if bedAvailable(beds, compartmentNo, bedNo):
                break
            else:
                console.print("The selected car and seat are not available. Please try again.", style='red')
        
        carID = 1
        if carID is not None:
            #############################
            ##INSERTION
            #############################
            query = "INSERT INTO BedTicket (carID, compartmentNo, bedNo, dateOfOccurrence, routeID, orderID, startingStationName, endingStationName) VALUES (?,?,?,?,?,?,?,?);"
            try:
                c.execute(query, (carID, compartmentNo, 1, date, routeID, orderID, startingStationName, endingStationName))
                conn.commit()
                if bedNo == 2:
                    c.execute(query, (carID, compartmentNo, 2, date, routeID, orderID, startingStationName, endingStationName))
                    conn.commit()
                console.print("Purchase Successful", style="green")
            except Exception as e:
                console.print(f"! Unsuccessful Purchase: {e}", style="red")
        else:
            console.print(f"! Unsuccessful Selection")
    else:
        console.print(f"! Unsuccessful Selection")

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
        availableSeats = []
        for i in range(1, nChairCars+1):
            seatsForCar = []
            for j in range(1, 13):
                seat = 'NA'
                for el in chairs:
                    if el[2] == i and el[3] == j:
                        seat = 'AV'
                        availableSeats.append((i, j))
                seatsForCar.append(seat)
            print(f"Car #{i}: ")
            print("__________________________________________")
            for i in range(0, 12, 4):
                text = Text()
                for j in range(i, i + 4):
                    color = "green" if seatsForCar[j] == "AV" else "red"
                    if (j == 0 or j == 4 or j == 8):
                        text.append('[] ')
                    text.append(f"{j + 1} {seatsForCar[j]}", style=color)
                    if (j == 11 or j == 3 or j == 7):
                        text.append(' []')
                    else:
                        text.append(' | ')
                console.print(text)
            print("__________________________________________\n\n")
    
        #############################
        ##SELECTION
        #############################
        while True:
            carNo = int(input("Select the car: "))
            seat = int(input("Select the seat: "))
            if (carNo, seat) in availableSeats:
                break
            else:
                console.print("The selected car and seat are not available. Please try again.", style='red')
        
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
    if (not re.match(r"^[a-zA-Z\s]*$", name)):
        return
    
    email = input('Enter your email: ')
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        console.print("! Invalid email.", style='red')
        return
    
    phone = input('Enter your phone number: ')
    if not re.match(r"^\d{8}$", phone):
        console.print("! Invalid phone number. Please enter a valid 8-digit phone number.", style='red')
        return
    
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
                        console.print("\n! Not all the routes are available to be booked\n", style='yellow')
                        console.print("AVAILABLE ROUTES:", style='bold cyan')
                        for index, row in enumerate(occurrenceExists):
                            text = Text(f'Index ', style='bold')
                            text.append(f'{index}', style='#FFAF00')
                            text.append(f':\t N-{row[0]} will pass on {row[-2]} the {row[-1]} at ')
                            text.append(f'{row[9]}', style='green')
                            text.append(f' The train has ')
                            text.append(f'{row[2]}', style='magenta')
                            text.append(f' seats cars and ')
                            text.append(f'{row[3]}', style='cyan')
                            text.append(f' sleeping cars.')
                            console.print(text)
                    
                    prompt_text = f'Choose your route by inserting the [bold #FFAF00]index[/bold #FFAF00] [0, {len(occurrenceExists)-1}]: '
                    idx = int(Prompt.ask(prompt_text, console=console))
                    if not (0 <= idx < len(occurrenceExists)):
                        idx = int(Prompt.ask(prompt_text, console=console))
                    
                    funcUser = input('\n Inside Ticket Shop: \n [1] Buy a Ticket for a Chair \n [2] Buy a ticket for a Bed \n [0] Exit\n \t>')
                    
                    if funcUser == '1':
                        buy_chair_ticket(occurrenceExists[idx], c, conn, orderID)
                    elif funcUser == '2' and occurrenceExists[idx][3] != 0:
                        buy_bed_ticket(occurrenceExists[idx], c, conn, orderID)
                    elif funcUser == '2' and occurrenceExists[idx][3] == 0:
                        console.print("No Sleeping Car for the selected train :<", style='red')
            else:
                console.print("! All the routes are sheduled but it's too early to book them, come back later", style='red')

    conn.close()


##############################################################################################################################################
## User Story: h
## All information about purchases made for future trips should be available for a user. This 
## functionality should be programmed
##############################################################################################################################################

import re
import sqlite3

def get_orders(db_path):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    # Validate name
    if not re.match(r"^[a-zA-Z\s]*$", name):
        print("Invalid name. Only letters and spaces are allowed. No special letters.")
        return

    # Validate email
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        console.print("! Invalid email.", style='red')
        return

    # Validate phone number
    if not re.match(r"^\d{8}$", phone):
        console.print("! Invalid phone number. Please enter a valid 8-digit phone number.", style='red')
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Execute the query to retrieve the customerID
    c.execute("SELECT DISTINCT customerID FROM Customer WHERE name = ? AND email = ? AND phone = ?;", (name, email, phone))
    
    customerID = c.fetchone()
    
    if customerID:
        # print(f"The customer ID is {customerID[0]}")
        
        # Retrieve bed ticket orders
        c.execute("""SELECT purchaseTime, purchaseDate, routeID, carID, compartmentNo, bedNo,
                     dateOfOccurrence, startingStationName, endingStationName FROM CustomerOrder 
                     LEFT JOIN BedTicket ON CustomerOrder.orderID = BedTicket.orderID 
                     WHERE CustomerOrder.customerID = ? AND ticketID NOT NULL;""", (customerID[0],))
        
        bed_ticket_orders = c.fetchall()
        
        if bed_ticket_orders:
            print("\nBed Ticket Orders:")
            for order in bed_ticket_orders:
                purchase_time, purchase_date, route_id, car_id,\
                compartment_no, bed_no,date_of_occurrence,\
                starting_station_name,\
                ending_station_name= order

                console.print(f"Route ID: [red]{route_id}[/red] Car ID: [blue]{car_id}[/blue] Compartment No.: [green]{compartment_no}[/green] Bed No.: [yellow]{bed_no}[/yellow] Date of Occurrence: [magenta]{date_of_occurrence}[/magenta]", end="")
                console.print(f" Starting Station Name: [cyan]{starting_station_name}[/cyan] Ending Station Name: [purple]{ending_station_name}[/purple]")
        else:
            console.print("No bed tickets", style='red')
        
        # Retrieve chair ticket orders
        c.execute("""SELECT purchaseTime,purchaseDate,
                     routeID,
                     carID,
                     seatNo,
                     dateOfOccurrence,
                     startingStationName,
                     endingStationName FROM CustomerOrder 
                     LEFT JOIN ChairTicket ON CustomerOrder.orderID=ChairTicket.orderID 
                     WHERE CustomerOrder.customerID=? AND ticketID NOT NULL;""",(customerID[0],))
        
        chair_ticket_orders=c.fetchall()
        
        if chair_ticket_orders:
            print("\nChair Ticket Orders:")
            for order in chair_ticket_orders:
                purchase_time,purchase_date,\
                route_id,\
                car_id,\
                seat_no,date_of_occurrence,\
                starting_station_name,\
                ending_station_name=order

                console.print(f"Route ID: [red]{route_id}[/red] Car ID: [blue]{car_id}[/blue] Seat No.: [green]{seat_no}[/green] Date of Occurrence: [yellow]{date_of_occurrence}[/yellow]", end="")
                console.print(f" The Starting Station Name: [magenta]{starting_station_name}[/magenta] The Ending Station Name: [cyan]{ending_station_name}[/cyan]")
        else:
            console.print("No chair tickets", style='red')