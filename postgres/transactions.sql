-- Mock values to be inserted into the Transaction table
--------------------------------------------------------
-- Transaction table has foreign key dependency with the user_info table.
-- Hence, we require two valid users.
-- Considering user ids 47 and 48 exists;
INSERT into TRANSACTION values(100, 47, 48, 10, 'Visa', 1, 't', NOW(), 'abc', NOW(), 'abc');
INSERT into TRANSACTION values(101, 47, 48, 20, 'Mastercard', 3, 'f', NOW()-INTERVAL '1 DAY', 'abc', NOW()-INTERVAL '1 DAY', 'abc');
INSERT into TRANSACTION values(102, 47, 48, 30, 'Amex', 2, 'f', NOW()-INTERVAL '2 DAY', 'abc', NOW()-INTERVAL '2 DAY', 'abc');
INSERT into TRANSACTION values(103, 47, 48, 9, 'Visa', 1, 'f', NOW()-INTERVAL '4 DAY', 'abc', NOW()-INTERVAL '4 DAY', 'abc');
INSERT into TRANSACTION values(104, 47, 48, 9, 'Mastercard', 3, 't', NOW()-INTERVAL '5 DAY', 'abc', NOW()-INTERVAL '5 DAY', 'abc');
INSERT into TRANSACTION values(105, 47, 48, 132, 'Amex', 2, 't', NOW()-INTERVAL '7 DAY', 'abc', NOW()-INTERVAL '7 DAY', 'abc');
INSERT into TRANSACTION values(106, 47, 48, 12, 'Visa', 1, 't', NOW()-INTERVAL '8 DAY', 'abc', NOW()-INTERVAL '8 DAY', 'abc');
-- Filter the start and end dates for the user 47 (payer_id) as 04/11/2023 and 04/21/2023