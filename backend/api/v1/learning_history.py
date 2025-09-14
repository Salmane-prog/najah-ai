from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.learning_history import LearningHistory
from schemas.learning_history import LearningHistoryCreate, LearningHistoryRead
from typing import List, Optional
from api.v1.users import get_current_user
from api.v1.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LearningHistoryRead, status_code=201)
def create_learning_history(entry: LearningHistoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # TODO: Affiner la sécurité (seul l’élève ou le système peut créer pour lui-même)
    if current_user.role not in ("student", "admin", "teacher", "parent"):
        raise HTTPException(status_code=403, detail="Accès interdit")
    if current_user.role == "student" and current_user.id != entry.student_id:
        raise HTTPException(status_code=403, detail="Un élève ne peut créer que pour lui-même")
    db_entry = LearningHistory(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=List[LearningHistoryRead])
def list_learning_history(student_id: Optional[int] = None, path_id: Optional[int] = None, content_id: Optional[int] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    print(f"[API] /learning_history/ - student_id: {student_id}, Token user: {current_user.id if current_user else 'None'}")
    print(f"[DEBUG] Endpoint learning_history appelé avec student_id={student_id}")
    # TODO: Affiner la sécurité (parents, enseignants, admin, élève concerné)
    query = db.query(LearningHistory)
    if student_id:
        query = query.filter(LearningHistory.student_id == student_id)
    if path_id:
        query = query.filter(LearningHistory.path_id == path_id)
    if content_id:
        query = query.filter(LearningHistory.content_id == content_id)
    results = query.order_by(LearningHistory.timestamp.desc()).all()
    print(f"[DEBUG] Nombre de résultats trouvés: {len(results)}")
    # Retourner une liste vide si aucun résultat trouvé (au lieu d'erreur 404)
    return results

@router.get("/{history_id}", response_model=LearningHistoryRead)
def get_learning_history(history_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(LearningHistory).filter(LearningHistory.id == history_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    # TODO: Affiner la sécurité (parents, enseignants, admin, élève concerné)
    return entry 