# Smart Canteen Pre-Ordering System Backend

Flask REST API for the Smart Canteen/NutriServe HTML, CSS, and vanilla JavaScript frontend.

## Stack

- Python Flask
- Flask-SQLAlchemy ORM
- Flask-JWT-Extended authentication
- Flask-Bcrypt password hashing
- Flask-CORS
- SQLite only

## Database

The app uses this SQLite file automatically:

```text
backend/instance/smart_canteen.db
```

Configuration:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///smart_canteen.db"
```

Because this is a relative SQLite URI, Flask-SQLAlchemy stores the database in the Flask `instance/` folder. Tables are created automatically on startup when `AUTO_CREATE_TABLES=1`.

## Install

```powershell
cd "C:\Users\Dhanush Ragava R V\OneDrive\Desktop\NUS2\NUS\NUS\backend"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Add Sample Data

```powershell
python dummy_data.py
```

Sample logins:

```text
Admin:    admin@nutriserve.com / admin123
User:     john@example.com / user123
Delivery: delivery@nutriserve.com / staff123
```

## Run Backend

From the project root:

```powershell
.\start_backend.bat
```

Or from `backend/`:

```powershell
.\start_backend.bat
```

Backend URL:

```text
http://127.0.0.1:5000
```

Health checks:

```text
GET http://127.0.0.1:5000/
GET http://127.0.0.1:5000/health
```

## Run Frontend

Open the frontend with Live Server at:

```text
http://127.0.0.1:5500/index.html
```

You can also open `index.html` directly, but Live Server is recommended.

## How Frontend Connects

The frontend JavaScript calls:

```javascript
const API_BASE_URL = "http://127.0.0.1:5000/api";
```

Login stores the JWT in `localStorage` as `access_token`. Protected requests send:

```javascript
Authorization: Bearer <access_token>
```

## Test APIs

Login:

```javascript
fetch("http://127.0.0.1:5000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "john@example.com",
    password: "user123"
  })
}).then(res => res.json()).then(console.log);
```

Get meals:

```javascript
fetch("http://127.0.0.1:5000/api/meals/?category=gym")
  .then(res => res.json())
  .then(console.log);
```

Create a weekly order:

```javascript
fetch("http://127.0.0.1:5000/api/orders/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${localStorage.getItem("access_token")}`
  },
  body: JSON.stringify({
    week_start_date: "2026-05-25",
    items: [
      { meal_id: 1, day_of_week: "Monday", quantity: 1 },
      { meal_id: 2, day_of_week: "Tuesday", quantity: 1 },
      { meal_id: 3, day_of_week: "Wednesday", quantity: 1 },
      { meal_id: 4, day_of_week: "Thursday", quantity: 1 },
      { meal_id: 5, day_of_week: "Friday", quantity: 1 },
      { meal_id: 6, day_of_week: "Saturday", quantity: 1 },
      { meal_id: 7, day_of_week: "Sunday", quantity: 1 }
    ]
  })
}).then(res => res.json()).then(console.log);
```

## Notes

- The backend uses SQLite only.
- SQLite tables auto-create on backend startup.
- CORS allows the frontend on `127.0.0.1:5500`.
- API responses use `{ "success": true, "message": "...", "data": ... }` and `{ "success": false, "message": "..." }`.
