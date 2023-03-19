CREATE TABLE IF NOT EXISTS RailwayStation (
    stationName VARCHAR(32) NOT NULL,
    altitude INT,
    CONSTRAINT pk PRIMARY KEY (stationName)
);

CREATE TABLE IF NOT EXISTS TrackSection (
    name VARCHAR(32) PRIMARY KEY,
    drivingEnergy VARCHAR(32),
    startStationName VARCHAR(32) NOT NULL,
    endStationName VARCHAR(32) NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (startStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (endStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SubSection (
    subSectionID INTEGER PRIMARY KEY AUTOINCREMENT,
    length INT,
    trackType VARCHAR(32),
    stationA VARCHAR(32) NOT NULL,
    stationB VARCHAR(32) NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (stationA) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (stationB) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TrainRoute (
    routeID INTEGER PRIMARY KEY AUTOINCREMENT,
    operator VARCHAR(32),
    direction INT,
    startStationCardinalNo INT NOT NULL,
    endStationCardinalNo INT NOT NULL,
    numberOfChairCars INT,
    numberOfSleepingCars INT,
    trackName VARCHAR(32) NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (trackName) REFERENCES TrackSection(name)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DaysOfTheWeek (
    dayOfTheWeek DATE NOT NULL,
    dayNo INT,
    CONSTRAINT pk PRIMARY KEY (dayOfTheWeek)
);

CREATE TABLE IF NOT EXISTS TrainCar (
    carID INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS ChairCar (
    carID INT NOT NULL,
    numberOfRows INT,
    numberOfSeatsXRow INT,
    CONSTRAINT pk PRIMARY KEY (carID),
    CONSTRAINT fk1 FOREIGN KEY (carID) REFERENCES TrainCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SleepingCar (
    carID INT NOT NULL,
    CONSTRAINT pk PRIMARY KEY (carID),
    CONSTRAINT fk1 FOREIGN KEY (carID) REFERENCES TrainCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Seat (
    carID INT NOT NULL,
    seatNo INT NOT NULL,
    -- rowNo INT,
    -- columnNo INT,
    CONSTRAINT pk PRIMARY KEY (carID, seatNo),
    CONSTRAINT fk1 FOREIGN KEY (carID) REFERENCES ChairCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Compartment (
    carID INT NOT NULL,
    compartmentNo INT NOT NULL,
    CONSTRAINT pk PRIMARY KEY (carID, compartmentNo),
    CONSTRAINT fk1 FOREIGN KEY (carID) REFERENCES TrainCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Bed (
    carID INT NOT NULL,
    compartmentNo INT NOT NULL,
    bedNo INT NOT NULL,
    CONSTRAINT pk PRIMARY KEY (carID, compartmentNo, bedNo),
    CONSTRAINT fk1 FOREIGN KEY (compartmentNo) REFERENCES Compartment(compartmentNo)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    CONSTRAINT fk2 FOREIGN KEY (carID) REFERENCES TrainCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TrainOccurrence (
    dateOfOccurrence DATE NOT NULL,
    routeID INT NOT NULL,
    CONSTRAINT pk PRIMARY KEY (dateOfOccurrence, routeID),
    CONSTRAINT fk1 FOREIGN KEY (routeID) REFERENCES TrainRoute(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customer (
    customerID INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) NOT NULL,
    email VARCHAR(32) NOT NULL,
    phone INT
);

CREATE TABLE IF NOT EXISTS CustomerOrder (
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    purchaseTime TIME,
    purchaseDate DATE,
    customerID INT NOT NULL,

    CONSTRAINT fk1 FOREIGN KEY (customerID) REFERENCES Customer(customerID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS BedTicket (
    ticketID INTEGER PRIMARY KEY AUTOINCREMENT,

    carID INT NOT NULL,
    compartmentNo INT NOT NULL,
    bedNo INT NOT NULL,

    dateOfOccurrence DATE NOT NULL,
    routeID INT NOT NULL,

    orderID INT NOT NULL,
    startingStationName VARCHAR(32) NOT NULL,
    endingStationName VARCHAR(32) NOT NULL,
    
    CONSTRAINT onceBooking UNIQUE (carID, compartmentNo, bedNo, dateOfOccurrence, routeID),

    CONSTRAINT fk1 FOREIGN KEY (carID) REFERENCES Bed(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk2 FOREIGN KEY (compartmentNo) REFERENCES Compartment(compartmentNo)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk3 FOREIGN KEY (bedNo) REFERENCES Bed(bedNo)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    CONSTRAINT fk4 FOREIGN KEY (dateOfOccurrence) REFERENCES TrainOccurrence(dateOfOccurrence)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk5 FOREIGN KEY (routeID) REFERENCES TrainOccurrence(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk6 FOREIGN KEY (orderID) REFERENCES CustomerOrder(orderID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk7 FOREIGN KEY (startingStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk8 FOREIGN KEY (endingStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ChairTicket (
    ticketID INTEGER PRIMARY KEY AUTOINCREMENT,

    carID INT NOT NULL,
    seatNo INT NOT NULL,

    dateOfOccurrence DATE NOT NULL,
    routeID INT NOT NULL,

    startingStationName VARCHAR(32) NOT NULL,
    endingStationName VARCHAR(32) NOT NULL,
    orderID INT NOT NULL,

    CONSTRAINT fk1 FOREIGN KEY (routeID, dateOfOccurrence) REFERENCES TrainOccurrence(routeID, dateOfOccurrence)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk3 FOREIGN KEY (carID, seatNo) REFERENCES Seat(carID, seatNo)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT f5 FOREIGN KEY (orderID) REFERENCES CustomerOrder(orderID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT f6 FOREIGN KEY (startingStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT f7 FOREIGN KEY (endingStationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Passes (
    name INT NOT NULL,
    stationName VARCHAR(32) NOT NULL,
    cardinalNo INT NOT NULL,

    CONSTRAINT pk  PRIMARY KEY (name, stationName),
    CONSTRAINT fk1 FOREIGN KEY (name) REFERENCES TrackSection(name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (stationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CarInRoute (
    routeID INT NOT NULL,
    carID INT NOT NULL,
    cardinalNo INT NOT NULL,

    CONSTRAINT pk  PRIMARY KEY (routeID, carID),
    CONSTRAINT fk1 FOREIGN KEY (routeID) REFERENCES TrainRoute(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (carID) REFERENCES TrainCar(carID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TimeTable (
    routeID INT NOT NULL,
    stationName VARCHAR(32) NOT NULL,
    departureTime TIME,
    arrivalTime TIME,

    CONSTRAINT pk  PRIMARY KEY (routeID, stationName),
    CONSTRAINT fk1 FOREIGN KEY (routeID) REFERENCES TrainRoute(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (stationName) REFERENCES RailwayStation(stationName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS OrderForOccurrence (
    orderID INT NOT NULL,
    dateOfOccurrence DATE NOT NULL,
    routeID INT NOT NULL,
    numberOfTickets INT NOT NULL,

    CONSTRAINT pk  PRIMARY KEY (orderID, dateOfOccurrence, routeID),
    CONSTRAINT fk1 FOREIGN KEY (orderID) REFERENCES CustomerOrder(orderID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (dateOfOccurrence) REFERENCES TrainOccurrence(dateOfOccurrence)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk3 FOREIGN KEY (routeID) REFERENCES TrainOccurrence(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StartFromStationInDay(
    routeID INT NOT NULL,
    dayOfTheWeek DATE NOT NULL,
    CONSTRAINT pk PRIMARY KEY(routeID, dayOfTheWeek),
    CONSTRAINT fk1 FOREIGN KEY (routeID) REFERENCES TrainRoute(routeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (dayOfTheWeek) REFERENCES DaysOfTheWeek(dayOfTheWeek)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);