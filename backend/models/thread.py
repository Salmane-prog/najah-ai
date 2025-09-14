from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Thread(Base):
    __tablename__ = "threads"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    type = Column(String, nullable=True)  # général, classe, privé, etc.
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by], viewonly=True)
    messages = relationship("Message", back_populates="thread") 