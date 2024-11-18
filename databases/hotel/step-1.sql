-- Create database (optional, depends on your setup)
CREATE DATABASE HotelManagement;

-- Use the database
USE HotelManagement;

-- Table for storing room information
CREATE TABLE Rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    size INT CHECK (size > 0), -- Size in square meters
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0), -- Price per night
    beds INT NOT NULL CHECK (beds > 0),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- Table for storing room images
CREATE TABLE RoomImages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES Rooms(id) ON DELETE CASCADE
);

-- Table for storing bookings
CREATE TABLE Bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES Rooms(id) ON DELETE CASCADE
);

-- Insert sample data into Hotels table
INSERT INTO Hotels (name, address, rating) VALUES
('Hotel Sunrise', '123 Main Street, Sunshine City', 4.5),
('Ocean View Resort', '456 Beach Avenue, Coastal Town', 4.7),
('Mountain Lodge', '789 Peak Road, Highland Valley', 4.2);

-- Insert sample data into Rooms table
INSERT INTO Rooms (hotel_id, name, size, price, beds, is_available) VALUES
(1, 'Deluxe Suite', 45, 200.00, 2, TRUE),
(1, 'Standard Room', 25, 100.00, 1, TRUE),
(2, 'Oceanfront Room', 30, 150.00, 2, TRUE),
(3, 'Mountain Cabin', 35, 120.00, 2, FALSE);

-- Insert sample data into RoomImages table
INSERT INTO RoomImages (room_id, url, description) VALUES
(1, 'https://example.com/deluxe_suite.jpg', 'A spacious deluxe suite with a king bed and city view.'),
(2, 'https://example.com/standard_room.jpg', 'A cozy standard room with modern amenities.'),
(3, 'https://example.com/oceanfront_room.jpg', 'A room with an oceanfront view and private balcony.'),
(4, 'https://example.com/mountain_cabin.jpg', 'A rustic cabin with a fireplace and mountain view.');

-- Insert sample data into Bookings table
INSERT INTO Bookings (room_id, customer_name, start_date, end_date, total_price) VALUES
(1, 'John Doe', '2024-12-01', '2024-12-05', 800.00),
(2, 'Jane Smith', '2024-12-10', '2024-12-12', 200.00);

-- Query data (example)
-- Get all rooms with their hotel name and availability
SELECT
    r.id AS room_id,
    r.name AS room_name,
    r.size AS room_size,
    r.price AS room_price,
    r.beds AS room_beds,
    r.is_available AS available,
    h.name AS hotel_name,
    h.address AS hotel_address
FROM
    Rooms r
JOIN
    Hotels h ON r.hotel_id = h.id;
