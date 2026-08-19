import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_success():
    response = client.post("/api/auth/login", json={
        "email": "admin@platform.ai",
        "password": "Admin@123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "ADMIN"


def test_login_invalid_password():
    response = client.post("/api/auth/login", json={
        "email": "admin@platform.ai",
        "password": "WrongPassword123"
    })
    assert response.status_code == 401
