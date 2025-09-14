from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.badge import Badge, UserBadge
from models.user import User
from schemas.badge import BadgeCreate, BadgeRead, UserBadgeRead
from typing import List, Optional
from api.v1.users import get_current_user
from api.v1.auth import require_role
from datetime import datetime
from services.notification import notify_users

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Badges
@router.post("/", response_model=BadgeRead, status_code=201)
def create_badge(badge: BadgeCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['admin', 'teacher']))):
    db_badge = Badge(**badge.dict())
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    return db_badge

@router.get("/", response_model=List[BadgeRead])
def list_badges(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Liste tous les badges disponibles."""
    try:
        badges = db.query(Badge).all()
        # Masquer les badges secrets pour les non-admins
        if current_user.role not in ["admin", "teacher"]:
            for badge in badges:
                if badge.secret:
                    badge.name = "Badge secret"
                    badge.description = "Ce badge est secret."
        return badges
    except Exception as e:
        print(f"[ERROR] Erreur dans list_badges: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@router.get("/{badge_id}", response_model=BadgeRead)
def get_badge(badge_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(status_code=404, detail="Badge non trouvé")
    return badge

@router.delete("/{badge_id}", status_code=204)
def delete_badge(badge_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['admin']))):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(status_code=404, detail="Badge non trouvé")
    db.delete(badge)
    db.commit()
    return

# Attribution d’un badge à un utilisateur
@router.post("/award/{user_id}/{badge_id}", response_model=UserBadgeRead, status_code=201)
async def award_badge(user_id: int, badge_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['admin', 'teacher']))):
    user = db.query(User).filter(User.id == user_id).first()
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not user or not badge:
        raise HTTPException(status_code=404, detail="Utilisateur ou badge non trouvé")
    user_badge = UserBadge(user_id=user_id, badge_id=badge_id, awarded_at=datetime.utcnow())
    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)
    # Notifier l’utilisateur (WebSocket/email selon préférences)
    await notify_users(db, [user_id], subject="Nouveau badge !", message=f"Vous avez reçu le badge : {badge.name}", notif_type="badge")
    return user_badge

# Liste des badges d’un utilisateur
@router.get("/user/{user_id}", response_model=List[UserBadgeRead])
def list_user_badges(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
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
    print(f"[API] /badges/user/{user_id} - Token user: {current_user.id if current_user else 'None'}")
    user_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    # Masquer les badges secrets non obtenus
    for ub in user_badges:
        if ub.badge and ub.badge.secret and ub.user_id != current_user.id:
            ub.badge.name = "Badge secret"
            ub.badge.description = "Ce badge est secret."
            ub.badge.image_url = None
    return user_badges

# Nombre de badges par utilisateur
@router.get("/user/{user_id}/count", response_model=int)
def count_user_badges(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(UserBadge).filter(UserBadge.user_id == user_id).count()

# Classement des utilisateurs par nombre de badges
@router.get("/leaderboard", response_model=List[dict])
def badges_leaderboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    type_badge: Optional[str] = Query(None),
    min_progression: float = Query(1.0),
    limit: int = Query(10)
):
    from sqlalchemy import func
    query = db.query(UserBadge.user_id, func.count(UserBadge.id).label("badge_count"), func.avg(UserBadge.progression).label("avg_progression"))
    if type_badge:
        query = query.join(Badge).filter(Badge.criteria == type_badge)
    if min_progression < 1.0:
        query = query.filter(UserBadge.progression >= min_progression)
    results = (
        query.group_by(UserBadge.user_id)
        .order_by(func.count(UserBadge.id).desc(), func.avg(UserBadge.progression).desc())
        .limit(limit)
        .all()
    )
    leaderboard = [
        {"user_id": user_id, "badge_count": badge_count, "avg_progression": avg_progression}
        for user_id, badge_count, avg_progression in results
    ]
    return leaderboard

# Liste des utilisateurs ayant un badge donné
@router.get("/{badge_id}/users", response_model=List[int])
def users_with_badge(badge_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_ids = db.query(UserBadge.user_id).filter(UserBadge.badge_id == badge_id).all()
    return [uid for (uid,) in user_ids] 