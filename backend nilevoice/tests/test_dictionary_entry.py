import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app
from app.models.language import Language
from app.models.role import Role
from app.models.user import User


def random_suffix() -> str:
    return uuid.uuid4().hex[:8]

client = TestClient(app)


def ensure_role(db: Session, name: str, description: str) -> Role:
    role = db.query(Role).filter(Role.name == name).one_or_none()
    if not role:
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def ensure_language(db: Session, code: str, name: str, native_name: str | None = None) -> Language:
    language = db.query(Language).filter(Language.code == code).one_or_none()
    if not language:
        language = Language(code=code, name=name, native_name=native_name)
        db.add(language)
        db.commit()
        db.refresh(language)
    return language


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_verified_user(db: Session, email: str, username: str, password: str, role_name: str, full_name: str) -> User:
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


def get_token(username: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_dictionary_entry_crud_and_search(db_session: Session):
    english = ensure_language(db_session, "en", "English", "English")
    spanish = ensure_language(db_session, "es", "Spanish", "Español")

    suffix = random_suffix()
    admin_username = f"admindict{suffix}"
    create_verified_user(
        db_session,
        email=f"admin-dict{suffix}@example.com",
        username=admin_username,
        password="AdminDict123!",
        full_name="Dictionary Admin",
        role_name="Admin",
    )
    admin_token = get_token(admin_username, "AdminDict123!")

    create_resp = client.post(
        "/api/v1/dictionary/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "language_id": english.id,
            "entry_type": "word",
            "term": "hello",
            "translation": "hola",
            "part_of_speech": "interjection",
            "example": "Hello, how are you?",
        },
    )
    assert create_resp.status_code == 201
    entry_data = create_resp.json()
    assert entry_data["term"] == "hello"
    assert entry_data["translation"] == "hola"
    entry_id = entry_data["id"]

    list_resp = client.get(
        "/api/v1/dictionary/",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"query": "hola", "languageId": english.id},
    )
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["total"] >= 1
    assert any(item["id"] == entry_id for item in list_data["items"])

    update_resp = client.put(
        f"/api/v1/dictionary/{entry_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"translation": "hola!", "is_verified": True},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["translation"] == "hola!"
    assert update_resp.json()["is_verified"] is True

    get_resp = client.get(
        f"/api/v1/dictionary/{entry_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["term"] == "hello"

    delete_resp = client.delete(
        f"/api/v1/dictionary/{entry_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert delete_resp.status_code == 204

    not_found_resp = client.get(
        f"/api/v1/dictionary/{entry_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert not_found_resp.status_code == 404
