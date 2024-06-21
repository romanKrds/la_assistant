import os

from flask import Blueprint, request

from la_assistant.auth import login_required
from la_assistant.db import get_db

bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')


def get_vocabulary(query, fields):
    repetitions_number = os.getenv('REPETITIONS_TO_MEMORIZE_WORD_NUMBER')
    word_set_length = os.getenv('MEMORIZE_WORD_SET_LENGTH')

    db = get_db()
    items = db.execute(query, (repetitions_number, word_set_length, *fields)).fetchall()

    return {"result": [dict(x) for x in items]}, 200

@bp.get('/list')
@login_required
def get_vocabulary_list():
    return get_vocabulary(
        '''
            SELECT
                vocabulary.id,
                vocabulary.language,
                vocabulary.word_1,
                vocabulary.word_2,
                vocabulary.sentence,
                user_vocabulary.times_showed
            FROM vocabulary LEFT OUTER JOIN user_vocabulary ON vocabulary.id = user_vocabulary.vocabulary_id
            WHERE user_vocabulary.times_showed < ? OR user_vocabulary.times_showed isnull
            LIMIT ?
        ''',
        ()
    )


@bp.get('/studied-list')
@login_required
def get_vocabulary_studied_list():
    return get_vocabulary(
        '''
            SELECT
                vocabulary.id,
                vocabulary.language,
                vocabulary.word_1,
                vocabulary.word_2,
                vocabulary.sentence,
                user_vocabulary.times_reviewed
            FROM vocabulary LEFT OUTER JOIN user_vocabulary ON vocabulary.id = user_vocabulary.vocabulary_id
            WHERE (user_vocabulary.times_reviewed < ? OR user_vocabulary.times_reviewed isnull) AND user_vocabulary.times_showed > 0
            LIMIT ?
        ''',
        ()
    )


@bp.route('/user-progress', methods=['POST'])
@login_required
def user_progress():
    db = get_db()
    data = request.get_json()
    user_id = data.get('user_id')
    vocabulary_id = data.get('vocabulary_id')
    is_review = data.get('is_review')
    error = None

    if not user_id:
        error = "user_id is required"
    if not vocabulary_id:
        error = "vocabulary_id is required"

    if error is not None:
        return {"error": error}, 400

    progress = db.execute(
        'SELECT * from user_vocabulary WHERE vocabulary_id = ? AND user_id = ?',
        (vocabulary_id, user_id)
    ).fetchone()

    if progress is None:
        add_user_progress_record(db, vocabulary_id, user_id)
    else:
        update_user_progress_record(db, vocabulary_id, user_id, progress, is_review)

    return {}, 200


def add_user_progress_record(db, vocabulary_id, user_id):
    times_showed = 1
    times_reviewed = 0

    db.execute(
        'INSERT INTO user_vocabulary (vocabulary_id, user_id, times_showed, times_reviewed) VALUES (?, ?, ?, ?)',
        (vocabulary_id, user_id, times_showed, times_reviewed)
    )
    db.commit()


def update_user_progress_record(db, vocabulary_id, user_id, progress, is_review):
    times_showed = int(dict(progress).get('times_showed'))
    times_reviewed = int(dict(progress).get('times_reviewed'))

    if is_review:
        times_reviewed += 1
    else:
        times_showed += 1

    db.execute(
        'UPDATE user_vocabulary SET times_showed = ?, times_reviewed = ? WHERE vocabulary_id = ? AND user_id = ?',
        (times_showed, times_reviewed, vocabulary_id, user_id)
    )
    db.commit()
