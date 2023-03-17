import os
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

    station_name = input('Insert the station name [ex. Trondheim]: ')
    weekday = input('Insert the day [ex. Monday]: ')
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

def main(fileExists):
    if not fileExists: 
        create_tables()
        insert_tables()
    print('Welcome to NorwegianRailways!')
    funcUser = input('Press 0 to get all train routes that stop at a particular station on a given weekday')
    if funcUser == '0':
        get_train_routes()

#Connect to the db
fileExists = True
if not os.path.exists(db_path):
    fileExists = False

main(fileExists)

