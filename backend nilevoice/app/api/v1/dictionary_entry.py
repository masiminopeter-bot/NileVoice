from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.core.security.auth import get_current_user, require_role
from app.schemas.dictionary_entry import (
    DictionaryEntryCreate,
    DictionaryEntryListResponse,
    DictionaryEntryResponse,
    DictionaryEntryUpdate,
)
from app.services.dictionary_entry_service import DictionaryEntryService

router = APIRouter()


@router.post("/", response_model=DictionaryEntryResponse, status_code=status.HTTP_201_CREATED)
def create_dictionary_entry(
    payload: DictionaryEntryCreate,
    db: Session = Depends(get_db_session),
    user=Depends(require_role("Admin")),
) -> DictionaryEntryResponse:
    service = DictionaryEntryService(db)
    try:
        entry = service.create_entry(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return entry


@router.get("/", response_model=DictionaryEntryListResponse)
def list_dictionary_entries(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    query: str | None = Query(None, min_length=1),
    language_id: int | None = Query(None, alias="languageId"),
    entry_type: str | None = Query(None, alias="entryType"),
    verified: bool | None = Query(None, alias="verified"),
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
) -> DictionaryEntryListResponse:
    service = DictionaryEntryService(db)
    items, total = service.list_entries(
        page=page,
        size=size,
        query=query,
        language_id=language_id,
        entry_type=entry_type,
        verified=verified,
    )
    return DictionaryEntryListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        query=query,
        language_id=language_id,
        entry_type=entry_type,
        verified=verified,
    )


@router.get("/{entry_id}", response_model=DictionaryEntryResponse)
def get_dictionary_entry(entry_id: int, db: Session = Depends(get_db_session), user=Depends(get_current_user)) -> DictionaryEntryResponse:
    service = DictionaryEntryService(db)
    entry = service.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dictionary entry not found")
    return entry


@router.put("/{entry_id}", response_model=DictionaryEntryResponse)
def update_dictionary_entry(
    entry_id: int,
    payload: DictionaryEntryUpdate,
    db: Session = Depends(get_db_session),
    user=Depends(require_role("Admin")),
) -> DictionaryEntryResponse:
    service = DictionaryEntryService(db)
    try:
        entry = service.update_entry(entry_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dictionary_entry(entry_id: int, db: Session = Depends(get_db_session), user=Depends(require_role("Admin"))) -> None:
    service = DictionaryEntryService(db)
    try:
        service.delete_entry(entry_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
