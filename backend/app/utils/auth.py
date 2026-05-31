from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User
from app.utils.response import error_response


def current_user():
    identity = get_jwt_identity()
    if identity is None:
        return None
    return User.query.get(int(identity))


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user or user.user_type not in roles:
                return error_response("Unauthorized access", 403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
