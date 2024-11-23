INSERT INTO rooms (id, name, size, beds, price, description)
VALUES
    (gen_random_uuid(), 'Standard Room', 300, 1, 100.00, 'Comfortable room in the city.'),
    (gen_random_uuid(), 'Executive Room', 400, 1, 200.00, 'Premium room with city views.'),
    (gen_random_uuid(), 'Deluxe Suite', 500, 2, 300.00, 'Spacious suite for extra comfort.'),
    (gen_random_uuid(), 'Family Suite', 700, 3, 400.00, 'Suite ideal for families.'),
    (gen_random_uuid(), 'Penthouse Suite', 1200, 1, 800.00, 'Luxurious penthouse with skyline views.');
