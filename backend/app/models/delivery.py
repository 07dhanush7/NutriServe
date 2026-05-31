from datetime import datetime
from app.extensions import db

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False, default=50)
    is_active = db.Column(db.Boolean, default=True)

    deliveries = db.relationship('Delivery', backref='time_slot', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'max_capacity': self.max_capacity,
            'is_active': self.is_active
        }

class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('weekly_orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id', ondelete='CASCADE'), nullable=False)
    delivery_staff_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_address = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'time_slot_id': self.time_slot_id,
            'delivery_staff_id': self.delivery_staff_id,
            'status': self.status,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'time_slot': self.time_slot.to_dict() if self.time_slot else None,
            'staff_name': self.staff.full_name if self.staff else None
        }
