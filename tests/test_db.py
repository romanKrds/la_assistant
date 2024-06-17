import sqlite3

import pytest
from la_assistant.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('la_assistant.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


# The init_db function creates the needed tables in the database
def test_init_db_creates_tables(app, client):
    with app.app_context():
        db = get_db()
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]

        # verify
        assert 'user' in tables
        assert 'mistake' in tables
        assert 'vocabulary' in tables
        assert 'user_vocabulary' in tables


# The init_db function inserts data in to the 'vocabulary' table according to 'word-list-de.csv':
def test_init_db_inserts_data_from_word_list(app, client):
    with app.app_context():
        db = get_db()

        # Assuming this line is the first row from 'word-list-de.csv'
        first_line_csv = ('Zeit', 'Person', 'Die Zeit wartet auf keinen Menschen.')

        # Fetch first row from db to verify
        first_row_db = db.execute(
            "SELECT word_1, word_2, sentence FROM vocabulary WHERE language = 'de' ORDER BY ID ASC LIMIT 1").fetchone()

        assert first_line_csv == tuple(first_row_db)