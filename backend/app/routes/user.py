from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.utils.auth import current_user
from app.utils.response import error_response, success_response

user_bp = Blueprint("user", __name__)


@user_bp.get("/profile")
@jwt_required()
def get_profile():
    user = current_user()
    if not user:
        return error_response("User not found", 404)
    return success_response("Profile retrieved successfully", user.to_dict())


@user_bp.put("/profile")
@jwt_required()
def update_profile():
    user = current_user()
    if not user:
        return error_response("User not found", 404)

    data = request.get_json(silent=True) or {}
    for field in ["full_name", "phone", "address"]:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return success_response("Profile updated successfully", user.to_dict())


@user_bp.post("/change-password")
@jwt_required()
def change_password():
    user = current_user()
    data = request.get_json(silent=True) or {}
    if not data.get("old_password") or not data.get("new_password"):
        return error_response("Old and new passwords are required", 400)
    if not user.check_password(data["old_password"]):
        return error_response("Incorrect old password", 400)
    if len(data["new_password"]) < 6:
        return error_response("Password must be at least 6 characters", 400)

    user.set_password(data["new_password"])
    db.session.commit()
    return success_response("Password changed successfully")


@user_bp.delete("/account")
@jwt_required()
def delete_account():
    user = current_user()
    if not user:
        return error_response("User not found", 404)
    user.is_active = False
    db.session.commit()
    return success_response("Account disabled successfully")
