import functools
from datetime import datetime

from flask import (
    Blueprint, g, abort, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from la_assistant.models import User
from la_assistant.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    token = session.get('token') or request.headers.get('Authorization')

    if token is None:
        g.user = None
    else:
        g.user = User.query.filter_by(token=token).first()


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


def validate_user_input(data):
    username = data.get('username')
    password = data.get('password')
    if not username:
        return 'Username is required.'
    elif not password:
        return 'Password is required.'


@bp.post('/register')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    error = validate_user_input(data)

    if error is None:
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is not None:
            error = f"User {username} is already registered."
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            return {}, 200

    return {"error": error}, 400


@bp.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    error = validate_user_input(data)

    if error is None:
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            token = get_token(user.password)
            user.token = token
            db.session.commit()
            session.clear()
            session['token'] = token

            return {"token": token}, 200

    return {"error": error}, 400


@bp.route('/logout')
@login_required
def logout():
    user = User.query.filter_by(username=g.user.username).first()
    user.token = None
    db.session.commit()
    session.clear()
    return {}, 200


def get_token(salt):
    date = datetime.now().timestamp()
    return generate_password_hash(salt + str(date)).split(':').pop()
