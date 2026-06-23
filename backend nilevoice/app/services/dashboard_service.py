from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.language import Language
from app.models.user import User
from app.models.dictionary_entry import DictionaryEntry
from app.models.translation_submission import TranslationSubmission


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def translator_dashboard(self) -> dict:
        total = self.db.query(func.count(TranslationSubmission.id)).scalar() or 0
        pending = self.db.query(func.count(TranslationSubmission.id)).filter(TranslationSubmission.status == "pending").scalar() or 0
        approved = self.db.query(func.count(TranslationSubmission.id)).filter(TranslationSubmission.status == "approved").scalar() or 0
        rejected = self.db.query(func.count(TranslationSubmission.id)).filter(TranslationSubmission.status == "rejected").scalar() or 0
        return {
            "total_submissions": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }

    def admin_dashboard(self) -> dict:
        total_users = self.db.query(func.count(User.id)).scalar() or 0
        total_translators = (
            self.db.query(func.count(User.id))
            .join(User.roles)
            .filter(User.roles.any(name="Translator"))
            .scalar() or 0
        )
        total_languages = self.db.query(func.count(Language.id)).scalar() or 0
        total_dictionary_entries = self.db.query(func.count(DictionaryEntry.id)).scalar() or 0
        total_pending_reviews = self.db.query(func.count(TranslationSubmission.id)).filter(TranslationSubmission.status == "pending").scalar() or 0
        return {
            "total_users": total_users,
            "total_translators": total_translators,
            "total_languages": total_languages,
            "total_dictionary_entries": total_dictionary_entries,
            "total_pending_reviews": total_pending_reviews,
        }
