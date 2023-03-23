import sqlite3
from rich.console import Console
from rich.text import Text
from code.helpers import dateToWeekday, inputWithFormat, next_day, next_dayOfTheWeek

console = Console(color_system="256")

##############################################################################
## User Story: c
## For a specified station, the user should be able to get all train routes that stop at the station on a given weekday.
##############################################################################
def get_train_routes(db_path):
    #Connect to database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    
    station_name = input('Insert the station name (ex. Trondheim): ')
    weekday = input('Insert the day (ex. Monday): ')

    # Query to find train routes passing through the inputted station on the inputted day
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
    
    # Error message if no results are found
    if not result:
        console.print(f"! No Tracks were found to pass at {station_name} during {weekday}.", style='red')
    
    # Loop through results and execute another query to find arrival and departure times for each route at the inputted station
    # CODERS: row: [0] routeID | [1] operator | [2] direction | [3] trackName
    for row in result:
        timeQuery = """
                        SELECT arrivalTime, departureTime 
                        FROM Timetable
                        WHERE routeID = ? AND stationName = ?
                    """
        c.execute(timeQuery, (row[0], station_name))
        time = c.fetchone()
        # Print out an error message if no times are found or print out formatted information about each route and its corresponding arrival/departure times
        if time is None:
            console.print(f"! Bad db implementation", style='red')
        else:
            if time[0] is None:
                console.print(f">> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  will start at {time[1]}", style='green')
            elif time[1] is None:
                console.print(f">> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  will end at at {time[0]}", style='green')
            else:
                console.print(f">> Route ID: {row[0]}, named {row[3]} and opeated by {row[1]}  from {time[0]} to {time[1]}", style='green')

    #Close connection to the database
    conn.close()

################################################################################################################################
## User Story: d
## The user should be able to search for train routes going between a starting station and an ending
## station based on date and time. All routes for the same day and the next should be returned and
## sorted by time.
################################################################################################################################
def findRoutesDateTime(db_path):
    #connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print('Search for train routes going between a starting station and an ending station based on date and starting time.')

    #input
    staStation = input('Starting Station (ex. Trondheim): ')
    endStation = input('Starting Station (ex. Mo i Rana): ')
    date = inputWithFormat('Date (format YYYY-MM-DD): ', '%Y-%m-%d')
    time = inputWithFormat('Starting Time (format HH:MM): ', '%H:%M')

    # Input interpretation: find day of the week and next day of the week
    dayOfTheWeek = dateToWeekday(date)
    nextDay = next_dayOfTheWeek(dayOfTheWeek)
    dateNext = next_day(date)

    #find train routes between starting and ending stations based on inputted date and time
    queryDay1 = """
                SELECT routeID, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndStationName, journeyEndNo, departureTime, arrivalTime, dayOfTheWeek
                FROM (
                    SELECT routeID AS routeID_, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName,journeyStartNo, journeyEndStationName,journeyEndNo, departureTime, arrivalTime
                    FROM TimeTable INNER JOIN (
                        SELECT routeID AS routeID_, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndStationName, journeyEndNo
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
                ORDER BY departureTime;
                """
    resultDay1 = c.execute(queryDay1, (staStation, endStation, staStation,time, dayOfTheWeek)).fetchall()

    #find train routes between starting and ending stations of the next day
    queryDay2 = """
                SELECT routeID, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndStationName, journeyEndNo, departureTime, arrivalTime, dayOfTheWeek
                FROM (
                    SELECT routeID AS routeID_, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyStartNo, journeyEndStationName, journeyEndNo, departureTime, arrivalTime
                    FROM TimeTable INNER JOIN (
                        SELECT routeID AS routeID_, direction, numberOfChairCars, numberOfSleepingCars, trackName, journeyStartStationName, journeyEndStationName, journeyStartNo, journeyEndNo
                        FROM TrainRoute INNER JOIN (
                                SELECT TS1.name AS trackName_, P1.stationName AS journeyStartStationName, P1.cardinalNo AS journeyStartNo, P2.stationName AS journeyEndStationName, P2.cardinalNo AS journeyEndNo
                                FROM TrackSection AS TS1 INNER JOIN Passes AS P1 ON (TS1.name = P1.name) JOIN TrackSection AS TS2 INNER JOIN Passes AS P2 ON (TS2.name = P2.name)
                                WHERE P1.stationName = ? AND P2.stationName = ? AND TS1.name = TS2.name
                            ) ON TrainRoute.trackName = trackName_
                        WHERE	(journeyStartNo < journeyEndNo AND direction = 0 AND journeyStartNo >= startStationCardinalNo AND journeyEndNo <= endStationCardinalNo) OR (journeyStartNo > journeyEndNo AND direction = 1 AND journeyStartNo <= startStationCardinalNo AND journeyEndNo >= endStationCardinalNo)
                        ) ON (routeID_ = TimeTable.routeID)
                    WHERE TimeTable.stationName = ?
                ) INNER JOIN StartFromStationInDay ON (routeID_ = StartFromStationInDay.routeID)
                WHERE (dayOfTheWeek = ?)
                ORDER BY departureTime;
                """
    resultDay2 = c.execute(queryDay2, (staStation, endStation, staStation, nextDay)).fetchall()

    # Combine results from both queries into one list adding the correct dates
    result = []
    for row in resultDay1:
        new_row = row + (date,)
        result.append(new_row)
    for row in resultDay2:
        new_row = row + (dateNext,)
        result.append(new_row)

    # Print out results in a formatted manner or an error message if no results are found
    if len(result) == 0:
        console.print(f"! No Result for {dayOfTheWeek} or {nextDay}", style='red')
    else:
        console.print("Routes Scheduled",style='cyan')
        for index, row in enumerate(result):
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
    # Close connection to database and return result list
    conn.close()    
    return result