-- ##########################
--          TABLES
-- ##########################

-- Persistent data related to a level.
CREATE TABLE status (
    id                  TEXT    PRIMARY KEY,
    -- When the level was scraped.
    uploaded            INTEGER NOT NULL,
    -- Approval level.
    approval            INTEGER NOT NULL DEFAULT 0,
    -- Number of "likes".
    -- Not used yet.
    kudos               INTEGER NOT NULL DEFAULT 0,
    -- Difficulty, community-based, 1-20 scale.
    -- Not used yet.
    piu_difficulty      REAL NOT NULL DEFAULT 10.0,
    -- text that can appear regarding the approval level.
    -- for instance, this might show the reason a level has a star ("comp 8 winner"), or why a level was rejected ("oneshots incorrectly cued")
    approval_message    TEXT
);

-- Data directly from vitals.
CREATE TABLE level (
    id              TEXT    REFERENCES status(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    artist          TEXT    NOT NULL,
    song            TEXT    NOT NULL,
    difficulty      INTEGER NOT NULL,
    seizure_warning INTEGER NOT NULL,
    description     TEXT    NOT NULL,
    max_bpm         REAL    NOT NULL,
    min_bpm         REAL    NOT NULL,
    last_updated    INTEGER NOT NULL, -- unix timestamp.
    single_player   INTEGER NOT NULL, -- 0 = false, 1 = true
    two_player      INTEGER NOT NULL,
    thumb           TEXT    DEFAULT NULL,
    url             TEXT    DEFAULT NULL,  -- Given url, may be null.
    url2            TEXT    NOT NULL, -- Rehosted url, always exists.
    icon            TEXT    DEFAULT NULL,
    hue             REAL    NOT NULL,
    has_classics    INTEGER NOT NULL, -- 0 = false, 1 = true
    has_oneshots    INTEGER NOT NULL, -- 0 = false, 1 = true
    has_squareshots INTEGER NOT NULL, -- 0 = false, 1 = true
    has_swing       INTEGER NOT NULL, -- 0 = false, 1 = true
    has_freetimes   INTEGER NOT NULL, -- 0 = false, 1 = true
    has_holds       INTEGER NOT NULL, -- 0 = false, 1 = true
    source_id       TEXT    NOT NULL,
    source_iid      TEXT    NOT NULL,
    PRIMARY KEY (id)
);

-- level tags, which are just strings. these are from the rdzip, so we don't make any more assumptions
CREATE TABLE level_tag (
    id      TEXT    REFERENCES level(id) ON DELETE CASCADE,
    tag     TEXT    NOT NULL,
    seq     INTEGER NOT NULL, -- index of this tag
    primary key (id, tag, seq)
);

-- level authors
CREATE TABLE level_author (
    id      TEXT    REFERENCES level(id) ON DELETE CASCADE,
    author  TEXT    NOT NULL,
    seq     INTEGER NOT NULL, -- index of this tag
    primary key (id, author, seq)
);

CREATE VIEW levels
AS
SELECT * FROM level INNER JOIN status ON level.id = status.id;

-- Search.
CREATE VIRTUAL TABLE ft USING fts5(artist, song, description, content=level, content_rowid=_rowid_);

-- Triggers to keep the FTS index up to date.
CREATE TRIGGER level_ai AFTER INSERT ON level BEGIN
  INSERT INTO ft(rowid, artist, song, description) VALUES (new._rowid_, new.artist, new.song, new.description);
END;
CREATE TRIGGER level_ad AFTER DELETE ON level BEGIN
  INSERT INTO ft(ft, rowid, artist, song, description) VALUES ('delete', old._rowid_, old.artist, old.song, old.description);
END;
CREATE TRIGGER level_au AFTER UPDATE ON level BEGIN
  INSERT INTO ft(ft, rowid, artist, song, description) VALUES ('delete', old._rowid_, old.artist, old.song, old.description);
  INSERT INTO ft(rowid, artist, song, description) VALUES (new._rowid_, new.artist, new.song, new.description);
END;