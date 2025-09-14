from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class ResourceRating(Base):
    __tablename__ = "resource_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, nullable=False)
    resource_type = Column(String(50), nullable=False)  # 'quiz', 'content'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="resource_ratings") 