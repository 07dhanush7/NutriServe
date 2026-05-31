from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.meal_plan import MealPlan
from app.models.order import OrderItem, WeeklyOrder
from app.models.payment_notification import Notification
from app.utils.auth import current_user, role_required
from app.utils.response import error_response, success_response
from app.utils.validators import require_fields

order_bp = Blueprint("order", __name__)
DAYS_OF_WEEK = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
ORDER_STATUSES = {"Pending", "Completed"}


def build_order_items(order, items):
    if not isinstance(items, list) or not items:
        return "items must be a non-empty list"

    selected_days = {item.get("day_of_week") for item in items}
    if selected_days != DAYS_OF_WEEK:
        return "Please select meals for all 7 days: Monday to Sunday"

    total_price = 0.0
    for item_data in items:
        missing_item = require_fields(item_data, ["meal_id", "day_of_week"])
        if missing_item:
            return missing_item

        meal = MealPlan.query.filter_by(id=item_data["meal_id"], is_available=True).first()
        if not meal:
            return f"Meal {item_data['meal_id']} not found or unavailable"

        quantity = int(item_data.get("quantity", 1))
        if quantity <= 0:
            return "Quantity must be greater than zero"

        order_item = OrderItem(
            order_id=order.id,
            meal_id=meal.id,
            day_of_week=item_data["day_of_week"],
            delivery_time=item_data.get("delivery_time"),
            quantity=quantity,
            price_at_time=meal.price,
        )
        db.session.add(order_item)
        total_price += meal.price * quantity

    order.total_price = round(total_price, 2)
    return None


@order_bp.post("/")
@jwt_required()
def create_order():
    user = current_user()
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["week_start_date", "items"])
    if missing:
        return error_response(missing, 400)
    try:
        week_start = datetime.strptime(data["week_start_date"], "%Y-%m-%d").date()
    except ValueError:
        return error_response("Invalid week_start_date. Use YYYY-MM-DD", 400)

    order = WeeklyOrder(
        user_id=user.id,
        week_start_date=week_start,
        delivery_address=data.get("delivery_address") or user.address,
        notes=data.get("notes"),
    )
    db.session.add(order)
    db.session.flush()

    item_error = build_order_items(order, data["items"])
    if item_error:
        db.session.rollback()
        status = 404 if "not found" in item_error else 400
        return error_response(item_error, status)

    db.session.add(Notification(
        user_id=user.id,
        title="Order placed",
        message=f"Your order #{order.id} was created successfully.",
        notification_type="order",
    ))
    db.session.commit()
    return success_response("Order created successfully", order.to_dict(), 201)


@order_bp.put("/<int:order_id>")
@jwt_required()
def update_order(order_id):
    user = current_user()
    query = WeeklyOrder.query.filter_by(id=order_id)
    if user.user_type != "admin":
        query = query.filter_by(user_id=user.id)
    order = query.first()
    if not order:
        return error_response("Order not found", 404)
    data = request.get_json(silent=True) or {}
    if "week_start_date" in data:
        try:
            order.week_start_date = datetime.strptime(data["week_start_date"], "%Y-%m-%d").date()
        except ValueError:
            return error_response("Invalid week_start_date. Use YYYY-MM-DD", 400)
    if "delivery_address" in data:
        order.delivery_address = data["delivery_address"]
    if "notes" in data:
        order.notes = data["notes"]

    if "items" in data:
        OrderItem.query.filter_by(order_id=order.id).delete()
        db.session.flush()
        item_error = build_order_items(order, data["items"])
        if item_error:
            db.session.rollback()
            status = 404 if "not found" in item_error else 400
            return error_response(item_error, status)

    db.session.commit()
    return success_response("Order updated successfully", order.to_dict())


@order_bp.get("/")
@jwt_required()
def get_orders():
    user = current_user()
    if user.user_type == "admin":
        orders = WeeklyOrder.query.order_by(WeeklyOrder.created_at.desc()).all()
    else:
        orders = WeeklyOrder.query.filter_by(user_id=user.id).order_by(WeeklyOrder.created_at.desc()).all()
    return success_response("Orders retrieved successfully", [order.to_dict() for order in orders])


@order_bp.get("/<int:order_id>")
@jwt_required()
def get_order(order_id):
    user = current_user()
    query = WeeklyOrder.query.filter_by(id=order_id)
    if user.user_type != "admin":
        query = query.filter_by(user_id=user.id)
    order = query.first()
    if not order:
        return error_response("Order not found", 404)
    return success_response("Order retrieved successfully", order.to_dict())


@order_bp.put("/<int:order_id>/status")
@role_required("admin")
def update_order_status(order_id):
    order = WeeklyOrder.query.get_or_404(order_id)
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in ORDER_STATUSES:
        return error_response("Invalid order status. Use Pending or Completed", 400)
    if order.status == status:
        return success_response("Order status already updated", order.to_dict())
    order.status = status
    db.session.add(Notification(
        user_id=order.user_id,
        title="Order updated",
        message=f"Your order #{order.id} status changed to {status}.",
        notification_type="order",
    ))
    db.session.commit()
    return success_response("Order status updated successfully", order.to_dict())


@order_bp.put("/<int:order_id>/cancel")
@jwt_required()
def cancel_order(order_id):
    user = current_user()
    query = WeeklyOrder.query.filter_by(id=order_id)
    if user.user_type != "admin":
        query = query.filter_by(user_id=user.id)
    order = query.first()
    if not order:
        return error_response("Order not found", 404)

    order.status = "Pending"
    db.session.commit()
    return success_response("Order moved back to Pending", order.to_dict())
