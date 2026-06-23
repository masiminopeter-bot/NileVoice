from typing import List, Optional

from pydantic import BaseModel, Field, constr


class LanguageBase(BaseModel):
    code: constr(strip_whitespace=True, min_length=2, max_length=16)
    name: constr(strip_whitespace=True, min_length=2, max_length=128)
    native_name: Optional[constr(strip_whitespace=True, max_length=128)] = None
    is_active: Optional[bool] = True
    description: Optional[str] = None


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(BaseModel):
    code: Optional[constr(strip_whitespace=True, min_length=2, max_length=16)] = None
    name: Optional[constr(strip_whitespace=True, min_length=2, max_length=128)] = None
    native_name: Optional[constr(strip_whitespace=True, max_length=128)] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class LanguageResponse(LanguageBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class LanguageListResponse(BaseModel):
    items: List[LanguageResponse]
    total: int
    page: int
    size: int
    query: Optional[str]
