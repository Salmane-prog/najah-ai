from typing import List, Literal
from services.email import send_email
from api.v1.notifications_ws import send_notification as send_ws_notification
from models.user import User
from models.notification import Notification
from models.notification_preference import NotificationPreference
from sqlalchemy.orm import Session

NotificationChannel = Literal["websocket", "email"]

# Fonction centrale d’envoi de notification
async def notify_users(
    db: Session,
    user_ids: List[int],
    subject: str,
    message: str,
    notif_type: str = "info",
    channels: List[NotificationChannel] = ["websocket", "email"],
    extra: dict = None
):
    for user_id in user_ids:
        # Préférences utilisateur
        prefs = db.query(NotificationPreference).filter_by(user_id=user_id, notif_type=notif_type).all()
        enabled_channels = set(channels)
        for pref in prefs:
            if not pref.enabled and pref.channel in enabled_channels:
                enabled_channels.remove(pref.channel)
        # WebSocket
        if "websocket" in enabled_channels:
            await send_ws_notification(user_id, message)
        # Email
        if "email" in enabled_channels:
            user = db.query(User).filter(User.id == user_id).first()
            if user and user.email:
                send_email(user.email, subject, message)
        # Historique notification (optionnel)
        notif = Notification(user_id=user_id, title=notif_type, message=message)
        db.add(notif)
    db.commit() 