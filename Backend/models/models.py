import enum

from sqlalchemy import (JSON, TIMESTAMP, Column, Enum, ForeignKey, Index, Integer,
                        String)
from sqlalchemy.sql import func

from models.database import Base


class PDFText(Base):
    __tablename__ = "pdf_text"
    __table_args__ = (
        Index("idx_pdf_text_id", "id", unique=True, postgresql_using="btree"),
    )

    class STATUS(enum.Enum):
        ACTIVE = 1
        INACTIVE = 2

    id = Column(Integer, primary_key=True, index=True)
    text = Column(JSON, nullable=False)
    processed_text = Column(JSON, nullable=False)
    context = Column(String, nullable=True)
    status = Column(Enum(STATUS, name="pdf_status_status"), default=STATUS.ACTIVE)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class ChatMessages(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("idx_chat_messages_pdf_text_id", "pdf_text_id", postgresql_using="btree"),
        Index("idx_chat_messages_type", "message_type", postgresql_using="btree"),
        Index("idx_chat_messages_status", "status", postgresql_using="btree"),
    )

    class MESSAGE_TYPE(enum.Enum):
        SYSTEM = 1
        USER = 2

    class STATUS(enum.Enum):
        ACTIVE = 1
        INACTIVE = 2

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    message_type = Column(Enum(MESSAGE_TYPE, name="chat_messages_type"))
    pdf_text_id = Column(
        Integer, ForeignKey("pdf_text.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(Enum(STATUS, name="chat_messages_status"), default=STATUS.ACTIVE)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
