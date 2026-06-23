from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.contact import Contact


class ContactRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, contact_id: int) -> Optional[Contact]:
        return self.db.query(Contact).filter(Contact.id == contact_id).one_or_none()

    def list(
        self,
        page: int = 1,
        size: int = 25,
        query: str | None = None,
        resolved: bool | None = None,
    ) -> tuple[list[Contact], int]:
        query_builder = self.db.query(Contact)
        if resolved is not None:
            query_builder = query_builder.filter(Contact.is_resolved == resolved)
        if query:
            search_term = f"%{query.strip().lower()}%"
            query_builder = query_builder.filter(
                or_(
                    Contact.name.ilike(search_term),
                    Contact.email.ilike(search_term),
                    Contact.subject.ilike(search_term),
                    Contact.message.ilike(search_term),
                )
            )
        total = query_builder.count()
        items = (
            query_builder.order_by(Contact.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total

    def create(self, contact: Contact) -> Contact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def update(self, contact: Contact) -> Contact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete(self, contact: Contact) -> None:
        self.db.delete(contact)
        self.db.commit()
