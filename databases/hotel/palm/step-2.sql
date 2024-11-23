INSERT INTO rooms (id, name, size, beds, price, description)
VALUES
    (gen_random_uuid(), 'Garden View Villa', 500, 1, 300.00, 'Villa with beautiful garden views.'),
    (gen_random_uuid(), 'Ocean Breeze Villa', 600, 2, 450.00, 'Villa with a fresh ocean breeze.'),
    (gen_random_uuid(), 'Luxury Pool Villa', 800, 2, 600.00, 'Villa with a private pool.'),
    (gen_random_uuid(), 'Family Retreat Villa', 1000, 3, 800.00, 'Spacious villa for large families.'),
    (gen_random_uuid(), 'Presidential Retreat Villa', 1500, 1, 1200.00, 'Exclusive retreat for ultimate privacy.');
