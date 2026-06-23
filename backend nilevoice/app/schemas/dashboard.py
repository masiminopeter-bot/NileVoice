from pydantic import BaseModel


class TranslatorDashboardResponse(BaseModel):
    total_submissions: int
    pending: int
    approved: int
    rejected: int


class AdminDashboardResponse(BaseModel):
    total_users: int
    total_translators: int
    total_languages: int
    total_dictionary_entries: int
    total_pending_reviews: int
