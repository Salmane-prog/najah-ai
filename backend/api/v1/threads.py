from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.thread import Thread
from schemas.thread import ThreadCreate, ThreadRead
from typing import List
from api.v1.users import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ThreadRead, status_code=201)
def create_thread(thread: ThreadCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_thread = Thread(**thread.dict())
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread

@router.get("/", response_model=List[ThreadRead])
def list_threads(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Thread).order_by(Thread.created_at.desc()).all()

@router.get("/{thread_id}", response_model=ThreadRead)
def get_thread(thread_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread non trouvé")
    return thread

@router.get("/user/{user_id}", response_model=List[ThreadRead])
def list_threads_by_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Thread).filter(Thread.created_by == user_id).order_by(Thread.created_at.desc()).all()

@router.delete("/{thread_id}", status_code=204)
def delete_thread(thread_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread non trouvé")
    db.delete(thread)
    db.commit()
    return 