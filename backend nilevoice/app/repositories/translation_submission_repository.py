from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.translation_submission import TranslationSubmission


class TranslationSubmissionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, submission_id: int) -> Optional[TranslationSubmission]:
        return self.db.query(TranslationSubmission).filter(TranslationSubmission.id == submission_id).one_or_none()

    def list(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        status: str | None = None,
    ) -> tuple[list[TranslationSubmission], int]:
        query_builder = self.db.query(TranslationSubmission)
        if status:
            query_builder = query_builder.filter(TranslationSubmission.status == status)
        if query:
            search_term = f"%{query.strip().lower()}%"
            query_builder = query_builder.filter(
                or_(
                    TranslationSubmission.original_text.ilike(search_term),
                    TranslationSubmission.translated_text.ilike(search_term),
                    TranslationSubmission.notes.ilike(search_term),
                )
            )
        total = query_builder.count()
        items = (
            query_builder.order_by(TranslationSubmission.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total

    def create(self, submission: TranslationSubmission) -> TranslationSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def update(self, submission: TranslationSubmission) -> TranslationSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def delete(self, submission: TranslationSubmission) -> None:
        self.db.delete(submission)
        self.db.commit()
