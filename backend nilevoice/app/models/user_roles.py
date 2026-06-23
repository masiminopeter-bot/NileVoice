from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
)
