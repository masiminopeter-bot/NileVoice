from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.schemas.language import (
    LanguageCreate,
    LanguageListResponse,
    LanguageResponse,
    LanguageUpdate,
)
from app.services.language_service import LanguageService

router = APIRouter()


@router.post("/", response_model=LanguageResponse, status_code=status.HTTP_201_CREATED)
def create_language(payload: LanguageCreate, db: Session = Depends(get_db_session)) -> LanguageResponse:
    service = LanguageService(db)
    try:
        language = service.create_language(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return language


@router.get("/", response_model=LanguageListResponse)
def list_languages(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    query: str | None = Query(None, min_length=1),
    db: Session = Depends(get_db_session),
) -> LanguageListResponse:
    service = LanguageService(db)
    items, total = service.list_languages(page=page, size=size, query=query)
    return LanguageListResponse(items=items, total=total, page=page, size=size, query=query)


@router.get("/{language_id}", response_model=LanguageResponse)
def get_language(language_id: int, db: Session = Depends(get_db_session)) -> LanguageResponse:
    service = LanguageService(db)
    language = service.get_language(language_id)
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language not found")
    return language


@router.put("/{language_id}", response_model=LanguageResponse)
def update_language(
    language_id: int,
    payload: LanguageUpdate,
    db: Session = Depends(get_db_session),
) -> LanguageResponse:
    service = LanguageService(db)
    try:
        language = service.update_language(language_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return language


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language(language_id: int, db: Session = Depends(get_db_session)) -> None:
    service = LanguageService(db)
    try:
        service.delete_language(language_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
