from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class NoteTag(Base):
    __tablename__ = "note_tags"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    tag = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    note = relationship("UserNote", foreign_keys=[note_id])

class NoteShare(Base):
    __tablename__ = "note_shares"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    shared_by = Column(Integer, ForeignKey("users.id"))
    shared_with = Column(Integer, ForeignKey("users.id"))
    permission = Column(String(20), default="read")  # 'read', 'write', 'admin'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    note = relationship("UserNote", foreign_keys=[note_id])
    shared_by_user = relationship("User", foreign_keys=[shared_by])
    shared_with_user = relationship("User", foreign_keys=[shared_with])

class NoteVersion(Base):
    __tablename__ = "note_versions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    version_number = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    note = relationship("UserNote", foreign_keys=[note_id])
    creator = relationship("User", foreign_keys=[created_by])

class NoteComment(Base):
    __tablename__ = "note_comments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    note = relationship("UserNote", foreign_keys=[note_id])
    user = relationship("User", foreign_keys=[user_id]) 