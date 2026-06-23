from typing import Optional

from sqlalchemy.orm import Session

from app.models.language import Language
from app.models.dictionary_entry import DictionaryEntry
from app.schemas.translation import TranslationRequest, TranslationResponse


class TranslationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def translate(self, payload: TranslationRequest) -> TranslationResponse:
        source_language = self.db.query(Language).filter(Language.id == payload.source_language_id).one_or_none()
        target_language = self.db.query(Language).filter(Language.id == payload.target_language_id).one_or_none()

        if not source_language or not target_language:
            return TranslationResponse(
                translation=None,
                source_language=source_language or Language(id=payload.source_language_id, code="", name="Unknown", native_name=None),
                target_language=target_language or Language(id=payload.target_language_id, code="", name="Unknown", native_name=None),
                message="Source or target language not found.",
            )

        entry = (
            self.db.query(DictionaryEntry)
            .filter(DictionaryEntry.language_id == payload.source_language_id)
            .filter(DictionaryEntry.is_verified == True)
            .filter(DictionaryEntry.term.ilike(payload.text.strip()))
            .first()
        )

        if entry and entry.translation:
            return TranslationResponse(
                translation=entry.translation,
                source_language=source_language,
                target_language=target_language,
            )

        return TranslationResponse(
            translation=None,
            source_language=source_language,
            target_language=target_language,
            message="Translation not found. Please try a different phrase or ensure the entry exists in the approved dictionary.",
        )
