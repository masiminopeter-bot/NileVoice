from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.sql import func

EntryType = Enum("word", "phrase", "sentence", name="dictionary_entry_type")


class DictionaryEntry(Base):
    __tablename__ = "dictionary_entries"
    __table_args__ = (
        UniqueConstraint("language_id", "term", "translation", name="uq_dictionary_entry_term_translation"),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True)
    entry_type = Column(EntryType, nullable=False, server_default="word", index=True)
    term = Column(String(255), nullable=False, index=True)
    translation = Column(String(255), nullable=False, index=True)
    part_of_speech = Column(String(50), nullable=True)
    example = Column(Text, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False, server_default="0")
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now())

    language = relationship("Language", back_populates="dictionary_entries")
    created_by = relationship("User", back_populates="dictionary_entries")
