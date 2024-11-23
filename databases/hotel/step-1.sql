-- Table: rooms
CREATE TABLE rooms (
    id UUID PRIMARY KEY, -- Unique identifier for each room
    name VARCHAR(255) NOT NULL, -- Room name
    size INTEGER NOT NULL, -- Room size in square feet
    beds INTEGER NOT NULL, -- Number of beds in the room
    price NUMERIC(10, 2) NOT NULL, -- Price per night
    description TEXT -- Room description
);

-- Table: room_availability
CREATE TABLE reservations (
    id UUID PRIMARY KEY, -- Unique identifier for the availability entry
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE, -- Room being tracked
    reservation_start_date DATE DEFAULT CURRENT_TIMESTAMP, -- Entry creation timestamp
    reservations_end_date DATE DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);


CREATE TABLE agencies (
    id UUID PRIMARY KEY, -- Unique identifier for the agency
    name VARCHAR(255) NOT NULL, -- Agency name
    token VARCHAR(255) NOT NULL UNIQUE, -- Authentication token
    description TEXT -- Additional information about the agency
);