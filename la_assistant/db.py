import os
import sqlite3
import csv

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # populate vocabulary table with predefined data
    with open(os.path.join(os.path.dirname(__file__), 'word-list-de.csv'), 'r', newline='') as file:
        csv_reader = csv.reader(file, delimiter='\t')

        for line in csv_reader:
            db.execute("INSERT INTO vocabulary (language, word_1, word_2, sentence) VALUES (?, ?, ?, ?)", ('de', *line))
            db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
