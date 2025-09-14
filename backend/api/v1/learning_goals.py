from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

from core.database import get_db
from api.v1.auth import require_role
from models.user import User
from models.organization import LearningGoal

router = APIRouter()

@router.get("/learning-goals")
def get_learning_goals(
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer les objectifs d'apprentissage d'un étudiant."""
    try:
        # Utiliser une requête SQL directe pour récupérer rowid
        from sqlalchemy import text
        query = text("""
            SELECT rowid as id, title, description, subject, target_date, progress, status, created_at
            FROM learning_goals 
            ORDER BY created_at DESC
        """)
        
        result = db.execute(query)
        goals_list = []
        for row in result:
            goals_list.append({
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "subject": row.subject,
                "target_date": row.target_date.isoformat() if row.target_date and hasattr(row.target_date, 'isoformat') else str(row.target_date) if row.target_date else None,
                "progress": row.progress,
                "status": row.status,
                "created_at": row.created_at.isoformat() if row.created_at and hasattr(row.created_at, 'isoformat') else str(row.created_at) if row.created_at else None
            })
        
        return goals_list
        
    except Exception as e:
        print(f"Erreur dans get_learning_goals: {str(e)}")
        return []

@router.post("/learning-goals")
def create_learning_goal(
    goal_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Créer un nouvel objectif d'apprentissage."""
    try:
        # Utiliser SQL direct pour éviter les problèmes SQLAlchemy
        from sqlalchemy import text
        
        insert_query = text("""
            INSERT INTO learning_goals (title, description, subject, target_date, progress, status, user_id, created_at)
            VALUES (:title, :description, :subject, :target_date, :progress, :status, :user_id, :created_at)
        """)
        
        target_date = datetime.fromisoformat(goal_data.get("target_date")) if goal_data.get("target_date") else None
        created_at = datetime.utcnow()
        
        result = db.execute(insert_query, {
            "title": goal_data.get("title"),
            "description": goal_data.get("description"),
            "subject": goal_data.get("subject"),
            "target_date": target_date,
            "progress": 0.0,
            "status": "active",
            "user_id": current_user.id,
            "created_at": created_at
        })
        
        db.commit()
        
        # Récupérer l'ID généré (utiliser rowid)
        goal_id = result.lastrowid
        
        return {
            "id": goal_id,
            "title": goal_data.get("title"),
            "description": goal_data.get("description"),
            "subject": goal_data.get("subject"),
            "target_date": goal_data.get("target_date"),
            "progress": 0.0,
            "status": "active",
            "created_at": created_at.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans create_learning_goal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'objectif: {str(e)}")

@router.post("/learning-goals/{goal_id}/update")
def update_learning_goal(
    goal_id: int,
    goal_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Modifier un objectif d'apprentissage."""
    print(f"🔧 Tentative de modification de l'objectif {goal_id}")
    try:
        # Utiliser une requête SQL directe pour récupérer par rowid
        from sqlalchemy import text
        query = text("""
            SELECT rowid as id, title, description, subject, target_date, progress, status, created_at
            FROM learning_goals 
            WHERE rowid = :goal_id AND user_id = :user_id
        """)
        
        result = db.execute(query, {"goal_id": goal_id, "user_id": current_user.id})
        goal_data_current = result.fetchone()
        
        if not goal_data_current:
            raise HTTPException(status_code=404, detail="Objectif non trouvé")
        
        # Construire la requête de mise à jour
        update_fields = []
        update_values = {"goal_id": goal_id, "user_id": current_user.id}
        
        if "title" in goal_data:
            update_fields.append("title = :title")
            update_values["title"] = goal_data["title"]
        if "description" in goal_data:
            update_fields.append("description = :description")
            update_values["description"] = goal_data["description"]
        if "subject" in goal_data:
            update_fields.append("subject = :subject")
            update_values["subject"] = goal_data["subject"]
        if "target_date" in goal_data:
            update_fields.append("target_date = :target_date")
            update_values["target_date"] = datetime.fromisoformat(goal_data["target_date"]) if goal_data["target_date"] else None
        if "progress" in goal_data:
            update_fields.append("progress = :progress")
            update_values["progress"] = goal_data["progress"]
        if "status" in goal_data:
            update_fields.append("status = :status")
            update_values["status"] = goal_data["status"]
        
        if update_fields:
            update_query = text(f"""
                UPDATE learning_goals 
                SET {', '.join(update_fields)}
                WHERE rowid = :goal_id AND user_id = :user_id
            """)
            db.execute(update_query, update_values)
            db.commit()
        
        # Récupérer l'objectif mis à jour
        result = db.execute(query, {"goal_id": goal_id, "user_id": current_user.id})
        updated_goal = result.fetchone()
        
        return {
            "id": updated_goal.id,
            "title": updated_goal.title,
            "description": updated_goal.description,
            "subject": updated_goal.subject,
            "target_date": updated_goal.target_date.isoformat() if updated_goal.target_date and hasattr(updated_goal.target_date, 'isoformat') else str(updated_goal.target_date) if updated_goal.target_date else None,
            "progress": updated_goal.progress,
            "status": updated_goal.status,
            "created_at": updated_goal.created_at.isoformat() if updated_goal.created_at and hasattr(updated_goal.created_at, 'isoformat') else str(updated_goal.created_at) if updated_goal.created_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur dans update_learning_goal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de l'objectif: {str(e)}")

@router.post("/learning-goals/{goal_id}/delete")
def delete_learning_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Supprimer un objectif d'apprentissage."""
    print(f"🗑️ Tentative de suppression de l'objectif {goal_id}")
    try:
        # Utiliser une requête SQL directe pour supprimer par rowid
        from sqlalchemy import text
        
        # Vérifier que l'objectif existe et appartient à l'utilisateur
        check_query = text("""
            SELECT rowid FROM learning_goals 
            WHERE rowid = :goal_id AND user_id = :user_id
        """)
        
        result = db.execute(check_query, {"goal_id": goal_id, "user_id": current_user.id})
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Objectif non trouvé")
        
        # Supprimer l'objectif
        delete_query = text("""
            DELETE FROM learning_goals 
            WHERE rowid = :goal_id AND user_id = :user_id
        """)
        
        db.execute(delete_query, {"goal_id": goal_id, "user_id": current_user.id})
        db.commit()
        
        return {"message": "Objectif supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur dans delete_learning_goal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'objectif: {str(e)}") 