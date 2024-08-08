import os
from flask import Blueprint, request, g
from .auth import login_required
from la_assistant.extensions import db
from la_assistant.models import UserVocabulary, Vocabulary
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')


@bp.get('/list')
@login_required
def get_vocabulary_list():
    repetitions_number = os.getenv('REPETITIONS_TO_MEMORIZE_WORD_NUMBER')
    word_set_length = os.getenv('MEMORIZE_WORD_SET_LENGTH')

    UV_alias = aliased(UserVocabulary)

    user_vocabularies = db.session.query(
        Vocabulary.id,
        Vocabulary.language,
        Vocabulary.word_1,
        Vocabulary.word_2,
        Vocabulary.sentence,
        UV_alias.times_showed
    ).outerjoin(
        UV_alias,
        and_(
            Vocabulary.id == UV_alias.vocabulary_id,
            UV_alias.user_id == g.user.id
        )
    ).filter(
        or_(UV_alias.times_showed < repetitions_number, UV_alias.times_showed.is_(None))
    ).limit(word_set_length).all()

    user_vocabularies_dict = [
        {
            "id": uv[0],
            "language": uv[1],
            "word_1": uv[2],
            "word_2": uv[3],
            "sentence": uv[4],
            "times_showed": uv[5]
        } for uv in user_vocabularies
    ]

    return {"result": user_vocabularies_dict}, 200

@bp.get('/studied-list')
@login_required
def get_vocabulary_studied_list():
    repetitions_number = os.getenv('REPETITIONS_TO_MEMORIZE_WORD_NUMBER')
    word_set_length = os.getenv('MEMORIZE_WORD_SET_LENGTH')

    UV_alias = aliased(UserVocabulary)

    user_vocabularies = db.session.query(
        Vocabulary.id,
        Vocabulary.language,
        Vocabulary.word_1,
        Vocabulary.word_2,
        Vocabulary.sentence,
        UV_alias.times_reviewed
    ).outerjoin(
        UV_alias,
        and_(
            Vocabulary.id == UV_alias.vocabulary_id,
            UV_alias.user_id == g.user.id
        )
    ).filter(
        and_(
            or_(UV_alias.times_reviewed < repetitions_number, UV_alias.times_reviewed.is_(None)),
            UV_alias.times_showed > 0
        )
    ).limit(word_set_length).all()

    user_vocabularies_dict = [
        {
            "id": uv[0],
            "language": uv[1],
            "word_1": uv[2],
            "word_2": uv[3],
            "sentence": uv[4],
            "times_reviewed": uv[5]
        } for uv in user_vocabularies
    ]

    return {"result": user_vocabularies_dict}, 200


@bp.route('/user-progress', methods=['POST'])
@login_required
def user_progress():
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

    progress = UserVocabulary.query.filter(
        and_(
            UserVocabulary.vocabulary_id == vocabulary_id,
            UserVocabulary.user_id == user_id
        )
    ).first()

    if progress is None:
        add_user_progress_record(vocabulary_id, user_id)
    else:
        update_user_progress_record(progress, is_review)

    return {}, 200


def add_user_progress_record(vocabulary_id, user_id):
    times_showed = 1
    times_reviewed = 0

    user_progress_record = UserVocabulary(
        vocabulary_id=vocabulary_id,
        user_id=user_id,
        times_showed=times_showed,
        times_reviewed=times_reviewed
    )
    db.session.add(user_progress_record)
    db.session.commit()


def update_user_progress_record(progress, is_review):
    times_showed = progress.times_showed
    times_reviewed = progress.times_reviewed

    if is_review:
        times_reviewed += 1
    else:
        times_showed += 1

    progress.times_showed = times_showed
    progress.times_reviewed = times_reviewed

    db.session.commit()
