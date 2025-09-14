from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    criteria = Column(Text, nullable=True)  # Règle d'attribution (texte ou JSON)
    image_url = Column(String, nullable=True)
    secret = Column(Boolean, default=False, nullable=False)
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badge"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    progression = Column(Float, default=1.0, nullable=False)  # 1.0 = badge obtenu, <1 = progression
    awarded_at = Column(DateTime, nullable=True)
    badge = relationship("Badge", back_populates="user_badges")
    user = relationship("User", foreign_keys=[user_id], viewonly=True)