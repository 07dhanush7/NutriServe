from datetime import datetime, timedelta
from secrets import token_urlsafe

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.payment_notification import TokenBlocklist
from app.models.user import User
from app.utils.response import error_response, success_response
from app.utils.validators import is_valid_email, require_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["full_name", "email", "password"])
    if missing:
        return error_response(missing, 400)

    email = data["email"].strip().lower()
    if not is_valid_email(email):
        return error_response("Invalid email address", 400)
    if len(data["password"]) < 6:
        return error_response("Password must be at least 6 characters", 400)
    if User.query.filter_by(email=email).first():
        return error_response("Email already registered", 409)

    user = User(
        full_name=data["full_name"].strip(),
        email=email,
        phone=data.get("phone"),
        address=data.get("address"),
        user_type=data.get("user_type", "user"),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return success_response("User registered successfully", user.to_dict(), 201)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["email", "password"])
    if missing:
        return error_response(missing, 400)

    user = User.query.filter_by(email=data["email"].strip().lower()).first()
    if not user or not user.check_password(data["password"]):
        return error_response("Invalid credentials", 401)
    if not user.is_active:
        return error_response("Account is disabled", 403)

    identity = str(user.id)
    return success_response(
        "Login successful",
        {
            "user": user.to_dict(),
            "access_token": create_access_token(identity=identity),
            "refresh_token": create_refresh_token(identity=identity),
        },
    )


@auth_bp.post("/logout")
@jwt_required()
def logout():
    token = get_jwt()
    block = TokenBlocklist(
        jti=token["jti"],
        token_type=token["type"],
        user_id=int(get_jwt_identity()),
    )
    db.session.add(block)
    db.session.commit()
    return success_response("Logged out successfully")


@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    if not is_valid_email(email):
        return error_response("Valid email is required", 400)

    user = User.query.filter_by(email=email).first()
    if not user:
        return error_response("User not found", 404)

    reset_token = token_urlsafe(24)
    user.reset_token = reset_token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=30)
    db.session.commit()

    return success_response(
        "Password reset token generated",
        {"reset_token": reset_token, "expires_in_minutes": 30},
    )


@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["email", "reset_token", "new_password"])
    if missing:
        return error_response(missing, 400)

    user = User.query.filter_by(email=data["email"].strip().lower()).first()
    if not user:
        return error_response("User not found", 404)
    if user.reset_token != data["reset_token"]:
        return error_response("Invalid reset token", 400)
    if not user.reset_token_expires_at or user.reset_token_expires_at < datetime.utcnow():
        return error_response("Reset token expired", 400)
    if len(data["new_password"]) < 6:
        return error_response("Password must be at least 6 characters", 400)

    user.set_password(data["new_password"])
    user.reset_token = None
    user.reset_token_expires_at = None
    db.session.commit()
    return success_response("Password reset successfully")
