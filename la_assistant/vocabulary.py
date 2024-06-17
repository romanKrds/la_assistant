import os

from flask import Blueprint, request

from la_assistant.auth import login_required
from la_assistant.db import get_db

bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')


@bp.get('/list')
@login_required
def get_vocabulary_list():
    repetitions_number = os.getenv('REPETITIONS_TO_MEMORIZE_WORD_NUMBER')
    word_set_length = os.getenv('MEMORIZE_WORD_SET_LENGTH')

    db = get_db()
    items = db.execute(
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
        (repetitions_number, word_set_length)
    ).fetchall()

    return {"result": [dict(x) for x in items]}, 200


@bp.route('/user-progress', methods=['POST'])
@login_required
def user_progress():
    db = get_db()
    data = request.get_json()
    user_id = data.get('user_id')
    vocabulary_id = data.get('vocabulary_id')
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
        times_showed = 1
        db.execute(
            'INSERT INTO user_vocabulary (vocabulary_id, user_id, times_showed) VALUES (?, ?, ?)',
            (vocabulary_id, user_id, times_showed)
        )
        db.commit()

        return {}, 200

    times_showed = int(dict(progress).get('times_showed')) + 1
    db.execute(
        'UPDATE user_vocabulary SET times_showed = ? WHERE vocabulary_id = ? AND user_id = ?',
        (times_showed, vocabulary_id, user_id)
    )
    db.commit()

    return {}, 200

