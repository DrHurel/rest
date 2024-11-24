CREATE TABLE hotels (
    hotel_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    rooms_margins DECIMAL(10,3) NOT NULL
);

CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY,
    hotel_id UUID REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(150) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    reservation_status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


