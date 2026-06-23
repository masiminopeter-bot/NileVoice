from datetime import datetime, timedelta
from typing import Optional

from datetime import datetime, timedelta
from typing import Optional, Tuple

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.refresh_token import RefreshToken
from app.models.role import Role
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.core.security.jwt import create_access_token
from app.core.security.utils import generate_random_token

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = AuthRepository(db)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, email: str, username: str, password: str, full_name: Optional[str] = None) -> User:
        existing_user = self.repository.get_user_by_email(email) or self.repository.get_user_by_username(username)
        if existing_user:
            raise ValueError("Email or username already in use")

        verification_token = generate_random_token()
        role = self.get_or_create_role("Visitor", "Default visitor role")

        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=self.hash_password(password),
            email_verified=False,
            verification_token=verification_token,
            verification_sent_at=datetime.utcnow(),
            roles=[role],
        )
        return self.repository.create_user(user)

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.repository.get_user_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Inactive user")
        if not user.email_verified:
            raise ValueError("Email address is not verified")
        return user

    def authenticate_refresh_token(self, refresh_token: str) -> RefreshToken:
        token = self.repository.get_refresh_token(refresh_token)
        if not token or token.revoked or token.expires_at < datetime.utcnow():
            raise ValueError("Invalid refresh token")
        return token

    def create_tokens(self, user: User) -> Tuple[str, str]:
        access_token = create_access_token(subject=str(user.id))
        refresh_token_str = generate_random_token()
        expires_at = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expires_days)
        self.repository.create_refresh_token(user=user, token=refresh_token_str, expires_at=expires_at)
        return access_token, refresh_token_str

    def revoke_refresh_token(self, token: str) -> None:
        self.repository.revoke_refresh_token(token)

    def send_verification_email(self, user: User) -> None:
        # Placeholder: integrate with email service.
        pass

    def verify_email(self, token: str) -> User:
        user = self.repository.get_user_by_verification_token(token)
        if not user:
            raise ValueError("Invalid verification token")
        if not user.verification_sent_at:
            raise ValueError("Verification token expired")
        expiration = user.verification_sent_at + timedelta(hours=settings.email_verification_token_expires_hours)
        if datetime.utcnow() > expiration:
            raise ValueError("Verification token expired")
        user.email_verified = True
        user.verification_token = None
        user.verification_sent_at = None
        return self.repository.update_user(user)

    def create_password_reset(self, email: str) -> User:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("Email not found")
        user.reset_password_token = generate_random_token()
        user.reset_password_sent_at = datetime.utcnow()
        return self.repository.update_user(user)

    def reset_password(self, token: str, new_password: str) -> User:
        user = self.repository.get_user_by_reset_token(token)
        if not user or not user.reset_password_sent_at:
            raise ValueError("Invalid reset token")
        expiration = user.reset_password_sent_at + timedelta(hours=settings.password_reset_token_expires_hours)
        if datetime.utcnow() > expiration:
            raise ValueError("Reset token expired")
        user.hashed_password = self.hash_password(new_password)
        user.reset_password_token = None
        user.reset_password_sent_at = None
        return self.repository.update_user(user)

    def get_or_create_role(self, name: str, description: Optional[str] = None) -> Role:
        role = self.repository.get_role_by_name(name)
        if role:
            return role
        role = Role(name=name, description=description)
        self.repository.db.add(role)
        self.repository.db.commit()
        self.repository.db.refresh(role)
        return role
