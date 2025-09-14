#!/usr/bin/env python3
"""
API pour le forum d'entraide
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.forum import ForumCategory, ForumThread, ForumReply
from schemas.forum import ForumThreadCreate, ForumThreadResponse

router = APIRouter(tags=["forum"])

def safe_parse_tags(tags_string):
    """Parse les tags de manière sécurisée, retourne une liste vide si invalide"""
    if not tags_string:
        return []
    
    try:
        # Essayer de parser le JSON
        parsed = json.loads(tags_string)
        if isinstance(parsed, list):
            return parsed
        else:
            return []
    except (json.JSONDecodeError, TypeError):
        # Si le parsing échoue, retourner une liste vide
        print(f"Warning: Tags invalides détectés: '{tags_string}'")
        return []

# ===== CATÉGORIES =====

@router.get("/categories")
def get_forum_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer toutes les catégories du forum"""
    categories = db.query(ForumCategory).all()
    
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "subject": cat.subject,
            "level": cat.level,
            "thread_count": len(cat.threads)
        }
        for cat in categories
    ]

@router.post("/categories")
def create_forum_category(
    name: str,
    description: Optional[str] = None,
    color: str = "#3B82F6",
    icon: str = "chat-bubble",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle catégorie (admin seulement)"""
    # Vérifier que l'utilisateur est admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les administrateurs peuvent créer des catégories"
        )
    
    # Vérifier que la catégorie n'existe pas déjà
    existing = db.query(ForumCategory).filter(ForumCategory.name == name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une catégorie avec ce nom existe déjà"
        )
    
    category = ForumCategory(
        name=name,
        description=description,
        color=color,
        icon=icon
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "color": category.color,
        "icon": category.icon
    }

# ===== THREADS =====

@router.get("/threads")
def get_forum_threads(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les threads du forum avec filtres"""
    try:
        query = db.query(ForumThread)
        
        if category_id:
            query = query.filter(ForumThread.category_id == category_id)
        
        if search:
            query = query.filter(
                ForumThread.title.contains(search) | 
                ForumThread.content.contains(search)
            )
        
        threads = query.order_by(ForumThread.is_pinned.desc(), ForumThread.updated_at.desc()).offset(offset).limit(limit).all()
        
        return [
            {
                "id": thread.id,
                "title": thread.title,
                "content": thread.content[:200] + "..." if len(thread.content) > 200 else thread.content,
                "category": {
                    "id": thread.category.id if thread.category else 0,
                    "name": thread.category.name if thread.category else "Général",
                    "description": thread.category.description if thread.category else ""
                },
                "author": {
                    "id": thread.author.id if thread.author else 0,
                    "name": (thread.author.first_name or "") + " " + (thread.author.last_name or "") if thread.author else "Utilisateur",
                    "email": thread.author.email if thread.author else ""
                },
                "tags": safe_parse_tags(thread.tags),
                "is_pinned": thread.is_pinned,
                "is_locked": thread.is_locked,
                "view_count": thread.view_count,
                "reply_count": thread.reply_count,
                "last_reply_at": thread.last_reply_at,
                "created_at": thread.created_at,
                "updated_at": thread.updated_at
            }
            for thread in threads
        ]
    except Exception as e:
        print(f"Erreur lors de la récupération des threads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des threads"
        )

@router.post("/threads", response_model=ForumThreadResponse)
def create_forum_thread(
    thread_data: ForumThreadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau thread"""
    # Vérifier que la catégorie existe
    category = db.query(ForumCategory).filter(ForumCategory.id == thread_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie non trouvée"
        )
    
    # Créer le thread
    thread = ForumThread(
        title=thread_data.title,
        content=thread_data.content,
        category_id=thread_data.category_id,
        author_id=current_user.id,
        tags=thread_data.tags
    )
    
    db.add(thread)
    db.commit()
    db.refresh(thread)
    
    return thread

@router.get("/threads/{thread_id}")
def get_forum_thread(
    thread_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un thread spécifique avec ses réponses"""
    thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread non trouvé"
        )
    
    # Incrémenter le compteur de vues
    thread.view_count += 1
    db.commit()
    
    return {
        "id": thread.id,
        "title": thread.title,
        "content": thread.content,
        "category": {
            "id": thread.category.id,
            "name": thread.category.name,
            "description": thread.category.description
        },
        "author": {
            "id": thread.author.id,
            "name": (thread.author.first_name or "") + " " + (thread.author.last_name or ""),
            "email": thread.author.email
        },
        "tags": safe_parse_tags(thread.tags),
        "is_pinned": thread.is_pinned,
        "is_locked": thread.is_locked,
        "view_count": thread.view_count,
        "reply_count": thread.reply_count,
        "last_reply_at": thread.last_reply_at,
        "created_at": thread.created_at,
        "updated_at": thread.updated_at,
        "replies": [
            {
                "id": reply.id,
                "content": reply.content,
                "author": {
                    "id": reply.author.id,
                    "name": (reply.author.first_name or "") + " " + (reply.author.last_name or ""),
                    "email": reply.author.email
                },
                "is_solution": reply.is_solution,
                "is_edited": reply.is_edited,
                "edited_at": reply.edited_at,
                "created_at": reply.created_at,
                "updated_at": reply.updated_at
            }
            for reply in thread.replies
        ]
    }

# ===== RÉPONSES =====

@router.post("/threads/{thread_id}/replies")
def create_forum_reply(
    thread_id: int,
    reply_data: dict,  # Accepter un dictionnaire avec le contenu
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une réponse à un thread"""
    try:
        # Vérifier que le thread existe
        thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
        if not thread:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thread non trouvé"
            )
        
        # Vérifier que le thread n'est pas verrouillé
        if thread.is_locked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce thread est verrouillé"
            )
        
        # Extraire le contenu du dictionnaire
        content = reply_data.get("content")
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le contenu de la réponse est requis"
            )
        
        # Créer la réponse
        reply = ForumReply(
            thread_id=thread_id,
            author_id=current_user.id,
            content=content
        )
        
        db.add(reply)
        
        # Mettre à jour le thread
        thread.reply_count += 1
        thread.last_reply_at = datetime.utcnow()
        thread.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(reply)
        
        return {
            "id": reply.id,
            "content": reply.content,
            "author": {
                "id": reply.author.id,
                "name": (reply.author.first_name or "") + " " + (reply.author.last_name or ""),
                "email": reply.author.email
            },
            "created_at": reply.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la création de la réponse: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création de la réponse"
        )

@router.put("/replies/{reply_id}/solution")
def mark_reply_as_solution(
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer une réponse comme solution"""
    reply = db.query(ForumReply).filter(ForumReply.id == reply_id).first()
    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Réponse non trouvée"
        )
    
    # Vérifier que l'utilisateur est l'auteur du thread
    thread = db.query(ForumThread).filter(ForumThread.id == reply.thread_id).first()
    if thread.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul l'auteur du thread peut marquer une réponse comme solution"
        )
    
    # Désactiver toutes les autres solutions
    db.query(ForumReply).filter(
        ForumReply.thread_id == reply.thread_id,
        ForumReply.is_solution == True
    ).update({"is_solution": False})
    
    # Marquer cette réponse comme solution
    reply.is_solution = True
    db.commit()
    
    return {"message": "Réponse marquée comme solution"} 