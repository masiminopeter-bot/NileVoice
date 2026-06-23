from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user_roles import user_roles
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(80), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False, server_default="0")
    verification_token = Column(String(128), nullable=True, unique=True, index=True)
    verification_sent_at = Column(DateTime(timezone=False), nullable=True)
    reset_password_token = Column(String(128), nullable=True, unique=True, index=True)
    reset_password_sent_at = Column(DateTime(timezone=False), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    is_superuser = Column(Boolean, nullable=False, default=False, server_default="0")
    last_login_at = Column(DateTime(timezone=False), nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now())

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    submissions = relationship("TranslationSubmission", back_populates="user", cascade="all, delete-orphan")
    dictionary_entries = relationship("DictionaryEntry", back_populates="created_by")
    contacts = relationship("Contact", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
