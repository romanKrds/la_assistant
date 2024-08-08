import os
import csv
import click
from la_assistant.models import *
from flask_migrate import Migrate
from .extensions import db


def populate_db():
    # populate vocabulary table with predefined data
    with open(os.path.join(os.path.dirname(__file__), 'word-list-de.csv'), 'r', newline='') as file:
        csv_reader = csv.reader(file, delimiter='\t')

        for line in csv_reader:
            vocab_item = Vocabulary(language='de', word_1=line[0], word_2=line[1], sentence=line[2])
            db.session.add(vocab_item)

        db.session.commit()


@click.command('populate-db')
def populate_db_command():
    """Clear the existing data and create new tables."""
    populate_db()
    click.echo('Populated the database with data.')


def init_app(app):
    db.init_app(app)
    Migrate(app, db)

    app.cli.add_command(populate_db_command)
