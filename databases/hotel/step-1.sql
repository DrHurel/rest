-- Create the database for Hotel 1
CREATE DATABASE Hotel1_Service_Web;

-- Switch to the database
USE Hotel1_Service_Web;

-- Create the Agencies table
CREATE TABLE Agencies (
    AgencyID INT AUTO_INCREMENT PRIMARY KEY,
    AgencyName VARCHAR(255) NOT NULL,
    Login VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Create the RoomOffers table
CREATE TABLE RoomOffers (
    OfferID INT AUTO_INCREMENT PRIMARY KEY,
    RoomType VARCHAR(50) NOT NULL,
    NumBeds INT NOT NULL,
    AvailableDate DATE NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    AgencyID INT NOT NULL,
    IsBooked BOOLEAN DEFAULT FALSE, -- Indicates if the offer is booked
    FOREIGN KEY (AgencyID) REFERENCES Agencies(AgencyID) ON DELETE CASCADE
);

-- Create the Reservations table
CREATE TABLE Reservations (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    OfferID INT NOT NULL,
    AgencyID INT NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    CustomerContact VARCHAR(255) NOT NULL,
    ReservationDate DATETIME NOT NULL,
    Status VARCHAR(50) NOT NULL,
    ReferenceNumber VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (OfferID) REFERENCES RoomOffers(OfferID) ON DELETE CASCADE,
    FOREIGN KEY (AgencyID) REFERENCES Agencies(AgencyID) ON DELETE CASCADE
);

-- Populate the Agencies table
INSERT INTO Agencies (AgencyName, Login, Password)
VALUES
('TravelEase', 'travels1', 'password123'),
('HolidayHub', 'holiday2', 'securepass'),
('WorldExplorer', 'world3', 'explorerpass');

-- Populate the RoomOffers table
INSERT INTO RoomOffers (RoomType, NumBeds, AvailableDate, Price, AgencyID, IsBooked)
VALUES
('Single Room', 1, '2024-12-01', 50.00, 1, FALSE),
('Double Room', 2, '2024-12-01', 80.00, 1, FALSE),
('Family Suite', 4, '2024-12-01', 150.00, 2, FALSE),
('Double Room', 2, '2024-12-02', 85.00, 3, FALSE),
('Single Room', 1, '2024-12-02', 55.00, 3, FALSE),
('Family Suite', 4, '2024-12-03', 160.00, 2, FALSE);
