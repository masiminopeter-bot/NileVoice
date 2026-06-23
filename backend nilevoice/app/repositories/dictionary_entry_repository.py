from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.dictionary_entry import DictionaryEntry


class DictionaryEntryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, entry_id: int) -> Optional[DictionaryEntry]:
        return self.db.query(DictionaryEntry).filter(DictionaryEntry.id == entry_id).one_or_none()

    def list(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        language_id: int | None = None,
        entry_type: str | None = None,
        verified: bool | None = None,
    ) -> tuple[list[DictionaryEntry], int]:
        query_builder = self.db.query(DictionaryEntry)
        if language_id is not None:
            query_builder = query_builder.filter(DictionaryEntry.language_id == language_id)
        if entry_type is not None:
            query_builder = query_builder.filter(DictionaryEntry.entry_type == entry_type)
        if verified is not None:
            query_builder = query_builder.filter(DictionaryEntry.is_verified == verified)
        if query:
            search_term = f"%{query.strip().lower()}%"
            query_builder = query_builder.filter(
                or_(
                    DictionaryEntry.term.ilike(search_term),
                    DictionaryEntry.translation.ilike(search_term),
                    DictionaryEntry.example.ilike(search_term),
                )
            )
        total = query_builder.count()
        items = (
            query_builder.order_by(DictionaryEntry.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total

    def create(self, entry: DictionaryEntry) -> DictionaryEntry:
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def update(self, entry: DictionaryEntry) -> DictionaryEntry:
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def delete(self, entry: DictionaryEntry) -> None:
        self.db.delete(entry)
        self.db.commit()
