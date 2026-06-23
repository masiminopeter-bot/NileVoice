from typing import Optional

from sqlalchemy.orm import Session

from app.models.dictionary_entry import DictionaryEntry
from app.repositories.dictionary_entry_repository import DictionaryEntryRepository
from app.schemas.dictionary_entry import DictionaryEntryCreate, DictionaryEntryUpdate


class DictionaryEntryService:
    def __init__(self, db: Session) -> None:
        self.repository = DictionaryEntryRepository(db)

    def get_entry(self, entry_id: int) -> Optional[DictionaryEntry]:
        return self.repository.get(entry_id)

    def list_entries(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        language_id: int | None = None,
        entry_type: str | None = None,
        verified: bool | None = None,
    ) -> tuple[list[DictionaryEntry], int]:
        return self.repository.list(
            page=page,
            size=size,
            query=query,
            language_id=language_id,
            entry_type=entry_type,
            verified=verified,
        )

    def create_entry(self, payload: DictionaryEntryCreate) -> DictionaryEntry:
        entry = DictionaryEntry(
            language_id=payload.language_id,
            entry_type=payload.entry_type,
            term=payload.term,
            translation=payload.translation,
            part_of_speech=payload.part_of_speech,
            example=payload.example,
            is_verified=True,
        )
        return self.repository.create(entry)

    def update_entry(self, entry_id: int, payload: DictionaryEntryUpdate) -> DictionaryEntry:
        entry = self.repository.get(entry_id)
        if not entry:
            raise ValueError("Dictionary entry not found")
        if payload.entry_type is not None:
            entry.entry_type = payload.entry_type
        if payload.term is not None:
            entry.term = payload.term
        if payload.translation is not None:
            entry.translation = payload.translation
        if payload.part_of_speech is not None:
            entry.part_of_speech = payload.part_of_speech
        if payload.example is not None:
            entry.example = payload.example
        if payload.is_verified is not None:
            entry.is_verified = payload.is_verified
        return self.repository.update(entry)

    def delete_entry(self, entry_id: int) -> None:
        entry = self.repository.get(entry_id)
        if not entry:
            raise ValueError("Dictionary entry not found")
        self.repository.delete(entry)
