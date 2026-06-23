from pydantic import BaseModel, constr


class TranslationRequest(BaseModel):
    source_language_id: int
    target_language_id: int
    text: constr(strip_whitespace=True, min_length=1, max_length=2000)


class LanguageSummary(BaseModel):
    id: int
    code: str
    name: str
    native_name: str | None = None

    class Config:
        orm_mode = True


class TranslationResponse(BaseModel):
    translation: str | None = None
    source_language: LanguageSummary
    target_language: LanguageSummary
    message: str | None = None

    class Config:
        orm_mode = True
