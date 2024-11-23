INSERT INTO rooms (id, name, size, beds, price, description)
VALUES
    (gen_random_uuid(), 'Oceanview Deluxe Room', 400, 1, 200.00, 'A stunning room with an ocean view.'),
    (gen_random_uuid(), 'Seaside Suite', 550, 2, 350.00, 'Spacious suite overlooking the seaside.'),
    (gen_random_uuid(), 'Family Room', 600, 3, 400.00, 'Perfect for families, with extra space.'),
    (gen_random_uuid(), 'Luxury Suite', 750, 1, 500.00, 'Luxury accommodations with premium amenities.'),
    (gen_random_uuid(), 'Honeymoon Penthouse', 1000, 1, 800.00, 'Private penthouse ideal for couples.');
