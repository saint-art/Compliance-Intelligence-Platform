PRAGMA foreign_keys = ON;

-- ============================================================
-- PERSONS
-- ============================================================

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

    entity_type TEXT NOT NULL DEFAULT 'PERSON',

    is_pep INTEGER NOT NULL DEFAULT 0,
    is_sanctioned INTEGER NOT NULL DEFAULT 0,

    risk_level TEXT NOT NULL DEFAULT 'LOW',

    confidence_score REAL NOT NULL DEFAULT 0,

    primary_source TEXT,

    last_verified TEXT,

    entity_status TEXT NOT NULL DEFAULT 'ACTIVE',

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    political_party TEXT,
    constituency TEXT,
    county TEXT,

    profile_url TEXT,
    image_url TEXT,

    status TEXT
);


-- ============================================================
-- INSTITUTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS institutions (

    institution_id INTEGER PRIMARY KEY AUTOINCREMENT,

    institution_name TEXT NOT NULL UNIQUE,

    category TEXT,
    country TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);


-- ============================================================
-- POSITIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS positions (

    position_id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL UNIQUE,

    description TEXT,
    category TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);


-- ============================================================
-- SOURCE DOCUMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS source_documents (

    document_id TEXT PRIMARY KEY,

    source_name TEXT NOT NULL,

    source_type TEXT,

    source_url TEXT,

    external_id TEXT,

    title TEXT,

    document_type TEXT,

    published_at TEXT,

    modified_at TEXT,

    collected_at TEXT,

    raw_path TEXT,

    checksum TEXT UNIQUE,

    status TEXT NOT NULL DEFAULT 'COLLECTED'
);


-- ============================================================
-- PERSON-POSITION RELATIONSHIPS
-- ============================================================

CREATE TABLE IF NOT EXISTS person_positions (

    person_position_id TEXT PRIMARY KEY,

    person_id INTEGER NOT NULL,

    position_id INTEGER NOT NULL,

    institution_id INTEGER NOT NULL,

    source_document_id TEXT NOT NULL,

    start_date TEXT,

    end_date TEXT,

    is_current INTEGER NOT NULL DEFAULT 1,

    confidence_score REAL NOT NULL DEFAULT 100,

    created_at TEXT NOT NULL,

    updated_at TEXT NOT NULL,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
        ON DELETE CASCADE,

    FOREIGN KEY (position_id)
        REFERENCES positions(position_id)
        ON DELETE CASCADE,

    FOREIGN KEY (institution_id)
        REFERENCES institutions(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (source_document_id)
        REFERENCES source_documents(document_id)
        ON DELETE CASCADE
);


-- ============================================================
-- GENERIC SOURCES
-- ============================================================

CREATE TABLE IF NOT EXISTS sources (

    source_id INTEGER PRIMARY KEY AUTOINCREMENT,

    person_id INTEGER,

    source_name TEXT,

    source_url TEXT,

    source_type TEXT,

    trust_score REAL,

    collected_at TEXT,

    last_verified TEXT,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
        ON DELETE CASCADE
);


-- ============================================================
-- ALIASES
-- ============================================================

CREATE TABLE IF NOT EXISTS aliases (

    alias_id INTEGER PRIMARY KEY AUTOINCREMENT,

    person_id INTEGER,

    alias TEXT,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
        ON DELETE CASCADE
);


-- ============================================================
-- SOURCE RUNS
-- ============================================================

CREATE TABLE IF NOT EXISTS source_runs (

    run_id INTEGER PRIMARY KEY AUTOINCREMENT,

    collector_name TEXT,

    source_name TEXT,

    records_found INTEGER DEFAULT 0,

    inserted INTEGER DEFAULT 0,

    updated INTEGER DEFAULT 0,

    skipped INTEGER DEFAULT 0,

    started_at TEXT,

    finished_at TEXT,

    status TEXT
);


-- ============================================================
-- ETL RUNS
-- ============================================================

CREATE TABLE IF NOT EXISTS etl_runs (

    run_id INTEGER PRIMARY KEY AUTOINCREMENT,

    collector TEXT,

    records_found INTEGER DEFAULT 0,

    inserted INTEGER DEFAULT 0,

    updated INTEGER DEFAULT 0,

    started_at TEXT,

    finished_at TEXT,

    status TEXT
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_person_name
ON persons(full_name);

CREATE INDEX IF NOT EXISTS idx_person_pep
ON persons(is_pep);

CREATE INDEX IF NOT EXISTS idx_person_source
ON persons(primary_source);

CREATE INDEX IF NOT EXISTS idx_position_title
ON positions(title);

CREATE INDEX IF NOT EXISTS idx_institution_name
ON institutions(institution_name);

CREATE INDEX IF NOT EXISTS idx_person_positions_person
ON person_positions(person_id);

CREATE INDEX IF NOT EXISTS idx_person_positions_position
ON person_positions(position_id);

CREATE INDEX IF NOT EXISTS idx_person_positions_institution
ON person_positions(institution_id);

CREATE INDEX IF NOT EXISTS idx_person_positions_document
ON person_positions(source_document_id);