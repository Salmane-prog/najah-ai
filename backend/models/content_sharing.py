from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class ContentSharing(Base):
    __tablename__ = "content_sharings"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    shared_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Teacher who shared
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Target configuration
    target_type = Column(String(20), nullable=False)  # 'class', 'student', 'all_students'
    target_ids = Column(JSON)  # Array of class_ids or student_ids
    
    # Sharing settings
    allow_download = Column(Boolean, default=True)
    allow_view = Column(Boolean, default=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    
    # Notification settings
    notify_students = Column(Boolean, default=True)
    custom_message = Column(Text, nullable=True)
    
    # Relationships
    content = relationship("Content", back_populates="sharings")
    shared_by_user = relationship("User", foreign_keys=[shared_by])
    
    # Statistics
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    student_count = Column(Integer, default=0)  # Number of students who can access

class ContentAccess(Base):
    __tablename__ = "content_accesses"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sharing_id = Column(Integer, ForeignKey("content_sharings.id"), nullable=False)
    
    # Access tracking
    first_accessed = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    access_count = Column(Integer, default=0)
    
    # Permissions
    can_view = Column(Boolean, default=True)
    can_download = Column(Boolean, default=True)
    
    # Relationships
    content = relationship("Content")
    student = relationship("User")
    sharing = relationship("ContentSharing")



