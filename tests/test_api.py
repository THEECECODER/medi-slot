from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_protected_endpoint_without_token():
    response = client.get("/bookings/")

    assert response.status_code in [401, 403]


def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401