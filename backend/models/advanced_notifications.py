from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    title_template = Column(String(255), nullable=False)
    message_template = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # 'email', 'sms', 'push', 'in_app'
    category = Column(String(50), nullable=False)  # 'academic', 'administrative', 'reminder', 'alert'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdvancedNotification(Base):
    __tablename__ = "advanced_notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("notification_templates.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # 'email', 'sms', 'push', 'in_app'
    category = Column(String(50), nullable=False)
    priority = Column(String(20), default="normal")  # 'low', 'normal', 'high', 'urgent'
    data = Column(JSON)  # Données supplémentaires (liens, actions, etc.)
    scheduled_at = Column(DateTime)  # Pour les notifications programmées
    sent_at = Column(DateTime)
    read_at = Column(DateTime)
    status = Column(String(20), default="pending")  # 'pending', 'sent', 'delivered', 'failed'
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User")
    template = relationship("NotificationTemplate")

class EmailNotification(Base):
    __tablename__ = "email_notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("advanced_notifications.id"), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    html_content = Column(Text)
    text_content = Column(Text)
    attachments = Column(JSON)  # Liste des pièces jointes
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    status = Column(String(20), default="pending")  # 'pending', 'sent', 'delivered', 'bounced', 'failed'
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    notification = relationship("AdvancedNotification")

class SMSNotification(Base):
    __tablename__ = "sms_notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("advanced_notifications.id"), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    status = Column(String(20), default="pending")  # 'pending', 'sent', 'delivered', 'failed'
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    notification = relationship("AdvancedNotification")

class PushNotification(Base):
    __tablename__ = "push_notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("advanced_notifications.id"), nullable=False)
    device_token = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    data = Column(JSON)  # Données supplémentaires
    badge_count = Column(Integer, default=0)
    sound = Column(String(100))
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    status = Column(String(20), default="pending")  # 'pending', 'sent', 'delivered', 'failed'
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    notification = relationship("AdvancedNotification")

class NotificationSchedule(Base):
    __tablename__ = "notification_schedules"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    template_id = Column(Integer, ForeignKey("notification_templates.id"), nullable=False)
    target_users = Column(JSON)  # Critères de sélection des utilisateurs
    schedule_type = Column(String(50), nullable=False)  # 'one_time', 'recurring', 'event_based'
    schedule_data = Column(JSON)  # Configuration de la planification
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    template = relationship("NotificationTemplate")
    creator = relationship("User")

class CalendarIntegration(Base):
    __tablename__ = "calendar_integrations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # 'google', 'outlook', 'ical', 'apple'
    calendar_id = Column(String(255), nullable=False)
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    sync_enabled = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    sync_frequency = Column(String(20), default="daily")  # 'hourly', 'daily', 'weekly'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    user = relationship("User")

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=False)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    frequency = Column(String(20), default="immediate")  # 'immediate', 'daily', 'weekly', 'never'
    quiet_hours_start = Column(String(5))  # Format HH:MM
    quiet_hours_end = Column(String(5))  # Format HH:MM
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    user = relationship("User") 