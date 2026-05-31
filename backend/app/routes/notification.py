from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.payment_notification import Notification
from app.utils.auth import current_user
from app.utils.response import error_response, success_response

notification_bp = Blueprint("notification", __name__)


@notification_bp.get("/")
@jwt_required()
def list_notifications():
    user = current_user()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    return success_response("Notifications retrieved successfully", [n.to_dict() for n in notifications])


@notification_bp.put("/<int:notification_id>/read")
@jwt_required()
def mark_read(notification_id):
    user = current_user()
    notification = Notification.query.filter_by(id=notification_id, user_id=user.id).first()
    if not notification:
        return error_response("Notification not found", 404)
    notification.is_read = True
    db.session.commit()
    return success_response("Notification marked as read", notification.to_dict())
