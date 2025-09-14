#!/usr/bin/env python3
"""
Endpoints pour la messagerie côté étudiant
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import json

from core.database import get_db
from models.user import User, UserRole
from models.thread import Thread
from models.messages import Message
from models.notification import Notification
from api.v1.auth import require_role

router = APIRouter()

@router.get("/conversations")
def get_student_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les conversations d'un étudiant avec les professeurs."""
    try:
        # Trouver tous les threads où l'étudiant est impliqué
        threads = db.query(Thread).filter(
            Thread.title.like(f"%{current_user.username}%")
        ).all()
        
        conversations = []
        for thread in threads:
            # Trouver le dernier message
            last_message = db.query(Message).filter(
                Message.thread_id == thread.id
            ).order_by(Message.created_at.desc()).first()
            
            # Compter les messages non lus
            unread_count = db.query(Message).filter(
                Message.thread_id == thread.id,
                Message.user_id != current_user.id,
                Message.is_read == False
            ).count()
            
            # Déterminer le nom du professeur (créateur du thread)
            teacher = db.query(User).filter(User.id == thread.created_by).first()
            teacher_name = "Professeur"
            if teacher:
                if teacher.first_name and teacher.last_name:
                    teacher_name = f"{teacher.first_name} {teacher.last_name}"
                elif teacher.username:
                    teacher_name = teacher.username
                elif teacher.email:
                    email_name = teacher.email.split('@')[0]
                    teacher_name = email_name.replace('.', ' ').title()
            
            conversations.append({
                "id": thread.id,
                "teacher_id": thread.created_by,
                "teacher_name": teacher_name,
                "teacher_email": teacher.email if teacher else "",
                "last_message": {
                    "content": last_message.content if last_message else "",
                    "timestamp": last_message.created_at.isoformat() if last_message else None,
                    "user_id": last_message.user_id if last_message else None
                },
                "unread_count": unread_count
            })
        
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des conversations: {str(e)}")

@router.get("/conversation/{thread_id}/messages")
def get_conversation_messages(
    thread_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer tous les messages d'une conversation."""
    try:
        # Vérifier que l'étudiant a accès à ce thread
        thread = db.query(Thread).filter(
            Thread.id == thread_id,
            Thread.title.like(f"%{current_user.username}%")
        ).first()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        messages = db.query(Message).filter(
            Message.thread_id == thread_id
        ).order_by(Message.created_at.asc()).all()
        
        formatted_messages = []
        for message in messages:
            sender = db.query(User).filter(User.id == message.user_id).first()
            formatted_messages.append({
                "id": message.id,
                "content": message.content,
                "timestamp": message.created_at.isoformat(),
                "user_id": message.user_id,
                "is_teacher": message.user_id != current_user.id,
                "sender_name": sender.username if sender else "Unknown"
            })
        
        return {"messages": formatted_messages}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des messages: {str(e)}")

@router.post("/conversation/{thread_id}/send")
def send_message_to_teacher(
    thread_id: int,
    message_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Envoyer un message à un professeur."""
    try:
        # Vérifier que l'étudiant a accès à ce thread
        thread = db.query(Thread).filter(
            Thread.id == thread_id,
            Thread.title.like(f"%{current_user.username}%")
        ).first()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        content = message_data.get("content", "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Le contenu du message ne peut pas être vide")
        
        # Créer le nouveau message
        new_message = Message(
            thread_id=thread_id,
            user_id=current_user.id,
            content=content,
            created_at=datetime.utcnow(),
            is_read=False
        )
        
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        # Créer une notification pour le professeur
        try:
            notification = Notification(
                user_id=thread.created_by,
                title="Nouveau message",
                message=f"Nouveau message de {current_user.username}",
                type="message",
                data=json.dumps({
                    "sender_id": current_user.id,
                    "sender_name": current_user.username,
                    "message_preview": content[:50] + "..." if len(content) > 50 else content,
                    "thread_id": thread.id
                }),
                is_read=False,
                created_at=datetime.utcnow()
            )
            
            db.add(notification)
            db.commit()
        except Exception as e:
            print(f"Erreur lors de la création de la notification: {str(e)}")
            # Ne pas faire échouer l'envoi du message si la notification échoue
        
        return {
            "message": "Message envoyé avec succès",
            "message_id": new_message.id,
            "timestamp": new_message.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'envoi du message: {str(e)}")

@router.post("/conversation/{thread_id}/mark-read")
def mark_messages_as_read(
    thread_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Marquer tous les messages d'une conversation comme lus."""
    try:
        # Vérifier que l'étudiant a accès à ce thread
        thread = db.query(Thread).filter(
            Thread.id == thread_id,
            Thread.title.like(f"%{current_user.username}%")
        ).first()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        # Marquer tous les messages non lus comme lus
        db.query(Message).filter(
            Message.thread_id == thread_id,
            Message.user_id != current_user.id,
            Message.is_read == False
        ).update({"is_read": True})
        
        db.commit()
        
        return {"message": "Messages marqués comme lus"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du marquage des messages: {str(e)}")

@router.get("/notifications")
def get_student_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les notifications d'un étudiant."""
    try:
        notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id
        ).order_by(Notification.created_at.desc()).all()
        
        formatted_notifications = []
        for notif in notifications:
            formatted_notifications.append({
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "type": notif.type,
                "data": json.loads(notif.data) if notif.data else {},
                "is_read": notif.is_read,
                "created_at": notif.created_at.isoformat()
            })
        
        return {"notifications": formatted_notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des notifications: {str(e)}")

@router.get("/notifications/unread-count")
def get_unread_notifications_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer le nombre de notifications non lues d'un étudiant."""
    try:
        unread_count = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ).count()
        
        return {"unread_count": unread_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du nombre de notifications: {str(e)}")

@router.post("/notifications/{notification_id}/mark-read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Marquer une notification comme lue."""
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification non trouvée")
        
        notification.is_read = True
        db.commit()
        
        return {"message": "Notification marquée comme lue"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du marquage de la notification: {str(e)}") 