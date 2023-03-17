INSERT INTO RailwayStation (stationName, altitude) SELECT 'Trondheim', 5.1 WHERE NOT EXISTS ( SELECT stationName FROM RailwayStation WHERE stationName = 'Trondheim');
INSERT INTO RailwayStation (stationName, altitude) SELECT 'Steinkjer', 3.6 WHERE NOT EXISTS (SELECT stationName FROM RailwayStation WHERE stationName = 'Steinkjer');
INSERT INTO RailwayStation (stationName, altitude) SELECT 'Mosjoen', 6.8 WHERE NOT EXISTS (SELECT stationName FROM RailwayStation WHERE stationName = 'Mosjoen');
INSERT INTO RailwayStation (stationName, altitude) SELECT 'Mo i Rana', 3.5 WHERE NOT EXISTS (SELECT stationName FROM RailwayStation WHERE stationName = 'Mo i Rana');
INSERT INTO RailwayStation (stationName, altitude) SELECT 'Fauske', 34.0 WHERE NOT EXISTS (SELECT stationName FROM RailwayStation WHERE stationName = 'Fauske');
INSERT INTO RailwayStation (stationName, altitude) SELECT 'Bodo', 4.1 WHERE NOT EXISTS (SELECT stationName FROM RailwayStation WHERE stationName = 'Bodo');

INSERT INTO SubSection (length, trackType, stationA, stationB) SELECT 120.0, 'double', 'Trondheim', 'Steinkjer' WHERE NOT EXISTS (SELECT * FROM SubSection WHERE subSectionID = 1);
INSERT INTO SubSection (length, trackType, stationA, stationB) SELECT 280.0, 'single', 'Steinkjer', 'Mosjoen' WHERE NOT EXISTS (SELECT * FROM SubSection WHERE subSectionID = 2);
INSERT INTO SubSection (length, trackType, stationA, stationB) SELECT 90.0, 'single', 'Mosjoen', 'Mo i Rana' WHERE NOT EXISTS (SELECT * FROM SubSection WHERE subSectionID = 3);
INSERT INTO SubSection (length, trackType, stationA, stationB) SELECT 170.0, 'single', 'Mo i Rana', 'Fauske' WHERE NOT EXISTS (SELECT * FROM SubSection WHERE subSectionID = 4);
INSERT INTO SubSection (length, trackType, stationA, stationB) SELECT 60.0, 'single', 'Fauske', 'Bodo' WHERE NOT EXISTS (SELECT * FROM SubSection WHERE subSectionID = 5);

INSERT INTO TrackSection (name, drivingEnergy, startStationName, endStationName) SELECT 'NordlandLine', 'diesel', 'Trondheim', 'Bodo' WHERE NOT EXISTS (SELECT * FROM TrackSection WHERE name='NordlandLine');

INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Trondheim', 1 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Trondheim'); 
INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Steinkjer', 2 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Steinkjer');
INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Mosjoen', 3 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Mosjoen');
INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Mo i Rana', 4 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Mo i Rana');
INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Fauske', 5 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Fauske');
INSERT INTO Passes (name, stationName, cardinalNo) SELECT 'NordlandLine', 'Bodo', 6 WHERE NOT EXISTS (SELECT * FROM Passes WHERE name = 'NordlandLine' AND stationName = 'Bodo');

INSERT INTO TrainRoute (operator, direction,startStationCardinalNo,endStationCardinalNo, numberOfChairCars, numberOfSleepingCars, trackName) SELECT 'SJ', 0, 1, 6, 2, 0, 'NordlandLine' WHERE NOT EXISTS (SELECT * FROM TrainRoute WHERE routeID = 1);
INSERT INTO TrainRoute (operator, direction,startStationCardinalNo,endStationCardinalNo, numberOfChairCars, numberOfSleepingCars, trackName) SELECT 'SJ', 0, 1, 6, 1, 1, 'NordlandLine' WHERE NOT EXISTS (SELECT * FROM TrainRoute WHERE routeID = 2);
INSERT INTO TrainRoute (operator, direction,startStationCardinalNo,endStationCardinalNo, numberOfChairCars, numberOfSleepingCars, trackName) SELECT 'SJ', 1, 4, 1, 1, 0, 'NordlandLine' WHERE NOT EXISTS (SELECT * FROM TrainRoute WHERE routeID = 3);

INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Sunday', 1 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Sunday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Monday', 2 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Monday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Tuesday', 3 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Tuesday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Wednesday', 4 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Wednesday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Thursday', 5 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Thursday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Friday', 6 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Friday');
INSERT INTO DaysOfTheWeek ( dayOfTheWeek, dayNo) SELECT 'Saturday', 7 WHERE NOT EXISTS (SELECT * FROM DaysOfTheWeek WHERE dayOfTheWeek = 'Saturday');

INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 1, 'Monday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Monday' AND routeID = 1);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 1, 'Tuesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Tuesday' AND routeID = 1);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 1, 'Wednesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Wednesday' AND routeID = 1);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 1, 'Thursday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Thursday' AND routeID = 1);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 1, 'Friday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Friday' AND routeID = 1);

INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Monday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Monday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Tuesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Tuesday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Wednesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Wednesday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Thursday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Thursday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Friday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Friday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Sunday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Sunday' AND routeID = 2);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 2, 'Saturday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Saturday' AND routeID = 2); 

INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 3, 'Monday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Monday' AND routeID = 3);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 3, 'Tuesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Tuesday' AND routeID = 3);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 3, 'Wednesday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Wednesday' AND routeID = 3);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 3, 'Thursday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Thursday' AND routeID = 3);
INSERT INTO StartFromStationInDay (routeID, dayOfTheWeek) SELECT 3, 'Friday' WHERE NOT EXISTS (SELECT * FROM StartFromStationInDay WHERE dayOfTheWeek = 'Friday' AND routeID = 3);

INSERT INTO TrainCar (type) SELECT 'SleepingCar' WHERE NOT EXISTS (SELECT * FROM TrainCar WHERE carID = 1);
INSERT INTO TrainCar (type) SELECT 'ChairCar' WHERE NOT EXISTS (SELECT * FROM TrainCar WHERE carID = 2);
INSERT INTO TrainCar (type) SELECT 'ChairCar' WHERE NOT EXISTS (SELECT * FROM TrainCar WHERE carID = 3);
INSERT INTO TrainCar (type) SELECT 'ChairCar' WHERE NOT EXISTS (SELECT * FROM TrainCar WHERE carID = 4);
INSERT INTO TrainCar (type) SELECT 'ChairCar' WHERE NOT EXISTS (SELECT * FROM TrainCar WHERE carID = 5);

INSERT INTO SleepingCar (carID) SELECT 1 WHERE NOT EXISTS (SELECT * FROM SleepingCar WHERE carID = 1);
INSERT INTO ChairCar (carID, numberOfRows, numberOfSeatsXRow) SELECT 2, 3, 4 WHERE NOT EXISTS (SELECT * FROM ChairCar WHERE carID = 2);
INSERT INTO ChairCar (carID, numberOfRows, numberOfSeatsXRow) SELECT 3, 3, 4  WHERE NOT EXISTS (SELECT * FROM ChairCar WHERE carID = 3);
INSERT INTO ChairCar (carID, numberOfRows, numberOfSeatsXRow) SELECT 4, 3, 4  WHERE NOT EXISTS (SELECT * FROM ChairCar WHERE carID = 4);
INSERT INTO ChairCar (carID, numberOfRows, numberOfSeatsXRow) SELECT 5, 3, 4  WHERE NOT EXISTS (SELECT * FROM ChairCar WHERE carID = 5);
 
INSERT INTO Compartment (carID, compartmentNo) VALUES (1,1);
INSERT INTO Compartment (carID, compartmentNo) VALUES (1,2);
INSERT INTO Compartment (carID, compartmentNo) VALUES (1,3);
INSERT INTO Compartment (carID, compartmentNo) VALUES (1,4);

INSERT INTO Bed(carID, compartmentNo, bedNo) VALUES (1, 1, 1);
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Trondheim', '07:49', NULL);
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Steinkjer', '09:51', '09:46');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Mosjoen', '13:20', '13:15');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Mo i Rana', '09:51', '09:46');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Fauske', '16:49', '16:44');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (1, 'Bodo', NULL, '17:34');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Trondheim', '23:05', NULL);
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Steinkjer', '00:57', '00:52');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Mosjoen', '04:41', '04:36');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Mo i Rana', '05:55', '05:50');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Fauske', '08:19', '08:14');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (2, 'Bodo', NULL, '09:05');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (3, 'Mo i Rana', '08:11', NULL);
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (3, 'Mosjoen', '09:14', '09:09');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (3, 'Steinkjer', '12:31', '12:26');
INSERT INTO TimeTable (routeID, stationName, departureTime, arrivalTime) VALUES (3, 'Trondheim S', NULL, '14:13');
 

 -- task E ------------------------------ --Date: YYYY-MM-DD
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-03', 1);
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-03', 2);
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-03', 3);
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-04', 1);
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-04', 2);
INSERT INTO TrainOccurrence (dateOfOccurrence, routeID) VALUES ('2023-04-04', 3);
