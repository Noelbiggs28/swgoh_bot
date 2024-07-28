-- No need to create a database in SQLite, just connect to the database file
DROP TABLE IF EXISTS PLATOONS;
DROP TABLE IF EXISTS PLAYERS;
DROP TABLE IF EXISTS PLAYERUNITS;
-- Create tables
CREATE TABLE PLATOONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase INTEGER,
    planet VARCHAR(50),
    operations INTEGER,
    character_name VARCHAR(50)
);

CREATE TABLE PLAYERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name VARCHAR(50),
    ally_code VARCHAR(50)
);

CREATE TABLE PLAYERUNITS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name VARCHAR(50),
    character_name VARCHAR(50),
    relic INTEGER,
    rarity INTEGER
);
