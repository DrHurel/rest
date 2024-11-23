INSERT INTO rooms (id, name, size, beds, price, description)
VALUES
    (gen_random_uuid(), 'Cozy Cabin Room', 300, 1, 150.00, 'Cozy cabin with mountain views.'),
    (gen_random_uuid(), 'Alpine View Room', 400, 2, 250.00, 'Room with an alpine view.'),
    (gen_random_uuid(), 'Family Suite', 650, 3, 350.00, 'Spacious suite for families.'),
    (gen_random_uuid(), 'Luxury Ski Suite', 800, 2, 500.00, 'Premium suite with ski-in access.'),
    (gen_random_uuid(), 'Presidential Lodge', 1200, 1, 1000.00, 'Exclusive lodge with breathtaking views.');
