from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.core.security.auth import get_current_user, require_role
from app.schemas.contact import ContactCreate, ContactListResponse, ContactResponse, ContactUpdate
from app.services.contact_service import ContactService

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    db: Session = Depends(get_db_session),
) -> ContactResponse:
    service = ContactService(db)
    contact = service.create_contact(None, payload)
    return contact


@router.get("/", response_model=ContactListResponse)
def list_contacts(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    query: str | None = Query(None, min_length=1),
    resolved: bool | None = Query(None),
    db: Session = Depends(get_db_session),
    user=Depends(require_role("Admin")),
) -> ContactListResponse:
    service = ContactService(db)
    items, total = service.list_contacts(page=page, size=size, query=query, resolved=resolved)
    return ContactListResponse(items=items, total=total, page=page, size=size, query=query, resolved=resolved)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db_session), user=Depends(require_role("Admin"))) -> ContactResponse:
    service = ContactService(db)
    contact = service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    payload: ContactUpdate,
    db: Session = Depends(get_db_session),
    user=Depends(require_role("Admin")),
) -> ContactResponse:
    service = ContactService(db)
    try:
        return service.update_contact(contact_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db_session), user=Depends(require_role("Admin"))) -> None:
    service = ContactService(db)
    try:
        service.delete_contact(contact_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
