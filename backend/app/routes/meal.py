from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, request
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.meal_plan import Category, MealPlan
from app.utils.auth import role_required
from app.utils.response import error_response, success_response
from app.utils.validators import require_fields

meal_bp = Blueprint("meal", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


@meal_bp.get("/")
def get_meals():
    category = request.args.get("category")
    search = request.args.get("search")
    include_unavailable = request.args.get("include_unavailable") == "1"

    query = MealPlan.query
    if category:
        query = query.filter(MealPlan.category.ilike(category))
    if search:
        query = query.filter(MealPlan.meal_name.ilike(f"%{search}%"))
    if not include_unavailable:
        query = query.filter_by(is_available=True)

    meals = query.order_by(MealPlan.created_at.desc()).all()
    return success_response("Meals retrieved successfully", [meal.to_dict() for meal in meals])


@meal_bp.get("/<int:meal_id>")
def get_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    return success_response("Meal retrieved successfully", meal.to_dict())


@meal_bp.post("/")
@role_required("admin")
def add_meal():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["meal_name", "category", "price"])
    if missing:
        return error_response(missing, 400)

    category = Category.query.filter_by(slug=data["category"]).first() or Category.query.filter_by(name=data["category"]).first()
    meal = MealPlan(
        meal_name=data["meal_name"],
        category=data["category"],
        category_id=category.id if category else None,
        price=float(data["price"]),
        calories=data.get("calories"),
        protein=data.get("protein"),
        carbs=data.get("carbs"),
        fats=data.get("fats"),
        image=data.get("image"),
        description=data.get("description"),
        is_available=data.get("is_available", True),
    )
    db.session.add(meal)
    db.session.commit()
    return success_response("Meal plan added successfully", meal.to_dict(), 201)


@meal_bp.put("/<int:meal_id>")
@role_required("admin")
def update_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    data = request.get_json(silent=True) or {}
    for field in ["meal_name", "category", "price", "calories", "protein", "carbs", "fats", "image", "description", "is_available"]:
        if field in data:
            setattr(meal, field, data[field])
    db.session.commit()
    return success_response("Meal plan updated successfully", meal.to_dict())


@meal_bp.delete("/<int:meal_id>")
@role_required("admin")
def delete_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return success_response("Meal plan deleted successfully")


@meal_bp.post("/upload-image")
@role_required("admin")
def upload_meal_image():
    file = request.files.get("image")
    if not file or not file.filename:
        return error_response("Image file is required", 400)

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return error_response("Allowed image types: png, jpg, jpeg, webp", 400)

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = secure_filename(f"{uuid4().hex}.{ext}")
    file.save(upload_dir / filename)
    return success_response("Image uploaded successfully", {"image": f"/uploads/{filename}"}, 201)
