SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (2, 3), (1, 3));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (1, 2), (1, 3), (1, 4), (4, 5), (1, 6), (1, 7), (5, 8), (5, 9), (9, 10), (1, 11), (2, 12), (6, 13), (9, 14), (7, 15));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (3, 9), (2, 11), (1, 13), (2, 4), (3, 14), (1, 17), (2, 12), (2, 5), (2, 4), (2, 18), (1, 4), (2, 16), (2, 5), (3, 6), (3, 11), (3, 17), (2, 19), (2, 14), (2, 6), (2, 7), (1, 17), (3, 19), (2, 11), (1, 11), (1, 10), (1, 8), (2, 17), (2, 14), (3, 14), (2, 7), (2, 6), (2, 6), (2, 9), (3, 10), (3, 15), (2, 14), (3, 19), (1, 8), (3, 19), (2, 19));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (10, 18), (2, 19), (5, 19), (5, 18), (5, 18), (10, 19), (11, 19), (10, 19), (1, 19), (4, 19));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (2, 8), (2, 10), (3, 6), (3, 14), (3, 11), (2, 16), (1, 16), (3, 6), (3, 9), (3, 11), (2, 15), (3, 7), (2, 16), (2, 13), (1, 16));
SELECT GraphCountBipartiteMaximumMatching (from, to) FROM VALUES('from UInt64, to UInt64', (3, 8), (3, 9), (1, 9), (3, 9), (3, 5), (3, 8), (2, 4), (3, 8), (1, 7), (3, 7), (2, 6), (3, 10), (2, 8), (3, 4), (1, 9), (1, 4), (2, 7), (3, 6), (2, 8));