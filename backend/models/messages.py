from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    thread_id = Column(Integer, ForeignKey("threads.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    
    # Relations
    thread = relationship("Thread", foreign_keys=[thread_id], viewonly=True)
    user = relationship("User", foreign_keys=[user_id], viewonly=True) 