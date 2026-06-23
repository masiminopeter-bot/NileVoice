from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.core.security.auth import get_current_user, require_role
from app.schemas.translation_submission import (
    TranslationSubmissionCreate,
    TranslationSubmissionListResponse,
    TranslationSubmissionResponse,
    TranslationSubmissionReview,
    TranslationSubmissionUpdate,
)
from app.services.translation_submission_service import TranslationSubmissionService

router = APIRouter()


@router.post("/", response_model=TranslationSubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    payload: TranslationSubmissionCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> TranslationSubmissionResponse:
    if not any(role.name == "Translator" for role in user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Translator role required")
    service = TranslationSubmissionService(db)
    submission = service.create_submission(user.id, payload)
    return submission


@router.get("/", response_model=TranslationSubmissionListResponse)
def list_submissions(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    query: str | None = Query(None, min_length=1),
    status: str | None = Query(None),
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
) -> TranslationSubmissionListResponse:
    service = TranslationSubmissionService(db)
    items, total = service.list_submissions(page=page, size=size, query=query, status=status)
    return TranslationSubmissionListResponse(items=items, total=total, page=page, size=size, query=query, status=status)


@router.get("/{submission_id}", response_model=TranslationSubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
) -> TranslationSubmissionResponse:
    service = TranslationSubmissionService(db)
    submission = service.get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission


@router.put("/{submission_id}", response_model=TranslationSubmissionResponse)
def update_submission(
    submission_id: int,
    payload: TranslationSubmissionUpdate,
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
) -> TranslationSubmissionResponse:
    service = TranslationSubmissionService(db)
    submission = service.get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    if submission.user_id != user.id and not any(role.name == "Admin" for role in user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot edit another translator's submission")
    try:
        return service.update_submission(submission_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(
    submission_id: int,
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
) -> None:
    service = TranslationSubmissionService(db)
    submission = service.get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    if submission.user_id != user.id and not any(role.name == "Admin" for role in user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user's submission")
    service.delete_submission(submission_id)


@router.post("/{submission_id}/review", response_model=TranslationSubmissionResponse)
def review_submission(
    submission_id: int,
    payload: TranslationSubmissionReview,
    db: Session = Depends(get_db_session),
    user=Depends(require_role("Admin")),
) -> TranslationSubmissionResponse:
    service = TranslationSubmissionService(db)
    try:
        return service.review_submission(submission_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
