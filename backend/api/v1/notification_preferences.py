from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.notification_preference import NotificationPreference
from schemas.notification_preference import NotificationPreferenceCreate, NotificationPreferenceRead
from typing import List
from api.v1.users import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/user/{user_id}", response_model=List[NotificationPreferenceRead])
def get_user_notification_preferences(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(NotificationPreference).filter(NotificationPreference.user_id == user_id).all()

@router.post("/", response_model=NotificationPreferenceRead, status_code=201)
def create_notification_preference(pref: NotificationPreferenceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_pref = NotificationPreference(**pref.dict())
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref

@router.put("/{pref_id}", response_model=NotificationPreferenceRead)
def update_notification_preference(pref_id: int, pref: NotificationPreferenceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_pref = db.query(NotificationPreference).filter(NotificationPreference.id == pref_id).first()
    if not db_pref:
        raise HTTPException(status_code=404, detail="Préférence non trouvée")
    for key, value in pref.dict().items():
        setattr(db_pref, key, value)
    db.commit()
    db.refresh(db_pref)
    return db_pref 