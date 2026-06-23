from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.core.security.auth import get_current_user, require_role
from app.schemas.dashboard import AdminDashboardResponse, TranslatorDashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/translator", response_model=TranslatorDashboardResponse)
def translator_dashboard(db: Session = Depends(get_db_session), user=Depends(get_current_user)) -> TranslatorDashboardResponse:
    service = DashboardService(db)
    summary = service.translator_dashboard()
    return TranslatorDashboardResponse(**summary)


@router.get("/admin", response_model=AdminDashboardResponse)
def admin_dashboard(db: Session = Depends(get_db_session), user=Depends(require_role("Admin"))) -> AdminDashboardResponse:
    service = DashboardService(db)
    summary = service.admin_dashboard()
    return AdminDashboardResponse(**summary)
