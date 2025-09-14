from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    content = relationship("Content", foreign_keys=[content_id])

class Collection(Base):
    __tablename__ = "collections"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    cover_image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    items = relationship("CollectionItem", back_populates="collection")

class CollectionItem(Base):
    __tablename__ = "collection_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    collection = relationship("Collection", back_populates="items")
    content = relationship("Content", foreign_keys=[content_id])

class ContentHistory(Base):
    __tablename__ = "content_history"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())
    time_spent = Column(Integer)  # seconds
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    rating = Column(Integer)  # 1-5
    review = Column(Text)
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    content = relationship("Content", foreign_keys=[content_id])

class ContentRecommendation(Base):
    __tablename__ = "content_recommendations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    score = Column(Float, nullable=False)  # 0.0 to 1.0
    reason = Column(String(255))
    algorithm = Column(String(50))  # 'collaborative', 'content_based', 'hybrid'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    content = relationship("Content", foreign_keys=[content_id])

class Playlist(Base):
    __tablename__ = "playlists"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    items = relationship("PlaylistItem", back_populates="playlist")

class PlaylistItem(Base):
    __tablename__ = "playlist_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    position = Column(Integer, nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    playlist = relationship("Playlist", back_populates="items")
    content = relationship("Content", foreign_keys=[content_id]) 