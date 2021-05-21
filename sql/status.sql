CREATE TABLE status (
    id                  TEXT    PRIMARY KEY,
    -- When the level was scraped.
    uploaded            INTEGER NOT NULL,
    -- Approval level.
    approval            INTEGER NOT NULL DEFAULT 0,
    -- Number of "likes".
    -- Not used yet.
    kudos               INTEGER NOT NULL DEFAULT 0,
);

CREATE TABLE user (
    id          TEXT        PRIMARY KEY,
    permission  INTEGER     DEFAULT 1
)