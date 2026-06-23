from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    refresh_token: Optional[str]


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str]


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class VerifyEmailRequest(BaseModel):
    token: str
