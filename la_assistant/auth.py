import functools
from datetime import datetime

from flask import (
    Blueprint, g, abort, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from la_assistant.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    token = session.get('token') or request.args.get('token')

    if token is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE token = ?', (token,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(401, 'Unauthorized')

        return view(**kwargs)

    return wrapped_view

def async_login_required(view):
    @functools.wraps(view)
    async def wrapped_view(**kwargs):
        if g.user is None:
            abort(401, 'Unauthorized')

        return await view(**kwargs)

    return wrapped_view


@bp.post('/register')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    error = None

    if not username:
        error = 'Username is required'
    elif not password:
        error = 'Password is required'

    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
        except db.IntegrityError:
            error = f'User {username} is already registered'
        else:
            return {}, 200

    return {"error": error}, 400


@bp.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        token = get_token(user['password'])
        db.execute(
            'UPDATE user SET token = ? WHERE username = ?', (token, username)
        )
        db.commit()
        session.clear()
        session['token'] = token
        return {"token": token}, 200

    return {"error": error}, 400


@bp.route('/logout')
@login_required
def logout():
    db = get_db()
    db.execute(
        'UPDATE user SET token = NULL WHERE username = ?', (g.user['username'],)
    )
    db.commit()
    session.clear()
    return {}, 200


def get_token(salt):
    date = datetime.now().timestamp()
    return generate_password_hash(salt + str(date)).split(':').pop()
