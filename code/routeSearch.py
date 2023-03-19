import sqlite3
from rich.console import Console
from code.helpers import dateToWeekday, inputWithFormat, next_day

console = Console()

##############################################################################
## User Story: c
## For a specified station, the user should be able to get all train routes that stop at the station on a given weekday.
##############################################################################
def get_train_routes(db_path):
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

################################################################################################################################
## User Story: d
## The user should be able to search for train routes going between a starting station and an ending
## station based on date and time. All routes for the same day and the next should be returned and
## sorted by time.
################################################################################################################################
def findRoutesDateTime(db_path):
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