from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from core.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Relations - Commentées temporairement pour éviter les erreurs circulaires
    # contents = relationship("Content", back_populates="category")