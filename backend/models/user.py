from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from core.database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.student)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations - Utiliser des chaînes pour éviter les imports circulaires
    advanced_notes = relationship("AdvancedNote", back_populates="author", lazy="dynamic")
    forum_threads = relationship("ForumThread", back_populates="author", lazy="dynamic")
    forum_replies = relationship("ForumReply", back_populates="author", lazy="dynamic")
    calendar_events = relationship("CalendarEvent", back_populates="user", lazy="dynamic")
    study_time_stats = relationship("StudyTimeStats", back_populates="user", lazy="dynamic") 
    
    # Relations pour l'évaluation adaptative
    # test_assignments = relationship("TestAssignment", back_populates="student")
    # test_attempts = relationship("TestAttempt", back_populates="student")
    # competency_analyses = relationship("CompetencyAnalysis", back_populates="student")
    
    # Relations pour l'analytics (commentées temporairement)
    # learning_analytics = relationship("LearningAnalytics", back_populates="student")
    # predictions = relationship("StudentPrediction", back_populates="student")
    # learning_patterns = relationship("LearningPattern", back_populates="student")
    # blockage_detections = relationship("BlockageDetection", back_populates="student")
    
    # Relations pour la collecte de données (commentées temporairement)
    # data_collections = relationship("DataCollection", back_populates="student")
    # pattern_analyses = relationship("AILearningPatternAnalysis", back_populates="student")
    
    # Relations pour les tableaux de bord (commentées temporairement)
    # teacher_dashboards = relationship("TeacherDashboard", foreign_keys="TeacherDashboard.teacher_id")
    # parent_dashboards = relationship("ParentDashboard", foreign_keys="ParentDashboard.parent_id")
    # student_dashboards = relationship("ParentDashboard", foreign_keys="ParentDashboard.student_id")
    
    # Relations pour la remédiation
    remediation_results = relationship("RemediationResult", back_populates="student", lazy="dynamic")
    remediation_badges = relationship("RemediationBadge", back_populates="student", lazy="dynamic")
    remediation_progress = relationship("RemediationProgress", back_populates="student", lazy="dynamic") 