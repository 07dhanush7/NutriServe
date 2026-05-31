from flask import Blueprint, request

from app.extensions import db
from app.models.meal_plan import Category
from app.utils.auth import role_required
from app.utils.response import error_response, success_response
from app.utils.validators import require_fields

category_bp = Blueprint("category", __name__)


@category_bp.get("/")
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return success_response("Categories retrieved successfully", [c.to_dict() for c in categories])


@category_bp.post("/")
@role_required("admin")
def create_category():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["name", "slug"])
    if missing:
        return error_response(missing, 400)
    if Category.query.filter((Category.name == data["name"]) | (Category.slug == data["slug"])).first():
        return error_response("Category already exists", 409)

    category = Category(
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        image_url=data.get("image_url"),
    )
    db.session.add(category)
    db.session.commit()
    return success_response("Category created successfully", category.to_dict(), 201)


@category_bp.put("/<int:category_id>")
@role_required("admin")
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json(silent=True) or {}
    for field in ["name", "slug", "description", "image_url", "is_active"]:
        if field in data:
            setattr(category, field, data[field])
    db.session.commit()
    return success_response("Category updated successfully", category.to_dict())


@category_bp.delete("/<int:category_id>")
@role_required("admin")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return success_response("Category deleted successfully")
