from typing import Optional

from sqlalchemy.orm import Session

from app.models.translation_submission import TranslationSubmission
from app.repositories.translation_submission_repository import TranslationSubmissionRepository
from app.schemas.translation_submission import (
    TranslationSubmissionCreate,
    TranslationSubmissionReview,
    TranslationSubmissionUpdate,
)


class TranslationSubmissionService:
    def __init__(self, db: Session) -> None:
        self.repository = TranslationSubmissionRepository(db)

    def get_submission(self, submission_id: int) -> Optional[TranslationSubmission]:
        return self.repository.get(submission_id)

    def list_submissions(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        status: str | None = None,
    ) -> tuple[list[TranslationSubmission], int]:
        return self.repository.list(page=page, size=size, query=query, status=status)

    def create_submission(self, user_id: int, payload: TranslationSubmissionCreate) -> TranslationSubmission:
        submission = TranslationSubmission(
            user_id=user_id,
            source_language_id=payload.source_language_id,
            target_language_id=payload.target_language_id,
            submission_type=payload.submission_type,
            source_text=payload.original_text,
            translated_text=payload.translated_text,
            notes=payload.notes,
        )
        return self.repository.create(submission)

    def update_submission(self, submission_id: int, payload: TranslationSubmissionUpdate) -> TranslationSubmission:
        submission = self.repository.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        if payload.submission_type is not None:
            submission.submission_type = payload.submission_type
        if payload.original_text is not None:
            submission.source_text = payload.original_text
        if payload.translated_text is not None:
            submission.translated_text = payload.translated_text
        if payload.notes is not None:
            submission.notes = payload.notes
        return self.repository.update(submission)

    def delete_submission(self, submission_id: int) -> None:
        submission = self.repository.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        self.repository.delete(submission)

    def review_submission(self, submission_id: int, payload: TranslationSubmissionReview) -> TranslationSubmission:
        submission = self.repository.get(submission_id)
        if not submission:
            raise ValueError("Submission not found")
        submission.status = payload.status
        if payload.reviewer_notes is not None:
            submission.notes = payload.reviewer_notes
        return self.repository.update(submission)
