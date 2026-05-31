from datetime import datetime, timedelta

from flask import Blueprint, request
from sqlalchemy import func

from app.extensions import db
from app.models.delivery import Delivery
from app.models.meal_plan import MealPlan
from app.models.order import OrderItem, WeeklyOrder
from app.models.payment_notification import Payment
from app.models.user import User
from app.utils.auth import role_required
from app.utils.response import success_response

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/dashboard")
@role_required("admin")
def get_dashboard_stats():
    paid_revenue = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.status == "Paid").scalar()
    data = {
        "total_users": User.query.filter_by(user_type="user").count(),
        "total_orders": WeeklyOrder.query.count(),
        "total_menu_items": MealPlan.query.count(),
        "total_revenue": round(float(paid_revenue or 0), 2),
        "pending_deliveries": Delivery.query.filter_by(status="Pending").count(),
        "pending_payments": Payment.query.filter_by(status="Pending").count(),
        "most_ordered_meals": most_ordered_meals(),
    }
    return success_response("Dashboard stats retrieved successfully", data)


def most_ordered_meals():
    rows = (
        db.session.query(MealPlan.meal_name, func.coalesce(func.sum(OrderItem.quantity), 0))
        .join(OrderItem, OrderItem.meal_id == MealPlan.id)
        .group_by(MealPlan.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    return [{"meal_name": name, "quantity": int(quantity or 0)} for name, quantity in rows]


@admin_bp.get("/analytics/revenue")
@role_required("admin")
def revenue_analytics():
    days = int(request.args.get("days", 30))
    start = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.session.query(func.date(Payment.created_at), func.sum(Payment.amount))
        .filter(Payment.status == "Paid", Payment.created_at >= start)
        .group_by(func.date(Payment.created_at))
        .all()
    )
    data = [{"date": str(day), "revenue": float(total or 0)} for day, total in rows]
    return success_response("Revenue analytics retrieved successfully", data)


@admin_bp.get("/analytics/orders")
@role_required("admin")
def order_analytics():
    rows = db.session.query(WeeklyOrder.status, func.count(WeeklyOrder.id)).group_by(WeeklyOrder.status).all()
    data = {status: count for status, count in rows}
    return success_response("Order analytics retrieved successfully", data)


@admin_bp.get("/users")
@role_required("admin")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return success_response("Users retrieved successfully", [user.to_dict() for user in users])
