from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.translation_service import TranslationService

router = APIRouter()


@router.post("/", response_model=TranslationResponse, status_code=status.HTTP_200_OK)
def translate_text(payload: TranslationRequest, db: Session = Depends(get_db_session)) -> TranslationResponse:
    service = TranslationService(db)
    response = service.translate(payload)
    return response
