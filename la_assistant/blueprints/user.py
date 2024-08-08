from flask import Blueprint, g
from .auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('info')
@login_required
def get_user_info():
    user = g.user

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200
