from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.sql import func


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    issued_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=False), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False, server_default="0")
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")
