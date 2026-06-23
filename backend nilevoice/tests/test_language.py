import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.models.language import Language

client = TestClient(app)


def random_suffix() -> str:
    return uuid.uuid4().hex[:8]


def ensure_language(db: Session, code: str, name: str, native_name: str | None = None) -> Language:
    language = db.query(Language).filter(Language.code == code).one_or_none()
    if not language:
        language = Language(code=code, name=name, native_name=native_name)
        db.add(language)
        db.commit()
        db.refresh(language)
    return language


def test_language_crud_lifecycle():
    suffix = random_suffix()
    code = f"lg{suffix}"
    name = f"Language {suffix}"

    create_resp = client.post(
        "/api/v1/languages/",
        json={"code": code, "name": name, "native_name": "Lang", "description": "Test language"},
    )
    assert create_resp.status_code == 201
    language = create_resp.json()
    assert language["code"] == code
    assert language["name"] == name

    list_resp = client.get(
        "/api/v1/languages/",
        params={"query": code},
    )
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["total"] >= 1
    assert any(item["id"] == language["id"] for item in list_data["items"])

    get_resp = client.get(f"/api/v1/languages/{language['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["code"] == code

    new_name = f"Updated {name}"
    update_resp = client.put(
        f"/api/v1/languages/{language['id']}",
        json={"name": new_name, "description": "Updated description"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == new_name

    delete_resp = client.delete(f"/api/v1/languages/{language['id']}")
    assert delete_resp.status_code == 204

    get_deleted_resp = client.get(f"/api/v1/languages/{language['id']}")
    assert get_deleted_resp.status_code == 404
