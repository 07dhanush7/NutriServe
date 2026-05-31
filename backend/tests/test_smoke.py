from app import create_app
from app.extensions import db


def test_health_and_auth_flow():
    app = create_app("testing")
    client = app.test_client()

    with app.app_context():
        db.create_all()

    assert client.get("/").status_code == 200
    assert client.get("/health").get_json()["status"] == "healthy"
    assert client.get("/favicon.ico").status_code == 204

    register = client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "password": "secret123",
    })
    assert register.status_code == 201

    login = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "secret123",
    })
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]

    profile = client.get("/api/users/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
