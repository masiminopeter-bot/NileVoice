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
settings = get_settings()


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


def test_translation_submission_crud_and_review(db_session: Session):
    suffix = random_suffix()
    english = ensure_language(db_session, f"en{suffix}", "English", "English")
    juba_arabic = ensure_language(db_session, f"juba_ar{suffix}", "Juba Arabic", "Juba Arabic")

    translator_username = f"translator{suffix}"
    create_verified_user(
        db_session,
        email=f"translator{suffix}@example.com",
        username=translator_username,
        password="TranslatorPass123!",
        full_name="Approved Translator",
        role_name="Translator",
    )
    translator_token = get_token(translator_username, "TranslatorPass123!")

    create_resp = client.post(
        "/api/v1/submissions/",
        headers={"Authorization": f"Bearer {translator_token}"},
        json={
            "source_language_id": english.id,
            "target_language_id": juba_arabic.id,
            "submission_type": "phrase",
            "original_text": "Hello world",
            "translated_text": "Salaam dunia",
            "notes": "Initial submission",
        },
    )
    assert create_resp.status_code == 201
    submission_data = create_resp.json()
    assert submission_data["submission_type"] == "phrase"
    assert submission_data["status"] == "pending"
    submission_id = submission_data["id"]

    list_resp = client.get(
        "/api/v1/submissions/",
        headers={"Authorization": f"Bearer {translator_token}"},
    )
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["total"] >= 1
    assert any(item["id"] == submission_id for item in list_data["items"])

    update_resp = client.put(
        f"/api/v1/submissions/{submission_id}",
        headers={"Authorization": f"Bearer {translator_token}"},
        json={"translated_text": "Salaam duniya", "notes": "Updated translation"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["translated_text"] == "Salaam duniya"

    admin_username = f"admin{suffix}"
    create_verified_user(
        db_session,
        email=f"admin{suffix}@example.com",
        username=admin_username,
        password="AdminPass123!",
        full_name="Platform Admin",
        role_name="Admin",
    )
    admin_token = get_token(admin_username, "AdminPass123!")

    review_resp = client.post(
        f"/api/v1/submissions/{submission_id}/review",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "approved", "reviewer_notes": "Looks good"},
    )
    assert review_resp.status_code == 200
    assert review_resp.json()["status"] == "approved"

    delete_resp = client.delete(
        f"/api/v1/submissions/{submission_id}",
        headers={"Authorization": f"Bearer {translator_token}"},
    )
    assert delete_resp.status_code == 204

    get_resp = client.get(
        f"/api/v1/submissions/{submission_id}",
        headers={"Authorization": f"Bearer {translator_token}"},
    )
    assert get_resp.status_code == 404
