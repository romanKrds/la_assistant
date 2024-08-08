from la_assistant.extensions import db


class UserVocabulary(db.Model):
    __tablename__ = 'user_vocabulary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    times_showed = db.Column(db.Integer, nullable=False)
    times_reviewed = db.Column(db.Integer, nullable=False)

    # relationships
    user = db.relationship('User', backref=db.backref('user_vocabularies', lazy=True))
