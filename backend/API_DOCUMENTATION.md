# Smart Canteen API Documentation

Base URL:

```text
http://127.0.0.1:5000
```

Response format:

```json
{ "success": true, "message": "Success", "data": {} }
```

```json
{ "success": false, "message": "Invalid credentials" }
```

## System

`GET /`

Returns backend running message.

`GET /health`

Returns `{ "status": "healthy" }`.

## Authentication

`POST /api/auth/register`

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "password": "user123",
  "user_type": "user"
}
```

`POST /api/auth/login`

```json
{
  "email": "john@example.com",
  "password": "user123"
}
```

Returns `access_token`, `refresh_token`, and user details.

`POST /api/auth/logout`

Requires `Authorization: Bearer <token>`.

`POST /api/auth/forgot-password`

```json
{ "email": "john@example.com" }
```

`POST /api/auth/reset-password`

```json
{
  "email": "john@example.com",
  "reset_token": "token-from-forgot-password",
  "new_password": "newpass123"
}
```

## Users

`GET /api/users/profile`

Requires auth.

`PUT /api/users/profile`

```json
{
  "full_name": "John Updated",
  "phone": "9999999999",
  "address": "Bangalore"
}
```

`DELETE /api/users/account`

Disables the account.

## Meal Plans

Categories:

- `elders`: Elderly Meal Plan
- `gym`: Gym Nutrition Meal Plan
- `kids`: Kids Meal Plan

`GET /api/meals/`

`GET /api/meals/?category=gym`

`GET /api/meals/?category=kids&search=pizza`

`GET /api/meals/<id>`

`POST /api/meals/`

Admin only.

```json
{
  "meal_name": "Protein Bowl",
  "category": "gym",
  "price": 180,
  "calories": 420,
  "protein": 35,
  "carbs": 35,
  "fats": 12,
  "image": "static/images/f1.jpg",
  "description": "High protein meal"
}
```

`PUT /api/meals/<id>`

Admin only.

`DELETE /api/meals/<id>`

Admin only.

## Weekly Orders

`POST /api/orders/`

Requires auth. Must include all 7 days.

```json
{
  "week_start_date": "2026-05-25",
  "delivery_address": "Bangalore",
  "items": [
    { "meal_id": 1, "day_of_week": "Monday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 2, "day_of_week": "Tuesday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 3, "day_of_week": "Wednesday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 4, "day_of_week": "Thursday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 5, "day_of_week": "Friday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 6, "day_of_week": "Saturday", "delivery_time": "12:00", "quantity": 1 },
    { "meal_id": 7, "day_of_week": "Sunday", "delivery_time": "12:00", "quantity": 1 }
  ]
}
```

`GET /api/orders/`

Users see their orders. Admin sees all orders.

`GET /api/orders/<id>`

`PUT /api/orders/<id>`

Updates weekly order details/items before delivery/cancellation.

`PUT /api/orders/<id>/cancel`

`PUT /api/orders/<id>/status`

Admin only. Valid statuses: `Pending`, `Confirmed`, `Preparing`, `Delivered`, `Cancelled`.

## Time Slots And Delivery

`GET /api/delivery/slots`

Returns active time slots with capacity information.

`POST /api/delivery/slots`

Admin only.

```json
{
  "start_time": "12:00",
  "end_time": "13:00",
  "max_capacity": 50
}
```

`PUT /api/delivery/slots/<id>`

Admin only.

`POST /api/delivery/schedule`

Admin only.

```json
{
  "order_id": 1,
  "time_slot_id": 1,
  "delivery_date": "2026-05-25",
  "delivery_staff_id": 3
}
```

`GET /api/delivery/schedule`

Admin or delivery staff.

`PUT /api/delivery/assign/<delivery_id>`

Admin only.

`PUT /api/delivery/status/<delivery_id>`

Admin or delivery staff.

## Payments

`POST /api/payments/create`

```json
{
  "order_id": 1,
  "payment_method": "Cash on Delivery"
}
```

Online structure:

```json
{
  "order_id": 1,
  "payment_method": "UPI",
  "provider": "GPay"
}
```

Statuses: `Pending`, `Paid`, `Failed`.

`GET /api/payments/`

Admin only.

`PUT /api/payments/<id>/status`

Admin only.

## Notifications

`GET /api/notifications/`

`PUT /api/notifications/<id>/read`

## Admin

`GET /api/admin/dashboard`

Returns total users, total orders, revenue, pending deliveries, pending payments, and most ordered meals.

`GET /api/admin/analytics/revenue?days=30`

`GET /api/admin/analytics/orders`

`GET /api/admin/users`
