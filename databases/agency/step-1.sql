-- Table: rooms
CREATE TABLE rooms (
    id UUID PRIMARY KEY, -- Unique identifier for each room
    name VARCHAR(255) NOT NULL, -- Room name
    size INTEGER NOT NULL, -- Room size in square feet
    beds INTEGER NOT NULL, -- Number of beds in the room
    price NUMERIC(10, 2) NOT NULL, -- Price per night
    description TEXT, -- Room description
    images JSONB, -- JSON array of image URLs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the room was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);

-- Table: room_availability
CREATE TABLE room_availability (
    id UUID PRIMARY KEY, -- Unique identifier for the availability entry
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE, -- Room being tracked
    start_date DATE NOT NULL, -- Start date of the availability period
    end_date DATE NOT NULL, -- End date of the availability period
    status VARCHAR(50) DEFAULT 'available', -- Status: 'available', 'booked', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Entry creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);


CREATE TABLE agencies (
    id UUID PRIMARY KEY, -- Unique identifier for the agency
    name VARCHAR(255) NOT NULL, -- Agency name
    token VARCHAR(255) NOT NULL UNIQUE, -- Authentication token
    description TEXT -- Additional information about the agency
);