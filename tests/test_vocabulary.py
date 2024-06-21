from unittest.mock import patch
import pytest
from la_assistant.db import get_db


# should skip items that was memorized by user
@patch('os.getenv')
def test_get_vocabulary_list(mock_getenv, client, auth):
    mock_getenv.side_effect = lambda key: {
        'REPETITIONS_TO_MEMORIZE_WORD_NUMBER': 3,
        'MEMORIZE_WORD_SET_LENGTH': 1
    }.get(key)

    auth.login()
    response = client.get('/vocabulary/list')

    assert response.status_code == 200
    assert response.json == {
        "result": [
            {
                'id': 2,
                'language': 'de',
                'sentence': 'Dieses Jahr habe ich einen neuen Weg zum Erfolg gefunden.',
                'times_showed': 0,
                'word_1': 'Jahr',
                'word_2': 'Weg'
            },
        ]
    }


# should skip items that was memorized by user during review
@patch('os.getenv')
def test_get_vocabulary_studied_list(mock_getenv, client, auth):
    mock_getenv.side_effect = lambda key: {
        'REPETITIONS_TO_MEMORIZE_WORD_NUMBER': 3,
        'MEMORIZE_WORD_SET_LENGTH': 1
    }.get(key)

    auth.login()
    response = client.get('/vocabulary/studied-list')

    assert response.status_code == 200
    assert response.json == {
        "result": [
            {
                'id': 2,
                'language': 'de',
                'sentence': 'Dieses Jahr habe ich einen neuen Weg zum Erfolg gefunden.',
                'times_reviewed': 0,
                'word_1': 'Jahr',
                'word_2': 'Weg'
            },
        ]
    }


def test_get_vocabulary_empty_studied_list(app, auth, client):
    auth.login()

    with app.app_context():
        db = get_db()
        db.execute(
            'DELETE FROM user_vocabulary'
        )
        db.commit()

    response = client.get('/vocabulary/studied-list')

    assert response.status_code == 200
    assert response.json == {
        "result": []
    }


@pytest.mark.parametrize(('user_id', 'vocabulary_id', 'message'), (
    ('', '1', 'user_id is required'),
    (1, '', 'vocabulary_id is required'),
))
def test_post_user_no_data_progress(client, auth, user_id, vocabulary_id, message):
    auth.login()

    response = client.post('/vocabulary/user-progress', json={"user_id": user_id, "vocabulary_id": vocabulary_id})

    assert message in response.json.get('error')


def get_user_progress(app, user_id, vocabulary_id):
    with app.app_context():
        return get_db().execute(
            "SELECT * FROM user_vocabulary WHERE user_id = ? AND vocabulary_id = ?", (user_id, vocabulary_id)
        ).fetchone()


# should add progress record if no progress for the vocabulary item exist
def test_post_user_progress(client, app, auth):
    user_id = 1
    vocabulary_id = 3
    assert get_user_progress(app, user_id, vocabulary_id) is None

    auth.login()
    response = client.post('/vocabulary/user-progress', json={"user_id": user_id, "vocabulary_id": vocabulary_id})

    assert response.status_code == 200
    assert get_user_progress(app, user_id, vocabulary_id) is not None


# should update existing progress record
def test_update_user_progress(client, app, auth):
    user_id = 1
    vocabulary_id = 2
    times_showed = dict(get_user_progress(app, user_id, vocabulary_id)).get('times_showed')

    auth.login()
    response = client.post('/vocabulary/user-progress', json={"user_id": user_id, "vocabulary_id": vocabulary_id})

    assert response.status_code == 200
    assert dict(get_user_progress(app, user_id, vocabulary_id)).get('times_showed') == times_showed + 1


# should update times_reviewed property if corresponding flag is provided
def test_update_times_reviewed_prop(app, client, auth):
    user_id = 1
    vocabulary_id = 2
    times_reviewed = dict(get_user_progress(app, user_id, vocabulary_id)).get('times_reviewed')

    auth.login()
    response = client.post('/vocabulary/user-progress', json={"user_id": user_id, "vocabulary_id": vocabulary_id, "is_review": True})

    assert response.status_code == 200
    assert dict(get_user_progress(app, user_id, vocabulary_id)).get('times_reviewed') == times_reviewed + 1