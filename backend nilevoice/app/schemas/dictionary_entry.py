from typing import Literal, Optional

from pydantic import BaseModel, constr


EntryType = Literal["word", "phrase", "sentence"]


class DictionaryEntryBase(BaseModel):
    language_id: int
    entry_type: EntryType = "word"
    term: constr(strip_whitespace=True, min_length=1, max_length=255)
    translation: constr(strip_whitespace=True, min_length=1, max_length=255)
    part_of_speech: Optional[constr(strip_whitespace=True, max_length=50)] = None
    example: Optional[str] = None


class DictionaryEntryCreate(DictionaryEntryBase):
    pass


class DictionaryEntryUpdate(BaseModel):
    entry_type: Optional[EntryType] = None
    term: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    translation: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    part_of_speech: Optional[constr(strip_whitespace=True, max_length=50)] = None
    example: Optional[str] = None
    is_verified: Optional[bool] = None


class DictionaryEntryResponse(DictionaryEntryBase):
    id: int
    is_verified: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class DictionaryEntryListResponse(BaseModel):
    items: list[DictionaryEntryResponse]
    total: int
    page: int
    size: int
    query: Optional[str] = None
    language_id: Optional[int] = None
    entry_type: Optional[EntryType] = None
    verified: Optional[bool] = None
