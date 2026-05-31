from datetime import datetime
from app.extensions import db

class WeeklyOrder(db.Model):
    __tablename__ = 'weekly_orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    week_start_date = db.Column(db.Date, nullable=False)
    delivery_address = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='weekly_order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='weekly_order', uselist=False, cascade='all, delete-orphan')
    delivery = db.relationship('Delivery', backref='weekly_order', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'total_price': self.total_price,
            'status': self.status,
            'week_start_date': self.week_start_date.isoformat() if self.week_start_date else None,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'payment': self.payment.to_dict() if self.payment else None,
            'delivery': self.delivery.to_dict() if self.delivery else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('weekly_orders.id', ondelete='CASCADE'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    delivery_time = db.Column(db.String(20), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_time = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'meal_id': self.meal_id,
            'day_of_week': self.day_of_week,
            'delivery_time': self.delivery_time,
            'quantity': self.quantity,
            'price_at_time': self.price_at_time,
            'line_total': self.quantity * self.price_at_time,
            'meal_name': self.meal_plan.meal_name if self.meal_plan else None
        }
