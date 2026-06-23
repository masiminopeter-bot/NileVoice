from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.language import Language


class LanguageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, language_id: int) -> Optional[Language]:
        return self.db.query(Language).filter(Language.id == language_id).one_or_none()

    def get_by_code(self, code: str) -> Optional[Language]:
        return self.db.query(Language).filter(Language.code == code).one_or_none()

    def list(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
    ) -> tuple[list[Language], int]:
        query_builder = self.db.query(Language)
        if query:
            query_lower = f"%{query.strip().lower()}%"
            query_builder = query_builder.filter(
                or_(
                    Language.name.ilike(query_lower),
                    Language.code.ilike(query_lower),
                    Language.native_name.ilike(query_lower),
                    Language.description.ilike(query_lower),
                )
            )
        total = query_builder.count()
        items = (
            query_builder.order_by(Language.name.asc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total

    def create(self, language: Language) -> Language:
        self.db.add(language)
        self.db.commit()
        self.db.refresh(language)
        return language

    def update(self, language: Language) -> Language:
        self.db.add(language)
        self.db.commit()
        self.db.refresh(language)
        return language

    def delete(self, language: Language) -> None:
        self.db.delete(language)
        self.db.commit()
