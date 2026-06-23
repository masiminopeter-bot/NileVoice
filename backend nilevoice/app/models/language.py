from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.sql import func


class Language(Base):
    __tablename__ = "languages"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(16), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False, index=True)
    native_name = Column(String(128), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now())

    source_submissions = relationship(
        "TranslationSubmission",
        back_populates="source_language",
        foreign_keys="TranslationSubmission.source_language_id",
    )
    target_submissions = relationship(
        "TranslationSubmission",
        back_populates="target_language",
        foreign_keys="TranslationSubmission.target_language_id",
    )
    dictionary_entries = relationship("DictionaryEntry", back_populates="language")
