-- Create Users table
CREATE TABLE Users (
    id          INTEGER PRIMARY KEY NOT NULL,
    username    TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    last_login  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);