from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.language import router as language_router
from app.api.v1.translation_submission import router as submission_router
from app.api.v1.dictionary_entry import router as dictionary_router
from app.api.v1.translate import router as translate_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.contact import router as contact_router

router = APIRouter()
router.include_router(health_router, prefix="", tags=["Health"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(language_router, prefix="/languages", tags=["Languages"])
router.include_router(submission_router, prefix="/submissions", tags=["Submissions"])
router.include_router(dictionary_router, prefix="/dictionary", tags=["Dictionary"])
router.include_router(translate_router, prefix="/translate", tags=["Translate"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(contact_router, prefix="/contacts", tags=["Contacts"])
