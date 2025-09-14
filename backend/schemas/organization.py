from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =====================================================
# SCHÉMAS POUR LES DEVOIRS
# =====================================================

class HomeworkBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    class_id: Optional[int] = None
    assigned_to: Optional[int] = None
    due_date: datetime
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    estimated_time: Optional[int] = None  # minutes

class HomeworkCreate(HomeworkBase):
    pass

class HomeworkUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    class_id: Optional[int] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed|overdue)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    estimated_time: Optional[int] = None
    actual_time: Optional[int] = None
    grade: Optional[float] = Field(None, ge=0, le=20)
    feedback: Optional[str] = None

class HomeworkResponse(HomeworkBase):
    id: int
    assigned_by: int
    status: str
    actual_time: Optional[int] = None
    grade: Optional[float] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES SESSIONS D'ÉTUDE
# =====================================================

class StudySessionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  # minutes
    goals: Optional[List[str]] = None
    notes: Optional[str] = None

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    goals: Optional[List[str]] = None
    status: Optional[str] = Field(None, pattern="^(planned|in_progress|completed|cancelled)$")
    notes: Optional[str] = None

class StudySessionResponse(StudySessionBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES RAPPELS
# =====================================================

class ReminderBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    reminder_time: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[Dict[str, Any]] = None

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    reminder_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ReminderResponse(ReminderBase):
    id: int
    user_id: int
    is_active: bool
    notification_sent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES OBJECTIFS D'APPRENTISSAGE
# =====================================================

class LearningGoalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    target_date: Optional[datetime] = None

class LearningGoalCreate(LearningGoalBase):
    pass

class LearningGoalUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = None
    target_date: Optional[datetime] = None
    progress: Optional[float] = Field(None, ge=0.0, le=1.0)
    status: Optional[str] = Field(None, pattern="^(active|completed|abandoned)$")

class LearningGoalResponse(LearningGoalBase):
    id: int
    user_id: int
    progress: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES STATISTIQUES
# =====================================================

class HomeworkStats(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int
    completion_rate: float

class StudySessionStats(BaseModel):
    total_sessions: int
    total_time_minutes: int
    average_productivity: float
    sessions_per_day: float

class OrganizationStats(BaseModel):
    homework: HomeworkStats
    study_sessions: StudySessionStats
    total_reminders: int
    active_goals: int
    completed_goals: int

# =====================================================
# SCHÉMAS POUR LES CALENDRIERS
# =====================================================

class CalendarEvent(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    event_type: str  # 'homework', 'study_session', 'reminder', 'goal'
    color: Optional[str] = None
    is_all_day: bool = False
    
    class Config:
        from_attributes = True

class CalendarView(BaseModel):
    events: List[CalendarEvent]
    date_range: Dict[str, datetime]
    total_events: int

# =====================================================
# SCHÉMAS POUR LES RAPPORTS
# =====================================================

class StudyReport(BaseModel):
    period: str  # 'week', 'month', 'semester'
    total_study_time: int  # minutes
    sessions_count: int
    subjects_covered: List[str]
    productivity_trend: List[Dict[str, Any]]
    goals_progress: List[Dict[str, Any]]
    recommendations: List[str]

class HomeworkReport(BaseModel):
    period: str
    total_assigned: int
    completed: int
    overdue: int
    average_grade: Optional[float]
    subjects_performance: List[Dict[str, Any]]
    completion_trend: List[Dict[str, Any]]

# =====================================================
# SCHÉMAS POUR LES NOTIFICATIONS
# =====================================================

class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str = Field(..., pattern="^(homework|reminder|goal|study)$")
    priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES PRÉFÉRENCES
# =====================================================

class OrganizationPreferences(BaseModel):
    default_study_duration: int = 45  # minutes
    break_duration: int = 15  # minutes
    study_reminders: bool = True
    homework_reminders: bool = True
    goal_reminders: bool = True
    notification_email: bool = True
    notification_push: bool = True
    theme: str = Field(default="default", pattern="^(default|dark|light|colorful)$")
    language: str = Field(default="fr", pattern="^(fr|en|ar)$")

class UserPreferencesUpdate(BaseModel):
    default_study_duration: Optional[int] = Field(None, ge=15, le=180)
    break_duration: Optional[int] = Field(None, ge=5, le=60)
    study_reminders: Optional[bool] = None
    homework_reminders: Optional[bool] = None
    goal_reminders: Optional[bool] = None
    notification_email: Optional[bool] = None
    notification_push: Optional[bool] = None
    theme: Optional[str] = Field(None, pattern="^(default|dark|light|colorful)$")
    language: Optional[str] = Field(None, pattern="^(fr|en|ar)$") 