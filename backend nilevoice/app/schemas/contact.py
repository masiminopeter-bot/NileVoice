from typing import Optional

from pydantic import BaseModel, constr


class ContactCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=255)
    email: constr(strip_whitespace=True, min_length=5, max_length=255)
    subject: constr(strip_whitespace=True, min_length=1, max_length=255)
    message: constr(strip_whitespace=True, min_length=1, max_length=5000)
    phone: Optional[constr(strip_whitespace=True, max_length=50)] = None


class ContactUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    email: Optional[constr(strip_whitespace=True, min_length=5, max_length=255)] = None
    subject: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    message: Optional[constr(strip_whitespace=True, min_length=1, max_length=5000)] = None
    phone: Optional[constr(strip_whitespace=True, max_length=50)] = None
    is_resolved: Optional[bool] = None


class ContactResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None
    is_resolved: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class ContactListResponse(BaseModel):
    items: list[ContactResponse]
    total: int
    page: int
    size: int
    query: Optional[str] = None
    resolved: Optional[bool] = None
