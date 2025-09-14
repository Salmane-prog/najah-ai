from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.content import Content, LearningPathContent
from schemas.content import ContentRead, NoteRead, ContentProgress
from models.user import User
from models.learning_path import LearningPath
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/{content_id}", response_model=ContentRead)
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer un contenu pédagogique."""
    
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.is_active == True
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    return content

@router.get("/")
def list_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Lister tous les contenus pédagogiques."""
    try:
        contents = db.query(Content).filter(Content.is_active == True).all()
        
        result = []
        for content in contents:
            result.append({
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "content_type": content.content_type,
                "subject": content.subject,
                "level": content.level,
                "difficulty": content.difficulty,
                "estimated_time": content.estimated_time,
                "created_at": content.created_at.isoformat() if content.created_at else None
            })
        
        return result
        
    except Exception as e:
        print(f"Erreur dans list_contents: {str(e)}")
        return []

@router.post("/", response_model=ContentRead)
def create_content(
    content_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer un nouveau contenu pédagogique."""
    
    content = Content(
        title=content_data["title"],
        description=content_data["description"],
        content_type=content_data["content_type"],
        subject=content_data["subject"],
        level=content_data["level"],
        difficulty=content_data.get("difficulty", 1.0),
        estimated_time=content_data.get("estimated_time", 15),
        content_data=content_data.get("content_data", ""),
        file_url=content_data.get("file_url", ""),
        thumbnail_url=content_data.get("thumbnail_url", ""),
        tags=json.dumps(content_data.get("tags", [])),
        learning_objectives=json.dumps(content_data.get("learning_objectives", [])),
        prerequisites=json.dumps(content_data.get("prerequisites", [])),
        skills_targeted=json.dumps(content_data.get("skills_targeted", [])),
        created_by=current_user.id
    )
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    return content

@router.put("/{content_id}", response_model=ContentRead)
def update_content(
    content_id: int,
    content_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Mettre à jour un contenu pédagogique."""
    
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Vérifier que l'utilisateur est le créateur ou un admin
    if content.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    # Mettre à jour les champs
    for field, value in content_data.items():
        if hasattr(content, field):
            if field in ["tags", "learning_objectives", "prerequisites", "skills_targeted"]:
                setattr(content, field, json.dumps(value))
            else:
                setattr(content, field, value)
    
    # content.updated_at = datetime.utcnow()  # Commenté temporairement
    db.commit()
    db.refresh(content)
    
    return content

@router.delete("/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer un contenu pédagogique."""
    
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Vérifier que l'utilisateur est le créateur ou un admin
    if content.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    # Marquer comme inactif au lieu de supprimer
    content.is_active = False
    db.commit()
    
    return {"message": "Contenu supprimé avec succès"}

@router.get("/{content_id}/notes", response_model=List[NoteRead])
def get_content_notes(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les notes d'un utilisateur pour un contenu."""
    
    # Vérifier que le contenu existe
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Pour l'instant, retourner des notes factices
    # TODO: Implémenter le modèle Note
    notes = [
        {
            "id": 1,
            "content_id": content_id,
            "user_id": current_user.id,
            "text": "Note importante sur ce contenu",
            "timestamp": 120,
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    return notes

@router.post("/{content_id}/notes", response_model=NoteRead)
def add_content_note(
    content_id: int,
    note_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Ajouter une note à un contenu."""
    
    # Vérifier que le contenu existe
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Pour l'instant, retourner une note factice
    # TODO: Implémenter le modèle Note
    note = {
        "id": len(note_data) + 1,
        "content_id": content_id,
        "user_id": current_user.id,
        "text": note_data["text"],
        "timestamp": note_data.get("timestamp", 0),
        "created_at": datetime.utcnow().isoformat()
    }
    
    return note

@router.post("/{content_id}/progress")
def update_content_progress(
    content_id: int,
    progress_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour la progression d'un utilisateur sur un contenu."""
    
    # Vérifier que le contenu existe
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Pour l'instant, juste retourner un succès
    # TODO: Implémenter le modèle ContentProgress
    return {
        "message": "Progression mise à jour",
        "content_id": content_id,
        "user_id": current_user.id,
        "progress": progress_data["progress"]
    }

@router.get("/recommendations/{student_id}")
def get_content_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Obtenir des recommandations de contenu pour un étudiant."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Analyser les préférences de l'étudiant
    # Pour l'instant, retourner des recommandations basées sur le niveau
    recommended_contents = db.query(Content).filter(
        Content.is_active == True,
        Content.level == "intermediate"  # Niveau par défaut
    ).limit(5).all()
    
    return {
        "student_id": student_id,
        "recommendations": recommended_contents
    }

@router.get("/search/")
def search_contents(
    q: str,
    subject: str = None,
    level: str = None,
    content_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Rechercher des contenus pédagogiques."""
    
    query = db.query(Content).filter(Content.is_active == True)
    
    # Recherche textuelle
    if q:
        query = query.filter(
            Content.title.ilike(f"%{q}%") |
            Content.description.ilike(f"%{q}%") |
            Content.subject.ilike(f"%{q}%")
        )
    
    # Filtres
    if subject:
        query = query.filter(Content.subject == subject)
    if level:
        query = query.filter(Content.level == level)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    contents = query.order_by(Content.created_at.desc()).all()
    
    return {
        "query": q,
        "results": contents,
        "total": len(contents)
    } 