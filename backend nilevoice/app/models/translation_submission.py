from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.sql import func

SubmissionStatus = Enum("pending", "approved", "rejected", name="submission_status")
SubmissionType = Enum("word", "phrase", "sentence", name="submission_type")


class TranslationSubmission(Base):
    __tablename__ = "translation_submissions"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_language_id = Column(
        Integer,
        ForeignKey("languages.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    target_language_id = Column(
        Integer,
        ForeignKey("languages.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    submission_type = Column(SubmissionType, nullable=False, server_default="word")
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)
    status = Column(SubmissionStatus, nullable=False, server_default="pending", index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="submissions")
    source_language = relationship("Language", foreign_keys=[source_language_id], back_populates="source_submissions")
    target_language = relationship("Language", foreign_keys=[target_language_id], back_populates="target_submissions")
