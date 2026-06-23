from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.role import Role
from app.models.user import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).one_or_none()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).one_or_none()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).one_or_none()

    def get_user_by_verification_token(self, token: str) -> Optional[User]:
        return self.db.query(User).filter(User.verification_token == token).one_or_none()

    def get_user_by_reset_token(self, token: str) -> Optional[User]:
        return self.db.query(User).filter(User.reset_password_token == token).one_or_none()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_role_by_name(self, name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == name).one_or_none()

    def create_refresh_token(self, user: User, token: str, expires_at: datetime) -> RefreshToken:
        refresh_token = RefreshToken(user_id=user.id, token=token, expires_at=expires_at)
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def revoke_refresh_token(self, token: str) -> Optional[RefreshToken]:
        refresh_token = self.db.query(RefreshToken).filter(RefreshToken.token == token).one_or_none()
        if refresh_token:
            refresh_token.revoked = True
            self.db.add(refresh_token)
            self.db.commit()
            self.db.refresh(refresh_token)
        return refresh_token

    def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).one_or_none()

    def list_roles(self) -> list[Role]:
        return self.db.query(Role).all()
