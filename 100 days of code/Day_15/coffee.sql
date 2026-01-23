CREATE TABLE IF NOT EXISTS coffee(
    coffee_name     TEXT NOT NULL UNIQUE,
    water_required  INTEGER,
    coffee_required INTEGER,
    milk_required   INTEGER,
    price           REAL NOT NULL

);

CREATE TABLE IF NOT EXISTS resources(
    water  INTEGER DEFAULT 0,
    coffee INTEGER DEFAULT 0,
    milk   INTEGER DEFAULT 0,
    money  REAL    DEFAULT 0.0
);