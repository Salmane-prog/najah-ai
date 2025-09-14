from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class UserLevel(Base):
    __tablename__ = "user_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    level = Column(Integer, default=1)
    current_xp = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    xp_to_next_level = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    challenge_type = Column(String(50), nullable=False)  # 'daily', 'weekly', 'achievement'
    xp_reward = Column(Integer, default=0)
    badge_reward_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    requirements = Column(Text, nullable=True)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserChallenge(Base):
    __tablename__ = "user_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Leaderboard(Base):
    __tablename__ = "leaderboards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    leaderboard_type = Column(String(50), nullable=False)  # 'global', 'class', 'subject'
    subject = Column(String(100), nullable=True)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    leaderboard_id = Column(Integer, ForeignKey("leaderboards.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    achievement_type = Column(String(50), nullable=False)  # 'quiz', 'streak', 'level', 'custom'
    requirements = Column(Text, nullable=True)  # JSON string
    xp_reward = Column(Integer, default=0)
    badge_reward_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    is_hidden = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now()) 