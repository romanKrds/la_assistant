DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS mistake;
DROP TABLE IF EXISTS vocabulary;
DROP TABLE IF EXISTS user_vocabulary;

CREATE TABLE user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL,
    thread_id TEXT,
    token     TEXT
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

CREATE TABLE vocabulary
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    sentence TEXT NOT NULL,
    word_1   TEXT NOT NULL,
    word_2   TEXT NOT NULL
);

CREATE TABLE user_vocabulary
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    vocabulary_id INTEGER NOT NULL,
    user_id       INTEGER NOT NULL,
    times_showed  INTEGER NOT NULL,
    times_reviewed  INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id)
);
