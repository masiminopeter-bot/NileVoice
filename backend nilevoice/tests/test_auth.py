import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def random_suffix() -> str:
    return uuid.uuid4().hex[:8]


def test_register_login_refresh_cycle():
    email = "testuser@example.com"
    username = "testuser"
    password = "SecurePass123!"

    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password, "full_name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["username"] == username

    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
    assert "refresh_token" in payload

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": payload["refresh_token"]},
    )
    assert response.status_code == 200
    refreshed = response.json()
    assert refreshed["access_token"] != payload["access_token"]
    assert refreshed["refresh_token"] != payload["refresh_token"]


def test_forgot_reset_password():
    suffix = random_suffix()
    email = f"resetuser{suffix}@example.com"
    username = f"resetuser{suffix}"
    password = "ResetPass123!"

    client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password, "full_name": "Reset User"},
    )

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": email},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Password reset token created"


def test_verify_email_requires_token():
    response = client.post(
        "/api/v1/auth/verify-email",
        json={"token": "invalid-token"},
    )
    assert response.status_code == 400
