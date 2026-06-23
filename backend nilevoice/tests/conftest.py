import uuid
from typing import Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app
from app.models.language import Language
from app.models.role import Role
from app.models.user import User


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def random_suffix() -> str:
    return uuid.uuid4().hex[:8]


def ensure_role(db: Session, name: str, description: str) -> Role:
    role = db.query(Role).filter(Role.name == name).one_or_none()
    if not role:
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def ensure_language(db: Session, code: str, name: str, native_name: Optional[str] = None) -> Language:
    language = db.query(Language).filter(Language.code == code).one_or_none()
    if not language:
        language = Language(code=code, name=name, native_name=native_name)
        db.add(language)
        db.commit()
        db.refresh(language)
    return language


def create_verified_user(db: Session, client: TestClient, email: str, username: str, password: str, full_name: str, role_name: str) -> User:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password, "full_name": full_name},
    )
    assert response.status_code == 201

    user = db.query(User).filter(User.email == email).one()
    user.email_verified = True
    user.is_active = True
    role = ensure_role(db, role_name, f"Auto-created {role_name} role")
    if role not in user.roles:
        user.roles.append(role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_token(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def verify_user_email(db: Session, client: TestClient, email: str) -> None:
    user = db.query(User).filter(User.email == email).one()
    assert user.verification_token is not None
    response = client.post(
        "/api/v1/auth/verify-email",
        json={"token": user.verification_token},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Email verified"
    db.refresh(user)
    assert user.email_verified is True
