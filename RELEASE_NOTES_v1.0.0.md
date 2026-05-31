# NutriServe v1.0.0

NutriServe v1.0.0 is the first public release of the Nutrition and Food Service Management Web Application.

## Highlights

- Static HTML, CSS, and JavaScript frontend.
- Flask REST API backend.
- SQLite database support for local development and demo deployment.
- JWT-based user authentication.
- Meal plans for elders, gym nutrition, and kids.
- Weekly meal ordering workflow.
- Payment creation and payment status tracking.
- Delivery slot and delivery schedule management.
- User notifications.
- Admin dashboard, analytics, user management, and meal management.
- Postman collection and API documentation.
- Render deployment configuration with Gunicorn.

## Deployment

This release includes:

- `Procfile`
- `render.yaml`
- Root `requirements.txt`
- Backend `requirements.txt` with Gunicorn
- Production environment variable documentation

Recommended Render backend settings:

```text
Build Command: pip install -r requirements.txt
Start Command: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT
Health Check Path: /health
```

## Contributors

### Backend Developer & Project Integration

- Dhanush
- GitHub: https://github.com/07dhanush7

### Frontend Developer

- Savishakthi Prasad
- GitHub: https://github.com/savishakthiprasad-eng

## Notes

SQLite is suitable for local development and demo deployments. For production usage with persistent user data, migrate to a managed database such as PostgreSQL and restrict CORS to the deployed frontend domain.
