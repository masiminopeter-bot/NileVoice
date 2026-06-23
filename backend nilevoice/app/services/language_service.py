from typing import Optional

from sqlalchemy.orm import Session

from app.models.language import Language
from app.repositories.language_repository import LanguageRepository
from app.schemas.language import LanguageCreate, LanguageUpdate


class LanguageService:
    def __init__(self, db: Session) -> None:
        self.repository = LanguageRepository(db)

    def get_language(self, language_id: int) -> Optional[Language]:
        return self.repository.get(language_id)

    def list_languages(self, page: int = 1, size: int = 25, query: str | None = None) -> tuple[list[Language], int]:
        return self.repository.list(page=page, size=size, query=query)

    def create_language(self, payload: LanguageCreate) -> Language:
        if self.repository.get_by_code(payload.code):
            raise ValueError("Language code already exists")

        language = Language(
            code=payload.code,
            name=payload.name,
            native_name=payload.native_name,
            is_active=payload.is_active,
            description=payload.description,
        )
        return self.repository.create(language)

    def update_language(self, language_id: int, payload: LanguageUpdate) -> Language:
        language = self.repository.get(language_id)
        if not language:
            raise ValueError("Language not found")

        if payload.code and payload.code != language.code:
            if self.repository.get_by_code(payload.code):
                raise ValueError("Language code already exists")
            language.code = payload.code
        if payload.name is not None:
            language.name = payload.name
        if payload.native_name is not None:
            language.native_name = payload.native_name
        if payload.is_active is not None:
            language.is_active = payload.is_active
        if payload.description is not None:
            language.description = payload.description

        return self.repository.update(language)

    def delete_language(self, language_id: int) -> None:
        language = self.repository.get(language_id)
        if not language:
            raise ValueError("Language not found")
        self.repository.delete(language)
