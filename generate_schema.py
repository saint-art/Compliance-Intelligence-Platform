from pathlib import Path

schema = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (

    person_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    first_name TEXT,

    middle_name TEXT,

    last_name TEXT,

    gender TEXT,

    nationality TEXT,

    country TEXT,

    date_of_birth TEXT,

    confidence_score REAL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS institutions (

    institution_id INTEGER PRIMARY KEY AUTOINCREMENT,

    institution_name TEXT UNIQUE,

    category TEXT,

    country TEXT

);

CREATE TABLE IF NOT EXISTS positions (

    position_id INTEGER PRIMARY KEY AUTOINCREMENT,

    person_id INTEGER,

    institution_id INTEGER,

    title TEXT,

    start_date TEXT,

    end_date TEXT,

    status TEXT,

    FOREIGN KEY(person_id)

        REFERENCES persons(person_id),

    FOREIGN KEY(institution_id)

        REFERENCES institutions(institution_id)

);

CREATE TABLE IF NOT EXISTS sources (

    source_id INTEGER PRIMARY KEY AUTOINCREMENT,

    person_id INTEGER,

    source_name TEXT,

    source_url TEXT,

    trust_score REAL,

    last_verified TEXT,

    FOREIGN KEY(person_id)

        REFERENCES persons(person_id)

);

CREATE TABLE IF NOT EXISTS aliases (

    alias_id INTEGER PRIMARY KEY AUTOINCREMENT,

    person_id INTEGER,

    alias TEXT,

    FOREIGN KEY(person_id)

        REFERENCES persons(person_id)

);

CREATE TABLE IF NOT EXISTS etl_runs (

    run_id INTEGER PRIMARY KEY AUTOINCREMENT,

    collector TEXT,

    records_found INTEGER,

    inserted INTEGER,

    updated INTEGER,

    started_at TEXT,

    finished_at TEXT,

    status TEXT

);

CREATE INDEX idx_person_name
ON persons(full_name);

CREATE INDEX idx_position_person
ON positions(person_id);

CREATE INDEX idx_source_person
ON sources(person_id);
"""

Path("database/schema.sql").write_text(schema)

print("database/schema.sql generated successfully.")
