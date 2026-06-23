import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.language import Language
from app.models.role import Role
from app.models.user import User

client = TestClient(app)


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


def ensure_language(db: Session, code: str, name: str, native_name: str | None = None) -> Language:
    language = db.query(Language).filter(Language.code == code).one_or_none()
    if not language:
        language = Language(code=code, name=name, native_name=native_name)
        db.add(language)
        db.commit()
        db.refresh(language)
    return language


def create_verified_user(db: Session, email: str, username: str, password: str, full_name: str, role_name: str) -> User:
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


def test_translate_text_with_dictionary_entry(db_session: Session):
    english = ensure_language(db_session, "en", "English", "English")
    spanish = ensure_language(db_session, "es", "Spanish", "Español")

    suffix = random_suffix()
    admin_username = f"admintranslate{suffix}"
    create_verified_user(
        db_session,
        email=f"admin-translate{suffix}@example.com",
        username=admin_username,
        password="AdminTranslate123!",
        full_name="Admin Translate",
        role_name="Admin",
    )
    admin_token = get_token(admin_username, "AdminTranslate123!")

    entry_response = client.post(
        "/api/v1/dictionary/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "language_id": english.id,
            "entry_type": "word",
            "term": "hello",
            "translation": "hola",
            "part_of_speech": "interjection",
            "example": "Hello there",
        },
    )
    assert entry_response.status_code == 201
    entry_data = entry_response.json()
    assert entry_data["term"] == "hello"

    translate_resp = client.post(
        "/api/v1/translate/",
        json={"source_language_id": english.id, "target_language_id": spanish.id, "text": "hello"},
    )
    assert translate_resp.status_code == 200
    translation_data = translate_resp.json()
    assert translation_data["translation"] == "hola"
    assert translation_data["source_language"]["id"] == english.id
    assert translation_data["target_language"]["id"] == spanish.id

    missing_resp = client.post(
        "/api/v1/translate/",
        json={"source_language_id": english.id, "target_language_id": spanish.id, "text": "missing-term"},
    )
    assert missing_resp.status_code == 200
    assert missing_resp.json()["translation"] is None
    assert "Translation not found" in missing_resp.json()["message"]
