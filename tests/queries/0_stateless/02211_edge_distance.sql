SELECT edgeDistance(11, 7) (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13));
SELECT edgeDistance(1, 15) (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17));
SELECT edgeDistance(3, 10) (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (6, 7), (1, 8), (3, 9), (6, 10), (8, 11));
SELECT edgeDistance(16, 8) (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (5, 3), (14, 12), (15, 4), (12, 9), (6, 3), (15, 7), (10, 17), (9, 4), (2, 3), (15, 13), (4, 16), (10, 16), (8, 2), (3, 16), (11, 10));
SELECT edgeDistance(8, 12) (from, to) FROM VALUES('from UInt64, to UInt64', (12, 12), (16, 17), (2, 15), (14, 10), (12, 1), (18, 18), (7, 19), (9, 11), (8, 3), (8, 9), (8, 12));
SELECT edgeDistance(4, 8) (from, to) FROM VALUES('from UInt64, to UInt64', (12, 14), (14, 7), (8, 14), (6, 7), (9, 15), (9, 7), (9, 10), (2, 4), (10, 11), (11, 5), (1, 15), (3, 13), (3, 12), (7, 2));