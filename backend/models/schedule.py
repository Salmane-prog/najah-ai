from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class ScheduleEvent(Base):
    __tablename__ = "schedule_events"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)  # 'course', 'exam', 'meeting', 'reminder'
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255))
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"))
    subject = Column(String(100))
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(JSON)  # {'type': 'weekly', 'days': ['monday', 'wednesday']}
    color = Column(String(7), default="#3B82F6")  # Hex color
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    teacher = relationship("User", foreign_keys=[teacher_id])
    class_group = relationship("ClassGroup")
    attendees = relationship("ScheduleAttendee", back_populates="event")

class ScheduleAttendee(Base):
    __tablename__ = "schedule_attendees"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("schedule_events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="attendee")  # 'attendee', 'presenter', 'organizer'
    status = Column(String(50), default="pending")  # 'pending', 'accepted', 'declined', 'tentative'
    notification_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    event = relationship("ScheduleEvent", back_populates="attendees")
    user = relationship("User", foreign_keys=[user_id])

class ScheduleCalendarIntegration(Base):
    __tablename__ = "schedule_calendar_integrations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # 'google', 'outlook', 'ical'
    calendar_id = Column(String(255), nullable=False)
    access_token = Column(Text)
    refresh_token = Column(Text)
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User", foreign_keys=[user_id]) 