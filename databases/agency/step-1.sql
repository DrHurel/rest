-- Create the database for Agency 1
CREATE DATABASE Agency1_Service_Web;

-- Switch to the database
USE Agency1_Service_Web;

-- Create the Reservations table
CREATE TABLE Reservations (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    OfferID INT NOT NULL,
    HotelID INT NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    CustomerContact VARCHAR(255) NOT NULL,
    ReservationDate DATETIME NOT NULL,
    Status VARCHAR(50) NOT NULL,
    ReferenceNumber VARCHAR(255) UNIQUE NOT NULL
);

-- Create the Hotels table
CREATE TABLE Hotels (
    HotelID INT AUTO_INCREMENT PRIMARY KEY,
    HotelURL VARCHAR(255),
);


-- Populate the Hotels table
INSERT INTO Hotels (HotelName, Address, Phone)
VALUES
('Hotel Paradise', 'localhost:3000'),
('Sunny Retreat', 'localhost:3001'),
('Mountain View Inn', 'localhost:3002');

-- Populate the Reservations table
INSERT INTO Reservations (OfferID, HotelID, CustomerName, CustomerContact, ReservationDate, Status, ReferenceNumber)
VALUES
(1, 1, 'John Doe', 'john.doe@example.com', '2024-12-01 14:30:00', 'Confirmed', 'RES123'),
(2, 2, 'Jane Smith', 'jane.smith@example.com', '2024-12-01 15:00:00', 'Confirmed', 'RES124'),
(3, 1, 'Alice Brown', 'alice.brown@example.com', '2024-12-02 10:00:00', 'Pending', 'RES125');
