from datetime import time

from app import create_app
from app.extensions import db
from app.models.delivery import TimeSlot
from app.models.meal_plan import Category, MealPlan
from app.models.user import User

app = create_app()


def create_user(full_name, email, phone, password, user_type, address=None):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    user = User(
        full_name=full_name,
        email=email,
        phone=phone,
        user_type=user_type,
        address=address,
    )
    user.set_password(password)
    db.session.add(user)
    return user


def seed_database():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        print("Seeding dummy data...")

        create_user("System Admin", "admin@nutriserve.com", "1234567890", "admin123", "admin")
        create_user("John Doe", "john@example.com", "0987654321", "user123", "user", "Bangalore")
        create_user("Delivery Person 1", "delivery@nutriserve.com", "1112223333", "staff123", "delivery")

        categories = [
            ("Elderly Meal Plan", "elders", "Healthy soft meals"),
            ("Gym Nutrition Meal Plan", "gym", "High-protein meals"),
            ("Kids Meal Plan", "kids", "Tasty fun meals"),
        ]
        category_map = {}
        for name, slug, description in categories:
            category = Category.query.filter_by(slug=slug).first()
            if not category:
                category = Category(name=name, slug=slug, description=description)
                db.session.add(category)
                db.session.flush()
            category_map[slug] = category

        meals = [
            ("Grilled Chicken", "gym", 220, "f1.jpg"), ("Protein Pasta", "gym", 200, "f2.jpg"),
            ("Egg Toast", "gym", 180, "f3.jpg"), ("Chicken Wrap", "gym", 150, "f4.jpg"),
            ("Paneer Bowl", "gym", 210, "f5.jpg"), ("Quinoa Salad", "gym", 190, "f6.jpg"),
            ("Steak", "gym", 190, "f7.jpg"), ("Salmon", "gym", 270, "f8.jpg"),
            ("Oats", "gym", 150, "f9.jpg"), ("Pancakes", "gym", 160, "f10.jpg"),
            ("Egg Combo", "gym", 120, "f11.jpg"), ("Yogurt Bowl", "gym", 140, "f12.jpg"),
            ("Chicken Salad", "gym", 180, "f13.jpg"), ("Tuna Sandwich", "gym", 170, "f14.jpg"),
            ("Veg Bowl", "gym", 160, "f15.jpg"),
            ("Idli", "elders", 80, "e1.jpg"), ("Khichdi", "elders", 120, "e2.jpg"),
            ("Porridge", "elders", 90, "e3.jpg"), ("Veggies", "elders", 100, "e4.jpg"),
            ("Dal Rice", "elders", 110, "e5.jpg"), ("Curd Rice", "elders", 90, "e6.jpg"),
            ("Fruit Bowl", "elders", 80, "e7.jpg"), ("Oats Meal", "elders", 95, "e8.jpg"),
            ("Soup", "elders", 100, "e9.jpg"), ("Veg Plate", "elders", 110, "e10.jpg"),
            ("Upma", "elders", 85, "e11.jpg"), ("Dal Soup", "elders", 95, "e12.jpg"),
            ("Chapati", "elders", 100, "e13.jpg"), ("Sambar Rice", "elders", 120, "e14.jpg"),
            ("Banana Mash", "elders", 70, "e15.jpg"),
            ("Kids Pancakes", "kids", 120, "k1.jpg"), ("Sandwich", "kids", 100, "k2.jpg"),
            ("Fruit Salad", "kids", 90, "k3.jpg"), ("Nuggets", "kids", 110, "k4.jpg"),
            ("Milkshake", "kids", 80, "k5.jpg"), ("Kids Oats", "kids", 95, "k6.jpg"),
            ("Mini Idli", "kids", 70, "k7.jpg"), ("Corn Salad", "kids", 85, "k8.jpg"),
            ("Pizza", "kids", 130, "k9.jpg"), ("Roll", "kids", 100, "k10.jpg"),
            ("Cupcake", "kids", 60, "k11.jpg"), ("Smoothie", "kids", 110, "k12.jpg"),
            ("Lean Protein", "kids", 70, "k13.jpg"), ("Paneer Fried Rice", "kids", 90, "k14.jpg"),
            ("Burger", "kids", 120, "k15.jpg"),
        ]
        for name, category, price, image in meals:
            meal = MealPlan.query.filter_by(meal_name=name, category=category).first()
            image_path = f"static/images/{image}"
            if meal:
                meal.price = price
                meal.image = image_path
                meal.category_id = category_map[category].id
                meal.is_available = True
            else:
                db.session.add(MealPlan(
                    meal_name=name,
                    category=category,
                    category_id=category_map[category].id,
                    price=price,
                    calories=350,
                    protein=20,
                    carbs=40,
                    fats=10,
                    image=image_path,
                    description=f"{name} for {category_map[category].name}",
                ))

        for start, end, capacity in [
            (time(11, 0), time(12, 0), 20),
            (time(12, 0), time(13, 0), 50),
            (time(13, 0), time(14, 0), 30),
        ]:
            if not TimeSlot.query.filter_by(start_time=start, end_time=end).first():
                db.session.add(TimeSlot(start_time=start, end_time=end, max_capacity=capacity))

        db.session.commit()
        print("Dummy data inserted successfully!")
        print("-" * 30)
        print("Admin login: admin@nutriserve.com / admin123")
        print("User login: john@example.com / user123")
        print("Delivery login: delivery@nutriserve.com / staff123")
        print("-" * 30)

if __name__ == "__main__":
    seed_database()
