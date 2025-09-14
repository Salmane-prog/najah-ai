from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User, UserRole
from models.messages import Message
from models.thread import Thread
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/conversations")
def get_teacher_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer toutes les conversations du professeur avec ses élèves."""
    try:
        # Récupérer les classes du professeur
        from models.class_group import ClassGroup, ClassStudent
        
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        if not teacher_classes:
            return {"conversations": []}
        
        class_ids = [c.id for c in teacher_classes]
        
        # Récupérer tous les élèves des classes du professeur
        students = db.query(User).join(ClassStudent).filter(
            ClassStudent.class_id.in_(class_ids),
            User.role == UserRole.student
        ).all()
        
        if not students:
            return {"conversations": []}
        
        # Récupérer les conversations existantes
        conversations = []
        for student in students:
            try:
                # Vérifier s'il y a des messages avec cet élève
                thread = db.query(Thread).filter(
                    Thread.created_by == current_user.id,
                    Thread.title.like(f"%{student.username}%")
                ).first()
                
                if thread:
                    # Récupérer le dernier message
                    last_message = db.query(Message).filter(
                        Message.thread_id == thread.id
                    ).order_by(Message.created_at.desc()).first()
                    
                    # Compter les messages non lus (envoyés par l'élève)
                    unread_count = db.query(Message).filter(
                        Message.thread_id == thread.id,
                        Message.user_id == student.id,
                        Message.is_read == False
                    ).count()
                    
                    # Déterminer le nom à afficher
                    display_name = "Élève sans nom"
                    if student.first_name and student.last_name:
                        display_name = f"{student.first_name} {student.last_name}"
                    elif student.username:
                        display_name = student.username
                    elif student.email:
                        email_name = student.email.split('@')[0]
                        display_name = email_name.replace('.', ' ').title()
                    
                    conversations.append({
                        "thread_id": thread.id,
                        "student": {
                            "id": student.id,
                            "name": display_name,
                            "email": student.email
                        },
                        "last_message": {
                            "content": last_message.content if last_message else "",
                            "timestamp": last_message.created_at.isoformat() if last_message else None,
                            "user_id": last_message.user_id if last_message else None
                        },
                        "unread_count": unread_count
                    })
                else:
                    # Pas de thread existant, l'élève apparaîtra dans la liste mais sans conversation
                    # Déterminer le nom à afficher
                    display_name = "Élève sans nom"
                    if student.first_name and student.last_name:
                        display_name = f"{student.first_name} {student.last_name}"
                    elif student.username:
                        display_name = student.username
                    elif student.email:
                        email_name = student.email.split('@')[0]
                        display_name = email_name.replace('.', ' ').title()
                    
                    conversations.append({
                        "thread_id": None,
                        "student": {
                            "id": student.id,
                            "name": display_name,
                            "email": student.email
                        },
                        "last_message": None,
                        "unread_count": 0
                    })
            except Exception as e:
                print(f"Erreur lors du traitement de l'élève {student.id}: {str(e)}")
                # Continuer avec l'élève suivant
                continue
        
        return {"conversations": conversations}
        
    except Exception as e:
        print(f"Erreur dans get_teacher_conversations: {str(e)}")
        # Retourner une liste vide en cas d'erreur
        return {"conversations": []}

@router.get("/conversation/{student_id}")
def get_conversation_with_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer la conversation avec un élève spécifique."""
    try:
        # Vérifier que l'élève existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Élève non trouvé")
        
        # Vérifier que le professeur a accès à cet élève
        from models.class_group import ClassGroup, ClassStudent
        
        teacher_has_access = db.query(ClassStudent).join(ClassGroup).filter(
            ClassStudent.student_id == student_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not teacher_has_access:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cet élève")
        
        # Trouver ou créer un thread pour cette conversation
        thread = db.query(Thread).filter(
            Thread.created_by == current_user.id,
            Thread.title.like(f"%{student.username}%")
        ).first()
        
        if not thread:
            # Créer un nouveau thread
            thread = Thread(
                title=f"Conversation avec {student.username}",
                created_by=current_user.id,
                type="teacher_student"
            )
            db.add(thread)
            db.commit()
            db.refresh(thread)
        
        # Marquer les messages comme lus (envoyés par l'élève)
        db.query(Message).filter(
            Message.thread_id == thread.id,
            Message.user_id == student_id,
            Message.is_read == False
        ).update({"is_read": True})
        db.commit()
        
        # Récupérer tous les messages du thread
        messages = db.query(Message).filter(
            Message.thread_id == thread.id
        ).order_by(Message.created_at.asc()).all()
        
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "id": msg.id,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat(),
                "user_id": msg.user_id,
                "is_teacher": msg.user_id == current_user.id,
                "sender_name": current_user.username if msg.user_id == current_user.id else student.username
            })
        
        return {
            "thread_id": thread.id,
            "student": {
                "id": student.id,
                "name": student.username or f"Élève {student.id}",
                "email": student.email
            },
            "messages": formatted_messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la conversation: {str(e)}")

@router.post("/conversation/{student_id}/send")
def send_message_to_student(
    student_id: int,
    message_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Envoyer un message à un élève."""
    try:
        content = message_data.get("content")
        if not content:
            raise HTTPException(status_code=400, detail="Le contenu du message est requis")
        
        # Vérifier que l'élève existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Élève non trouvé")
        
        # Vérifier que le professeur a accès à cet élève
        from models.class_group import ClassGroup, ClassStudent
        
        teacher_has_access = db.query(ClassStudent).join(ClassGroup).filter(
            ClassStudent.student_id == student_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not teacher_has_access:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cet élève")
        
        # Trouver ou créer un thread
        thread = db.query(Thread).filter(
            Thread.created_by == current_user.id,
            Thread.title.like(f"%{student.username}%")
        ).first()
        
        if not thread:
            # Créer un nouveau thread pour cette conversation
            thread = Thread(
                title=f"Conversation avec {student.username}",
                created_by=current_user.id,
                type="teacher_student"
            )
            db.add(thread)
            db.commit()
            db.refresh(thread)
            print(f"Nouveau thread créé: {thread.id} pour {student.username}")
        
        # Créer le message
        new_message = Message(
            content=content,
            user_id=current_user.id,
            thread_id=thread.id,
            is_read=False
        )
        
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        # Créer une notification pour l'étudiant
        try:
            from models.notification import Notification
            import json
            
            # Déterminer le nom du professeur pour la notification
            teacher_name = "Professeur"
            if current_user.first_name and current_user.last_name:
                teacher_name = f"{current_user.first_name} {current_user.last_name}"
            elif current_user.username:
                teacher_name = current_user.username
            elif current_user.email:
                email_name = current_user.email.split('@')[0]
                teacher_name = email_name.replace('.', ' ').title()
            
            notification = Notification(
                user_id=student_id,
                title="Nouveau message",
                message=f"Nouveau message de {teacher_name}",
                type="message",
                data=json.dumps({
                    "sender_id": current_user.id,
                    "sender_name": teacher_name,
                    "message_preview": content[:50] + "..." if len(content) > 50 else content,
                    "thread_id": thread.id
                }),
                is_read=False,
                created_at=datetime.utcnow()
            )
            
            db.add(notification)
            db.commit()
            print(f"✅ Notification créée pour l'étudiant {student_id}")
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

@router.get("/conversation/{student_id}/messages")
def get_conversation_messages(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer tous les messages d'une conversation avec un étudiant."""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer le thread de conversation
        thread = db.query(Thread).filter(
            Thread.created_by == current_user.id,
            Thread.title.like(f"%{student.username}%")
        ).first()
        
        if not thread:
            return {"messages": []}
        
        # Récupérer tous les messages du thread
        messages = db.query(Message).filter(
            Message.thread_id == thread.id
        ).order_by(Message.created_at.asc()).all()
        
        # Formater les messages
        formatted_messages = []
        for message in messages:
            sender = db.query(User).filter(User.id == message.user_id).first()
            formatted_messages.append({
                "id": message.id,
                "content": message.content,
                "timestamp": message.created_at.isoformat(),
                "user_id": message.user_id,
                "is_teacher": message.user_id == current_user.id,
                "sender_name": sender.username if sender else "Unknown"
            })
        
        return {"messages": formatted_messages}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des messages: {str(e)}")

@router.post("/conversation/{thread_id}/mark-read")
def mark_messages_as_read(
    thread_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Marquer tous les messages d'un thread comme lus."""
    try:
        # Vérifier que le thread appartient au professeur
        thread = db.query(Thread).filter(
            Thread.id == thread_id,
            Thread.created_by == current_user.id
        ).first()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread non trouvé")
        
        # Marquer tous les messages comme lus
        db.query(Message).filter(
            Message.thread_id == thread_id,
            Message.user_id != current_user.id  # Seulement les messages des autres
        ).update({"is_read": True})
        
        db.commit()
        
        return {"message": "Messages marqués comme lus"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du marquage des messages: {str(e)}")

# WebSocket pour les messages temps réel
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Traiter les messages reçus
            message_data = json.loads(data)
            # Logique de traitement des messages temps réel
    except WebSocketDisconnect:
        manager.disconnect(user_id) 