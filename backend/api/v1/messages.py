from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.messages import Message
from models.thread import Thread
from schemas.message import MessageCreate, MessageRead
from typing import List
from api.v1.users import get_current_user
from api.v1.notifications_ws import send_notification

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MessageRead, status_code=201)
async def create_message(message: MessageCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    # Notifier l’auteur du thread (si différent de l’auteur du message)
    thread = db.query(Thread).filter(Thread.id == db_message.thread_id).first()
    if thread and thread.created_by != db_message.user_id:
        await send_notification(thread.created_by, f"Nouveau message dans votre thread : {thread.title}")
    return db_message

@router.get("/", response_model=List[MessageRead])
def list_messages(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Message).order_by(Message.created_at.asc()).all()

@router.get("/thread/{thread_id}", response_model=List[MessageRead])
def list_messages_by_thread(thread_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Message).filter(Message.thread_id == thread_id).order_by(Message.created_at.asc()).all()

@router.get("/user/{user_id}", response_model=List[MessageRead])
def list_messages_by_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    import inspect
    frame = inspect.currentframe()
    try:
        request = None
        for f in inspect.stack():
            if 'request' in f.frame.f_locals:
                request = f.frame.f_locals['request']
                break
        if request:
            print(f"[DEBUG] Authorization header: {request.headers.get('authorization')}")
    except Exception as e:
        print(f"[DEBUG] Impossible d'afficher le header Authorization: {e}")
    print(f"[API] /messages/user/{user_id} - Token user: {current_user.id if current_user else 'None'}")
    return db.query(Message).filter(Message.user_id == user_id).order_by(Message.created_at.asc()).all()

@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    db.delete(message)
    db.commit()
    return 