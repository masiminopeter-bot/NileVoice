from typing import Optional

from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate, ContactUpdate


class ContactService:
    def __init__(self, db: Session) -> None:
        self.repository = ContactRepository(db)

    def get_contact(self, contact_id: int) -> Optional[Contact]:
        return self.repository.get(contact_id)

    def list_contacts(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        resolved: bool | None = None,
    ) -> tuple[list[Contact], int]:
        return self.repository.list(page=page, size=size, query=query, resolved=resolved)

    def create_contact(self, user_id: int | None, payload: ContactCreate) -> Contact:
        contact = Contact(
            user_id=user_id,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            subject=payload.subject,
            message=payload.message,
            is_resolved=False,
        )
        return self.repository.create(contact)

    def update_contact(self, contact_id: int, payload: ContactUpdate) -> Contact:
        contact = self.repository.get(contact_id)
        if not contact:
            raise ValueError("Contact not found")
        if payload.name is not None:
            contact.name = payload.name
        if payload.email is not None:
            contact.email = payload.email
        if payload.subject is not None:
            contact.subject = payload.subject
        if payload.message is not None:
            contact.message = payload.message
        if payload.phone is not None:
            contact.phone = payload.phone
        if payload.is_resolved is not None:
            contact.is_resolved = payload.is_resolved
        return self.repository.update(contact)

    def delete_contact(self, contact_id: int) -> None:
        contact = self.repository.get(contact_id)
        if not contact:
            raise ValueError("Contact not found")
        self.repository.delete(contact)
