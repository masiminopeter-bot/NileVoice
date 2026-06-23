from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.sql import func

AuditActionType = Enum(
    "create",
    "update",
    "delete",
    "login",
    "logout",
    "token_refresh",
    name="audit_action_type",
)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(AuditActionType, nullable=False)
    resource_type = Column(String(128), nullable=True)
    resource_id = Column(String(128), nullable=True)
    changes = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="audit_logs")
