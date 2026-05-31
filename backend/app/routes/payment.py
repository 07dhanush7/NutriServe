from uuid import uuid4

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.order import WeeklyOrder
from app.models.payment_notification import Notification, Payment
from app.utils.auth import current_user, role_required
from app.utils.response import error_response, success_response
from app.utils.validators import require_fields

payment_bp = Blueprint("payment", __name__)


@payment_bp.post("/create")
@jwt_required()
def create_payment():
    user = current_user()
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["order_id", "payment_method"])
    if missing:
        return error_response(missing, 400)

    query = WeeklyOrder.query.filter_by(id=data["order_id"])
    if user.user_type != "admin":
        query = query.filter_by(user_id=user.id)
    order = query.first()
    if not order:
        return error_response("Order not found", 404)
    if order.payment:
        return error_response("Payment already exists for this order", 409)

    method = data["payment_method"]
    is_online = method.lower() in ["online", "upi", "card"]
    payment = Payment(
        order_id=order.id,
        amount=order.total_price,
        payment_method=method,
        status="Paid" if is_online else "Pending",
        transaction_id=str(uuid4()) if is_online else None,
        provider=data.get("provider"),
        provider_payload=data.get("provider_payload"),
    )
    db.session.add(payment)
    db.session.add(Notification(
        user_id=order.user_id,
        title="Payment updated",
        message=f"Payment for order #{order.id} is {payment.status}.",
        notification_type="payment",
    ))
    db.session.commit()
    return success_response("Payment created successfully", payment.to_dict(), 201)


@payment_bp.get("/")
@role_required("admin")
def list_payments():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return success_response("Payments retrieved successfully", [p.to_dict() for p in payments])


@payment_bp.put("/<int:payment_id>/status")
@role_required("admin")
def update_payment_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in ["Pending", "Paid", "Failed", "Refunded"]:
        return error_response("Invalid payment status", 400)

    payment.status = status
    db.session.add(Notification(
        user_id=payment.weekly_order.user_id,
        title="Payment status changed",
        message=f"Payment for order #{payment.order_id} is {status}.",
        notification_type="payment",
    ))
    db.session.commit()
    return success_response("Payment status updated successfully", payment.to_dict())
