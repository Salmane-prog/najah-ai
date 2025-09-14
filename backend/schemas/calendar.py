#!/usr/bin/env python3
"""
Schémas Pydantic pour le calendrier et les statistiques
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# =====================================================
# SCHÉMAS POUR LES ÉVÉNEMENTS DU CALENDRIER
# =====================================================

class CalendarEventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: str = Field(..., pattern="^(homework|study_session|reminder|goal|exam|meeting)$")
    start_date: datetime
    end_date: Optional[datetime] = None
    all_day: bool = False
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    location: Optional[str] = None
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    recurrence: str = Field(default="none", pattern="^(none|daily|weekly|monthly|yearly)$")
    recurrence_end: Optional[datetime] = None

class CalendarEventCreate(CalendarEventBase):
    pass

class CalendarEventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: Optional[str] = Field(None, pattern="^(homework|study_session|reminder|goal|exam|meeting)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    all_day: Optional[bool] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    location: Optional[str] = None
    recurrence: Optional[str] = Field(None, pattern="^(none|daily|weekly|monthly|yearly)$")
    recurrence_end: Optional[datetime] = None

class CalendarEventResponse(CalendarEventBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES STATISTIQUES DE TEMPS D'ÉTUDE
# =====================================================

class StudyTimeStatsBase(BaseModel):
    date: datetime
    subject: str = Field(..., min_length=1, max_length=100)
    duration_minutes: int = Field(..., ge=1)
    session_count: int = Field(default=1, ge=1)

class StudyTimeStatsCreate(StudyTimeStatsBase):
    pass

class StudyTimeStatsUpdate(BaseModel):
    date: Optional[datetime] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    duration_minutes: Optional[int] = Field(None, ge=1)
    session_count: Optional[int] = Field(None, ge=1)

class StudyTimeStatsResponse(StudyTimeStatsBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES STATISTIQUES D'ORGANISATION
# =====================================================

class OrganizationStatsResponse(BaseModel):
    total_homeworks: int
    total_study_sessions: int
    completed_sessions: int
    total_goals: int
    completed_goals: int
    active_reminders: int
    total_calendar_events: int
    upcoming_events: int

class StudyTimeStatsSummaryResponse(BaseModel):
    total_time: int  # en minutes
    average_per_session: float
    sessions_count: int
    subject_breakdown: List[dict]  # [{"subject": "Math", "time": 120}, ...]
