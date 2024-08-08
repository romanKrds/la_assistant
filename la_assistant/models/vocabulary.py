from la_assistant.extensions import db


class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language = db.Column(db.String(8), nullable=False)
    sentence = db.Column(db.String(256), nullable=False)
    word_1 = db.Column(db.String(100), nullable=False)
    word_2 = db.Column(db.String(100), nullable=False)