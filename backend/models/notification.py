from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum

class NotificationType(enum.Enum):
    QUIZ_COMPLETED = "quiz_completed"
    BADGE_EARNED = "badge_earned"
    ASSIGNMENT_DUE = "assignment_due"
    GRADE_POSTED = "grade_posted"
    SYSTEM_ALERT = "system_alert"
    TEACHER_MESSAGE = "teacher_message"
    STUDENT_MESSAGE = "student_message"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    CHALLENGE_COMPLETED = "challenge_completed"
    LEARNING_REMINDER = "learning_reminder"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    icon = Column(String(50), nullable=True)  # Ajout de la colonne icon
    points_reward = Column(Integer, default=0)  # Ajout de la colonne points_reward
    is_read = Column(Boolean, default=False)
    is_important = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    user = relationship("User", foreign_keys=[user_id], viewonly=True)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type})>" 