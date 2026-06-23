from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class RoleSchema(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str]
    email_verified: bool
    is_active: bool
    is_superuser: bool
    roles: List[RoleSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
