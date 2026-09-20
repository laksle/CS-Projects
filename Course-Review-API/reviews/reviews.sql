DROP TABLE IF EXISTS reviews;
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    comment TEXT,
    UNIQUE (user_id, course_id)
);