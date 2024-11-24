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
    reservation_end_date DATE DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);


CREATE TABLE agencies (
    id UUID PRIMARY KEY, -- Unique identifier for the agency
    name VARCHAR(255) NOT NULL, -- Agency name
    token VARCHAR(255) NOT NULL UNIQUE, -- Authentication token
    description TEXT -- Additional information about the agency
);

CREATE OR REPLACE FUNCTION create_reservation(
    r_id UUID,
    r_start_date DATE,
    r_end_date DATE
) RETURNS TABLE (id UUID, room_id UUID, reservation_start_date DATE, reservation_end_date DATE) AS $$
BEGIN
    -- Perform the INSERT operation
    INSERT INTO reservations (id, room_id, reservation_start_date, reservation_end_date)
    VALUES (gen_random_uuid(), r_id, r_start_date, r_end_date)
    RETURNING reservations.id, reservations.room_id, reservations.reservation_start_date, reservations.reservation_end_date
    INTO id, room_id, reservation_start_date, reservation_end_date;

    -- Return the inserted data (from variables)
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION is_room_available(
    r_id UUID,
    start_date DATE,
    end_date DATE
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check for overlapping reservations
    RETURN NOT EXISTS (
        SELECT 1
        FROM reservations
        WHERE reservations.room_id = r_id
          AND reservations.reservation_start_date < end_date
          AND reservations.reservation_end_date > start_date
    );
END;
$$ LANGUAGE plpgsql;
