from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class StudyGroup(Base):
    __tablename__ = "study_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=True)
    max_members = Column(Integer, default=10)
    is_public = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("StudyGroupMember", back_populates="group")
    messages = relationship("GroupMessage", back_populates="group")
    resources = relationship("GroupResource", back_populates="group")

class StudyGroupMember(Base):
    __tablename__ = "study_group_members"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default="member")  # member, moderator, admin
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relations
    group = relationship("StudyGroup", back_populates="members")
    user = relationship("User", foreign_keys=[user_id])

class GroupMessage(Base):
    __tablename__ = "group_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, file, image, link
    attachments = Column(JSON, nullable=True)  # Liste des fichiers attachés
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    group = relationship("StudyGroup", back_populates="messages")
    user = relationship("User", foreign_keys=[user_id])

class GroupResource(Base):
    __tablename__ = "group_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False)  # document, link, video, image
    file_url = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # en bytes
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    group = relationship("StudyGroup", back_populates="resources")
    uploader = relationship("User", foreign_keys=[uploaded_by])

class CollaborationProject(Base):
    __tablename__ = "collaboration_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=True)
    status = Column(String(20), default="active")  # active, completed, archived
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("ProjectMember", back_populates="project")
    tasks = relationship("ProjectTask", back_populates="project")

class ProjectMember(Base):
    __tablename__ = "project_members"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("collaboration_projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default="member")  # member, leader, contributor
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relations
    project = relationship("CollaborationProject", back_populates="members")
    user = relationship("User", foreign_keys=[user_id])

class ProjectTask(Base):
    __tablename__ = "project_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("collaboration_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    priority = Column(String(20), default="medium")  # low, medium, high
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    project = relationship("CollaborationProject", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assigned_to])
    creator = relationship("User", foreign_keys=[created_by]) 