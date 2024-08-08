from la_assistant.extensions import db as _db
from la_assistant.database import populate_db
from sqlalchemy import inspect
from la_assistant.models import Vocabulary



def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_populate_db():
        Recorder.called = True

    monkeypatch.setattr('la_assistant.database.populate_db', fake_populate_db)
    result = runner.invoke(args=['populate-db'])
    assert 'Populated' in result.output
    assert Recorder.called


# The init_db function creates the needed tables in the database
def test_init_db_creates_tables(app, client):
    with app.app_context():
        inspector = inspect(_db.engine)
        tables = inspector.get_table_names()

        # verify
        assert 'user' in tables
        assert 'vocabulary' in tables
        assert 'user_vocabulary' in tables


# The populate_db function inserts data in to the 'vocabulary' table according to 'word-list-de.csv':
def test_init_db_inserts_data_from_word_list(app, client):
    with app.app_context():
        # Assuming this line is the first row from 'word-list-de.csv'
        first_line_csv = ('Zeit', 'Person', 'Die Zeit wartet auf keinen Menschen.')

        populate_db()
        # Fetch first row from db to verify
        first_row_db = Vocabulary.query.filter_by(language='de').order_by(Vocabulary.id).first()

        assert first_line_csv == (first_row_db.word_1, first_row_db.word_2, first_row_db.sentence)