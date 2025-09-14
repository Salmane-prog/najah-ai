#!/usr/bin/env python3
"""
API pour les notes avancées
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.notes import AdvancedNote, AdvancedSubject, AdvancedChapter

router = APIRouter(tags=["notes"])

# ===== MATIÈRES =====
@router.get("/notes-advanced/subjects")
def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer toutes les matières disponibles"""
    try:
        subjects = db.query(AdvancedSubject).all()
        if not subjects:
            # Créer des matières par défaut si aucune n'existe
            default_subjects = [
                {"name": "Mathématiques", "color": "#3B82F6"},
                {"name": "Sciences", "color": "#10B981"},
                {"name": "Français", "color": "#8B5CF6"},
                {"name": "Histoire", "color": "#F59E0B"},
                {"name": "Anglais", "color": "#EF4444"}
            ]
            
            for subject_data in default_subjects:
                subject = AdvancedSubject(**subject_data)
                db.add(subject)
            
            db.commit()
            db.refresh(subject)
            subjects = db.query(AdvancedSubject).all()
        
        return [
            {
                "id": subject.id,
                "name": subject.name,
                "color": subject.color,
                "note_count": subject.note_count
            }
            for subject in subjects
        ]
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des matières: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des matières"
        )

# ===== CHAPITRES =====
@router.get("/notes-advanced/chapters")
def get_chapters(
    subject_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les chapitres par matière"""
    try:
        query = db.query(AdvancedChapter)
        if subject_id:
            query = query.filter(AdvancedChapter.subject_id == subject_id)
        
        chapters = query.all()
        
        if not chapters and subject_id:
            # Créer des chapitres par défaut selon la matière
            default_chapters = {
                1: [  # Mathématiques
                    {"name": "Algèbre linéaire", "subject_id": 1},
                    {"name": "Calcul différentiel", "subject_id": 1},
                    {"name": "Géométrie", "subject_id": 1}
                ],
                2: [  # Sciences
                    {"name": "Mécanique", "subject_id": 2},
                    {"name": "Thermodynamique", "subject_id": 2},
                    {"name": "Électricité", "subject_id": 2}
                ],
                3: [  # Français
                    {"name": "Grammaire", "subject_id": 3},
                    {"name": "Conjugaison", "subject_id": 3},
                    {"name": "Vocabulaire", "subject_id": 3}
                ]
            }
            
            if subject_id in default_chapters:
                for chapter_data in default_chapters[subject_id]:
                    chapter = AdvancedChapter(**chapter_data)
                    db.add(chapter)
                
                db.commit()
                chapters = db.query(AdvancedChapter).filter(AdvancedChapter.subject_id == subject_id).all()
        
        return [
            {
                "id": chapter.id,
                "name": chapter.name,
                "subject_id": chapter.subject_id,
                "note_count": chapter.note_count
            }
            for chapter in chapters
        ]
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des chapitres: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des chapitres"
        )

# ===== NOTES =====
@router.get("/notes-advanced/")
def get_notes(
    subject_id: Optional[int] = None,
    chapter_id: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les notes avancées avec filtres"""
    try:
        query = db.query(AdvancedNote).filter(AdvancedNote.author_id == current_user.id)
        
        # Appliquer les filtres
        if subject_id:
            query = query.filter(AdvancedNote.subject_id == subject_id)
        
        if chapter_id:
            query = query.filter(AdvancedNote.chapter_id == chapter_id)
        
        if search:
            search_lower = search.lower()
            query = query.filter(
                (AdvancedNote.title.ilike(f"%{search_lower}%")) |
                (AdvancedNote.content.ilike(f"%{search_lower}%"))
            )
        
        # Pagination
        total = query.count()
        notes = query.offset(offset).limit(limit).all()
        
        return {
            "notes": [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "subject_id": note.subject_id,
                    "chapter_id": note.chapter_id,
                    "tags": note.tags or [],
                    "color": note.color,
                    "created_at": note.created_at.isoformat() if note.created_at else None,
                    "updated_at": note.updated_at.isoformat() if note.updated_at else None,
                    "is_favorite": note.is_favorite,
                    "is_shared": note.is_shared,
                    "shared_with": note.shared_with or [],
                    "version": note.version,
                    "attachments": []  # Pour l'instant, pas de pièces jointes
                }
                for note in notes
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des notes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des notes"
        )

@router.post("/notes-advanced/")
def create_note(
    note_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle note avancée"""
    try:
        # Extraire les données de la note
        title = note_data.get("title")
        content = note_data.get("content")
        subject_id = note_data.get("subject_id")
        chapter_id = note_data.get("chapter_id")
        tags = note_data.get("tags", [])
        color = note_data.get("color", "#3B82F6")
        
        # Validation des champs obligatoires
        if not title or not content or not subject_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tous les champs obligatoires doivent être remplis"
            )
        
        # Créer la nouvelle note
        new_note = AdvancedNote(
            title=title,
            content=content,
            subject_id=subject_id,
            chapter_id=chapter_id,
            tags=tags if isinstance(tags, list) else [],
            color=color,
            author_id=current_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        
        print(f"✅ Note créée avec succès: {new_note.id}")
        
        # Mettre à jour le compteur de notes du chapitre si applicable
        if chapter_id:
            chapter = db.query(AdvancedChapter).filter(AdvancedChapter.id == chapter_id).first()
            if chapter:
                chapter.note_count += 1
                db.commit()
        
        # Mettre à jour le compteur de notes de la matière
        subject = db.query(AdvancedSubject).filter(AdvancedSubject.id == subject_id).first()
        if subject:
            subject.note_count += 1
            db.commit()
        
        return {
            "id": new_note.id,
            "title": new_note.title,
            "content": new_note.content,
            "subject_id": new_note.subject_id,
            "chapter_id": new_note.chapter_id,
            "tags": new_note.tags or [],
            "color": new_note.color,
            "created_at": new_note.created_at.isoformat() if new_note.created_at else None,
            "updated_at": new_note.updated_at.isoformat() if new_note.updated_at else None,
            "is_favorite": new_note.is_favorite,
            "is_shared": new_note.is_shared,
            "shared_with": new_note.shared_with or [],
            "version": new_note.version,
            "attachments": []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la création de la note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création de la note"
        )

@router.get("/notes-advanced/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une note spécifique"""
    try:
        note = db.query(AdvancedNote).filter(
            AdvancedNote.id == note_id,
            AdvancedNote.author_id == current_user.id
        ).first()
        
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note non trouvée"
            )
        
        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject_id": note.subject_id,
            "chapter_id": note.chapter_id,
            "tags": note.tags or [],
            "color": note.color,
            "created_at": note.created_at.isoformat() if note.created_at else None,
            "updated_at": note.updated_at.isoformat() if note.updated_at else None,
            "is_favorite": note.is_favorite,
            "is_shared": note.is_shared,
            "shared_with": note.shared_with or [],
            "version": note.version,
            "attachments": []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de la note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de la note"
        )

@router.put("/notes-advanced/{note_id}")
def update_note(
    note_id: int,
    note_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour une note existante"""
    try:
        note = db.query(AdvancedNote).filter(
            AdvancedNote.id == note_id,
            AdvancedNote.author_id == current_user.id
        ).first()
        
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note non trouvée"
            )
        
        # Mettre à jour les champs
        if "title" in note_data:
            note.title = note_data["title"]
        if "content" in note_data:
            note.content = note_data["content"]
        if "subject_id" in note_data:
            note.subject_id = note_data["subject_id"]
        if "chapter_id" in note_data:
            note.chapter_id = note_data["chapter_id"]
        if "tags" in note_data:
            note.tags = note_data["tags"]
        if "color" in note_data:
            note.color = note_data["color"]
        
        note.updated_at = datetime.utcnow()
        note.version += 1
        
        db.commit()
        db.refresh(note)
        
        print(f"✅ Note mise à jour avec succès: {note.id}")
        
        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject_id": note.subject_id,
            "chapter_id": note.chapter_id,
            "tags": note.tags or [],
            "color": note.color,
            "created_at": note.created_at.isoformat() if note.created_at else None,
            "updated_at": note.updated_at.isoformat() if note.updated_at else None,
            "is_favorite": note.is_favorite,
            "is_shared": note.is_shared,
            "shared_with": note.shared_with or [],
            "version": note.version,
            "attachments": []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la mise à jour de la note"
        )

@router.delete("/notes-advanced/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer une note"""
    try:
        note = db.query(AdvancedNote).filter(
            AdvancedNote.id == note_id,
            AdvancedNote.author_id == current_user.id
        ).first()
        
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note non trouvée"
            )
        
        # Mettre à jour les compteurs avant suppression
        if note.chapter_id:
            chapter = db.query(AdvancedChapter).filter(AdvancedChapter.id == note.chapter_id).first()
            if chapter and chapter.note_count > 0:
                chapter.note_count -= 1
        
        subject = db.query(AdvancedSubject).filter(AdvancedSubject.id == note.subject_id).first()
        if subject and subject.note_count > 0:
            subject.note_count -= 1
        
        db.delete(note)
        db.commit()
        
        print(f"✅ Note supprimée avec succès: {note_id}")
        
        return {"message": f"Note {note_id} supprimée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la suppression de la note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la suppression de la note"
        ) 