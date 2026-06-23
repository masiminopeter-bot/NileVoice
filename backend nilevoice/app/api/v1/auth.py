from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_db_session
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.core.security.auth import require_role

settings = get_settings()
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db_session)) -> UserResponse:
    service = AuthService(db)
    try:
        user = service.register_user(
            email=request.email,
            username=request.username,
            password=request.password,
            full_name=request.full_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db_session)) -> TokenResponse:
    service = AuthService(db)
    try:
        user = service.authenticate_user(request.username, request.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))

    access_token, refresh_token = service.create_tokens(user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db_session)) -> TokenResponse:
    service = AuthService(db)
    try:
        token = service.authenticate_refresh_token(request.refresh_token)
        access_token, refresh_token = service.create_tokens(token.user)
        service.revoke_refresh_token(request.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db_session)) -> dict:
    service = AuthService(db)
    try:
        service.create_password_reset(request.email)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return {"detail": "Password reset token created"}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db_session)) -> dict:
    service = AuthService(db)
    try:
        service.reset_password(request.token, request.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {"detail": "Password reset completed"}


@router.post("/verify-email")
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db_session)) -> dict:
    service = AuthService(db)
    try:
        service.verify_email(request.token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {"detail": "Email verified"}


@router.get("/admin-only")
def admin_only(user: User = Depends(require_role("Admin"))) -> dict:
    return {"detail": f"Hello, {user.username}. Admin access granted."}
