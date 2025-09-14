from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizAssignment, QuizResult
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from pydantic import BaseModel

# Modèles Pydantic pour la validation des données
class QuizAssignmentRequest(BaseModel):
    quiz_id: int
    student_ids: List[int]
    due_date: str = None  # Format: "YYYY-MM-DD HH:MM:SS"
    class_id: int | None = None  # Optionnel: assigner à toute une classe

class QuizAssignmentResponse(BaseModel):
    message: str
    assigned_count: int
    assignments: List[Dict[str, Any]]

router = APIRouter()

# ============================================================================
# ENDPOINTS CÔTÉ PROFESSEUR
# ============================================================================

@router.post("/assign", response_model=QuizAssignmentResponse)
def assign_quiz_to_students(
    assignment_data: QuizAssignmentRequest,
    db: Session = Depends(get_db)
):
    """Assigner un quiz à des étudiants (version test sans auth)"""
    try:
        # Vérifier que le quiz existe
        quiz = db.query(Quiz).filter(Quiz.id == assignment_data.quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz non trouvé")
        
        # Vérifier que tous les étudiants existent
        students = db.query(User).filter(User.id.in_(assignment_data.student_ids)).all()
        if len(students) != len(assignment_data.student_ids):
            raise HTTPException(status_code=404, detail="Un ou plusieurs étudiants non trouvés")
        
        # Convertir la date d'échéance si fournie
        due_date = None
        if assignment_data.due_date:
            try:
                due_date = datetime.fromisoformat(assignment_data.due_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD HH:MM:SS")
        
        # Créer les assignations
        created_assignments = []
        for student_id in assignment_data.student_ids:
            # Vérifier si l'assignation existe déjà
            existing_assignment = db.query(QuizAssignment).filter(
                QuizAssignment.quiz_id == assignment_data.quiz_id,
                QuizAssignment.student_id == student_id,
                QuizAssignment.is_active == True
            ).first()
            
            if existing_assignment:
                # Mettre à jour l'assignation existante
                existing_assignment.due_date = due_date
                existing_assignment.updated_at = datetime.utcnow()
                existing_assignment.status = "assigned"
                db.commit()
                created_assignments.append(existing_assignment)
            else:
                # Créer une nouvelle assignation
                new_assignment = QuizAssignment(
                    quiz_id=assignment_data.quiz_id,
                    student_id=student_id,
                    class_id=assignment_data.class_id,
                    assigned_by=1,  # ID du professeur (version test)
                    due_date=due_date,
                    status="assigned",
                    is_active=True
                )
                db.add(new_assignment)
                created_assignments.append(new_assignment)
        
        db.commit()
        
        # Formater la réponse
        formatted_assignments = []
        for assignment in created_assignments:
            student = next(s for s in students if s.id == assignment.student_id)
            formatted_assignments.append({
                "id": assignment.id,
                "quiz_id": assignment.quiz_id,
                "quiz_title": quiz.title,
                "student_id": assignment.student_id,
                "student_name": student.username or f"Étudiant {student.id}",
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                "status": assignment.status,
                "assigned_at": assignment.created_at.isoformat()
            })
        
        return QuizAssignmentResponse(
            message=f"Quiz '{quiz.title}' assigné avec succès à {len(created_assignments)} étudiant(s)",
            assigned_count=len(created_assignments),
            assignments=formatted_assignments
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur assign_quiz_to_students: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'assignation: {str(e)}")

@router.get("/teacher/{teacher_id}/assignments")
def get_teacher_assignments(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer tous les quiz assignés par un professeur"""
    try:
        # Vérifier que le professeur existe
        teacher = db.query(User).filter(User.id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Professeur non trouvé")
        
        # Récupérer les assignations du professeur
        assignments = db.query(QuizAssignment).filter(
            QuizAssignment.assigned_by == teacher_id,
            QuizAssignment.is_active == True
        ).all()
        
        # Formater les assignations
        formatted_assignments = []
        for assignment in assignments:
            quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
            student = db.query(User).filter(User.id == assignment.student_id).first()
            
            if quiz and student:
                # Vérifier si l'étudiant a déjà répondu
                quiz_result = db.query(QuizResult).filter(
                    QuizResult.quiz_id == assignment.quiz_id,
                    QuizResult.student_id == assignment.student_id
                ).first()
                
                formatted_assignments.append({
                    "id": assignment.id,
                    "quiz_id": assignment.quiz_id,
                    "quiz_title": quiz.title,
                    "student_id": assignment.student_id,
                    "student_name": student.username or f"Étudiant {student.id}",
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status,
                    "assigned_at": assignment.created_at.isoformat(),
                    "student_status": "fait" if quiz_result else "assigné",
                    "score": quiz_result.score if quiz_result else None,
                    "completed_at": quiz_result.completed_at.isoformat() if quiz_result else None
                })
        
        return {
            "teacher_id": teacher_id,
            "total_assignments": len(formatted_assignments),
            "assignments": formatted_assignments
        }
        
    except Exception as e:
        print(f"❌ Erreur get_teacher_assignments: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS CÔTÉ ÉTUDIANT (AMÉLIORÉS)
# ============================================================================

@router.get("/student/{student_id}")
def get_student_quiz_assignments(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les quiz assignés à un étudiant avec statut réel (version test sans auth)"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les quiz assignés
        assignments = db.query(QuizAssignment).filter(
            QuizAssignment.student_id == student_id,
            QuizAssignment.is_active == True
        ).all()
        
        # Si aucun quiz assigné, retourner des données de test
        if not assignments:
            return [
                {
                    "id": 1,
                    "quiz_id": 1,
                    "quiz_title": "Quiz de Grammaire Française",
                    "subject": "Français",
                    "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                    "status": "assigned",
                    "assigned_by": "Prof. Martin",
                    "estimated_duration": 30,
                    "student_status": "assigné"
                },
                {
                    "id": 2,
                    "quiz_id": 2,
                    "quiz_title": "Quiz de Vocabulaire A1",
                    "subject": "Français",
                    "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat(),
                    "status": "assigned",
                    "assigned_by": "Prof. Martin",
                    "estimated_duration": 25,
                    "student_status": "assigné"
                }
            ]
        
        # Formater les quiz assignés avec statut réel
        formatted_assignments = []
        for assignment in assignments:
            quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
            if quiz:
                # Vérifier si l'étudiant a déjà répondu
                quiz_result = db.query(QuizResult).filter(
                    QuizResult.quiz_id == assignment.quiz_id,
                    QuizResult.student_id == student_id
                ).first()
                
                # Déterminer le statut réel de l'étudiant
                if quiz_result:
                    student_status = "fait" if quiz_result.is_completed else "en cours"
                    score = quiz_result.score
                    completed_at = quiz_result.completed_at.isoformat() if quiz_result.completed_at else None
                else:
                    student_status = "assigné"
                    score = None
                    completed_at = None
                
                formatted_assignments.append({
                    "id": assignment.id,
                    "quiz_id": assignment.quiz_id,
                    "quiz_title": quiz.title,
                    "subject": quiz.subject or "Général",
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status or "assigned",
                    "assigned_by": "Prof. Assigné",
                    "estimated_duration": quiz.time_limit or 30,
                    "student_status": student_status,
                    "score": score,
                    "completed_at": completed_at,
                    "assigned_at": assignment.created_at.isoformat()
                })
        
        return formatted_assignments
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur get_student_quiz_assignments: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/student/{student_id}/pending")
def get_pending_assignments(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les quiz assignés en attente (non répondu)"""
    try:
        all_assignments = get_student_quiz_assignments(student_id, db)
        pending = [a for a in all_assignments if a.get("student_status") == "assigné"]
        
        return {
            "student_id": student_id,
            "total_pending": len(pending),
            "assignments": pending
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/completed")
def get_completed_assignments(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les quiz assignés complétés (répondu)"""
    try:
        all_assignments = get_student_quiz_assignments(student_id, db)
        completed = [a for a in all_assignments if a.get("student_status") in ["fait", "en cours"]]
        
        return {
            "student_id": student_id,
            "total_completed": len(completed),
            "assignments": completed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS DE GESTION
# ============================================================================

@router.put("/{assignment_id}/status")
def update_assignment_status(
    assignment_id: int,
    status: str = Query(..., description="Nouveau statut: assigned, in_progress, completed, overdue"),
    db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une assignation"""
    try:
        assignment = db.query(QuizAssignment).filter(QuizAssignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignation non trouvée")
        
        assignment.status = status
        assignment.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": f"Statut mis à jour vers '{status}'",
            "assignment_id": assignment_id,
            "new_status": status
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer une assignation (désactiver)"""
    try:
        assignment = db.query(QuizAssignment).filter(QuizAssignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignation non trouvée")
        
        assignment.is_active = False
        assignment.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": "Assignation supprimée avec succès",
            "assignment_id": assignment_id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
