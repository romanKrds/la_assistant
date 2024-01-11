DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS mistake;

CREATE TABLE user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL,
    thread_id TEXT,
    token TEXT
);

CREATE TABLE mistake
(
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id                  INTEGER   NOT NULL,
    created_at               TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    language                 TEXT      NOT NULL,
    origin                   TEXT      NOT NULL,
    explanation              TEXT      NOT NULL,
    corrected_origin         TEXT      NOT NULL,
    times_showed             INTEGER   NOT NULL DEFAULT 0,
    times_reviewed           INTEGER   NOT NULL DEFAULT 0,
    times_reviewed_correctly INTEGER   NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user (id)
);