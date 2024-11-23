INSERT INTO rooms (id, name, size, beds, price, description)
VALUES
    (gen_random_uuid(), 'Classic Queen Room', 350, 1, 150.00, 'Classic room with a queen bed.'),
    (gen_random_uuid(), 'Superior Double Room', 450, 2, 200.00, 'Superior room with double beds.'),
    (gen_random_uuid(), 'Junior Suite', 550, 1, 300.00, 'Junior suite with elegant decor.'),
    (gen_random_uuid(), 'Luxury Courtyard Suite', 700, 1, 500.00, 'Suite with a private courtyard.'),
    (gen_random_uuid(), 'Presidential Suite', 1000, 1, 1000.00, 'Top-tier suite with royal features.');
