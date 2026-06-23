from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, constr


SubmissionType = Literal["word", "phrase", "sentence"]
SubmissionStatus = Literal["pending", "approved", "rejected"]


class TranslationSubmissionBase(BaseModel):
    source_language_id: int
    target_language_id: int
    submission_type: SubmissionType = Field(..., description="Type of submission: word, phrase, or sentence")
    original_text: constr(strip_whitespace=True, min_length=1, max_length=2000)
    translated_text: Optional[constr(strip_whitespace=True, min_length=1, max_length=2000)] = None
    notes: Optional[str] = None


class TranslationSubmissionCreate(TranslationSubmissionBase):
    pass


class TranslationSubmissionUpdate(BaseModel):
    submission_type: Optional[SubmissionType] = None
    original_text: Optional[constr(strip_whitespace=True, min_length=1, max_length=2000)] = None
    translated_text: Optional[constr(strip_whitespace=True, min_length=1, max_length=2000)] = None
    notes: Optional[str] = None


class TranslationSubmissionReview(BaseModel):
    status: SubmissionStatus
    reviewer_notes: Optional[str] = None


class TranslationSubmissionResponse(TranslationSubmissionBase):
    id: int
    user_id: int
    status: SubmissionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TranslationSubmissionListResponse(BaseModel):
    items: list[TranslationSubmissionResponse]
    total: int
    page: int
    size: int
    query: Optional[str] = None
    status: Optional[SubmissionStatus] = None
