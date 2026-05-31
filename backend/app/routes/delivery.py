from datetime import datetime

from flask import Blueprint, request

from app.extensions import db
from app.models.delivery import Delivery, TimeSlot
from app.models.order import WeeklyOrder
from app.models.payment_notification import Notification
from app.models.user import User
from app.utils.auth import role_required
from app.utils.response import error_response, success_response
from app.utils.validators import require_fields

delivery_bp = Blueprint("delivery", __name__)


@delivery_bp.get("/slots")
def get_slots():
    slots = TimeSlot.query.filter_by(is_active=True).order_by(TimeSlot.start_time.asc()).all()
    data = []
    for slot in slots:
        slot_data = slot.to_dict()
        booked = Delivery.query.filter_by(time_slot_id=slot.id).count()
        slot_data["booked_count"] = booked
        slot_data["available_capacity"] = max(slot.max_capacity - booked, 0)
        data.append(slot_data)
    return success_response("Time slots retrieved successfully", data)


@delivery_bp.post("/slots")
@role_required("admin")
def add_slot():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["start_time", "end_time"])
    if missing:
        return error_response(missing, 400)
    try:
        start = datetime.strptime(data["start_time"], "%H:%M").time()
        end = datetime.strptime(data["end_time"], "%H:%M").time()
    except ValueError:
        return error_response("Invalid time format. Use HH:MM", 400)

    slot = TimeSlot(start_time=start, end_time=end, max_capacity=int(data.get("max_capacity", 50)))
    db.session.add(slot)
    db.session.commit()
    return success_response("Time slot added successfully", slot.to_dict(), 201)


@delivery_bp.put("/slots/<int:slot_id>")
@role_required("admin")
def update_slot(slot_id):
    slot = TimeSlot.query.get_or_404(slot_id)
    data = request.get_json(silent=True) or {}
    if "start_time" in data:
        try:
            slot.start_time = datetime.strptime(data["start_time"], "%H:%M").time()
        except ValueError:
            return error_response("Invalid start_time. Use HH:MM", 400)
    if "end_time" in data:
        try:
            slot.end_time = datetime.strptime(data["end_time"], "%H:%M").time()
        except ValueError:
            return error_response("Invalid end_time. Use HH:MM", 400)
    if "max_capacity" in data:
        slot.max_capacity = int(data["max_capacity"])
    if "is_active" in data:
        slot.is_active = bool(data["is_active"])
    db.session.commit()
    return success_response("Time slot updated successfully", slot.to_dict())


@delivery_bp.post("/schedule")
@role_required("admin")
def schedule_delivery():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["order_id", "time_slot_id", "delivery_date"])
    if missing:
        return error_response(missing, 400)
    order = WeeklyOrder.query.get(data["order_id"])
    slot = TimeSlot.query.get(data["time_slot_id"])
    if not order:
        return error_response("Order not found", 404)
    if not slot or not slot.is_active:
        return error_response("Time slot not found or inactive", 404)
    if order.delivery:
        return error_response("Delivery already scheduled for this order", 409)

    try:
        delivery_date = datetime.strptime(data["delivery_date"], "%Y-%m-%d").date()
    except ValueError:
        return error_response("Invalid delivery_date. Use YYYY-MM-DD", 400)

    booked = Delivery.query.filter_by(time_slot_id=slot.id, delivery_date=delivery_date).count()
    if booked >= slot.max_capacity:
        return error_response("Time slot capacity is full", 409)

    delivery = Delivery(
        order_id=order.id,
        time_slot_id=slot.id,
        delivery_staff_id=data.get("delivery_staff_id"),
        delivery_date=delivery_date,
        delivery_address=data.get("delivery_address") or order.delivery_address,
        notes=data.get("notes"),
    )
    db.session.add(delivery)
    db.session.add(Notification(
        user_id=order.user_id,
        title="Delivery scheduled",
        message=f"Delivery for order #{order.id} has been scheduled.",
        notification_type="delivery",
    ))
    db.session.commit()
    return success_response("Delivery scheduled successfully", delivery.to_dict(), 201)


@delivery_bp.get("/schedule")
@role_required("admin", "delivery")
def get_deliveries():
    deliveries = Delivery.query.order_by(Delivery.delivery_date.desc()).all()
    return success_response("Deliveries retrieved successfully", [d.to_dict() for d in deliveries])


@delivery_bp.put("/assign/<int:delivery_id>")
@role_required("admin")
def assign_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    data = request.get_json(silent=True) or {}
    staff_id = data.get("delivery_staff_id")
    staff = User.query.filter_by(id=staff_id, user_type="delivery").first()
    if not staff:
        return error_response("Delivery staff not found", 404)

    delivery.delivery_staff_id = staff.id
    delivery.status = "Assigned"
    db.session.commit()
    return success_response("Delivery assigned successfully", delivery.to_dict())


@delivery_bp.put("/status/<int:delivery_id>")
@role_required("admin", "delivery")
def update_status(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in ["Pending", "Assigned", "Out for delivery", "Delivered", "Failed"]:
        return error_response("Invalid delivery status", 400)

    delivery.status = status
    if status == "Delivered":
        delivery.weekly_order.status = "Completed"
    db.session.add(Notification(
        user_id=delivery.weekly_order.user_id,
        title="Delivery updated",
        message=f"Delivery for order #{delivery.order_id} is {status}.",
        notification_type="delivery",
    ))
    db.session.commit()
    return success_response("Delivery status updated successfully", delivery.to_dict())
