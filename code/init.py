import sqlite3

##############################################################################
## Database definition function
##############################################################################
def create_tables(db_path, file_path='database/dbDefinition.sql'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(file_path, 'r') as f:
        sql_script = f.read()

    c.executescript(sql_script)

    conn.commit()
    conn.close()

##############################################################################
## User Stories: a and b
## Database basic insertion function:
## checkout database/dbDefinition.sql for more information
##############################################################################
def insert_tables(db_path, file_path='database/dbInsertion.sql'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(file_path, 'r') as f:
        sql_script = f.read()

    c.executescript(sql_script)
    conn.commit()
    
    #Insertion of the Seats
    for carID in range(2, 6):
        for seatNo in range(1, 13):
            c.execute("""INSERT INTO Seat (carID, seatNo) SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Seat WHERE carID = ? AND seatNo = ?);""", (carID, seatNo, carID, seatNo))
    
    #Insertion of the Beds
    #for carId in range(1):
    carID = 1
    for compartmentNo in range(1, 5):
        for bedNo in range(1,3):
            c.execute("""INSERT INTO Bed(carID, compartmentNo, bedNo) VALUES (?, ?, ?)""", (carID, compartmentNo,bedNo))
    
    conn.commit()
    conn.close()