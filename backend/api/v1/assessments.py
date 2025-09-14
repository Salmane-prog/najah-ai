#!/usr/bin/env python3
"""
API pour la gestion des évaluations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult
from models.class_group import ClassGroup, ClassStudent
# Pas de modèle Subject, le sujet est un champ string dans Quiz
from core.security import get_current_user

router = APIRouter(prefix="/api/v1/assessments", tags=["Assessments"])

# ============================================================================
# ENDPOINTS POUR LES ASSESSMENTS
# ============================================================================

@router.get("/student/{student_id}/pending")
async def get_student_pending_assessments(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les assessments en attente d'un étudiant"""
    try:
        # Vérifier que l'utilisateur peut accéder à ces données
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé aux assessments de cet étudiant"
            )
        
        # Récupérer les classes de l'étudiant
        student_classes = db.query(ClassGroup).join(ClassStudent).filter(
            ClassStudent.student_id == student_id
        ).all()
        
        if not student_classes:
            return {"status": "success", "data": {"message": "Aucune classe trouvée pour cet étudiant"}}
        
        # Récupérer les assessments des classes de l'étudiant
        pending_assessments = []
        for class_group in student_classes:
            class_assessments = db.query(Quiz).filter(
                Quiz.class_group_id == class_group.id,
                Quiz.is_active == True,
                Quiz.assessment_type == "formative"  # Supposons que c'est le type d'évaluation
            ).all()
            
            for assessment in class_assessments:
                # Vérifier si l'étudiant a déjà passé cet assessment
                existing_result = db.query(QuizResult).filter(
                    QuizResult.user_id == student_id,
                    QuizResult.quiz_id == assessment.id
                ).first()
                
                if not existing_result:  # Seulement les assessments non passés
                    assessment_data = {
                        "id": assessment.id,
                        "title": assessment.title,
                        "description": assessment.description,
                        "subject": assessment.subject if assessment.subject else "Général",
                        "class_name": class_group.name,
                        "type": "formative",
                        "difficulty": assessment.difficulty,
                        "estimated_time": assessment.estimated_time,
                        "total_questions": assessment.total_questions if hasattr(assessment, 'total_questions') else 10,
                        "due_date": None,  # À implémenter avec une vraie table d'assignation
                        "assigned_date": assessment.created_at.isoformat(),
                        "status": "pending"
                    }
                    
                    pending_assessments.append(assessment_data)
        
        # Si aucun assessment en attente, retourner une liste vide
        if not pending_assessments:
            return {"status": "success", "data": []}
        
        return {"status": "success", "data": pending_assessments}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des assessments: {str(e)}"
        )

@router.get("/student/{student_id}/completed")
async def get_student_completed_assessments(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les assessments complétés d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les résultats des assessments
        completed_assessments = db.query(QuizResult).filter(
            QuizResult.user_id == student_id
        ).all()
        
        if not completed_assessments:
            return {"status": "success", "data": []}
        
        assessment_data = []
        for result in completed_assessments:
            if result.quiz:
                assessment_info = {
                    "id": result.quiz.id,
                    "title": result.quiz.title,
                                            "subject": result.quiz.subject if result.quiz.subject else "Général",
                    "score": result.score,
                    "is_correct": result.is_correct,
                    "completed_at": result.created_at.isoformat(),
                    "time_taken": result.time_taken if hasattr(result, 'time_taken') else None,
                    "total_questions": result.quiz.total_questions if hasattr(result.quiz, 'total_questions') else 10
                }
                assessment_data.append(assessment_info)
        
        return {"status": "success", "data": assessment_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/upcoming")
async def get_student_upcoming_assessments(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les assessments à venir d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Pour l'instant, retourner une liste vide
        # À implémenter avec une vraie table de planning d'assessments
        return {"status": "success", "data": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS POUR LES PROFESSEURS
# ============================================================================

@router.get("/teacher/{teacher_id}/class/{class_id}")
async def get_class_assessments(
    teacher_id: int,
    class_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les assessments d'une classe"""
    try:
        if current_user.role.value != "teacher" or current_user.id != teacher_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == teacher_id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Récupérer les assessments de la classe
        class_assessments = db.query(Quiz).filter(
            Quiz.class_group_id == class_id,
            Quiz.is_active == True
        ).all()
        
        assessment_data = []
        for assessment in class_assessments:
            # Calculer les statistiques de la classe
            class_results = db.query(QuizResult).filter(
                QuizResult.quiz_id == assessment.id
            ).all()
            
            if class_results:
                scores = [result.score for result in class_results if result.score is not None]
                average_score = round(sum(scores) / len(scores), 2) if scores else 0
                completion_rate = round(len(class_results) / len(class_group.students) * 100, 2) if class_group.students else 0
            else:
                average_score = 0
                completion_rate = 0
            
            assessment_info = {
                "id": assessment.id,
                "title": assessment.title,
                "description": assessment.description,
                "subject": assessment.subject if assessment.subject else "Général",
                "difficulty": assessment.difficulty,
                "estimated_time": assessment.estimated_time,
                "total_questions": assessment.total_questions if hasattr(assessment, 'total_questions') else 10,
                "created_at": assessment.created_at.isoformat(),
                "due_date": None,  # À implémenter
                "class_stats": {
                    "total_students": len(class_group.students),
                    "completed_count": len(class_results),
                    "completion_rate": completion_rate,
                    "average_score": average_score
                }
            }
            
            assessment_data.append(assessment_info)
        
        return {"status": "success", "data": assessment_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/create")
async def create_assessment(
    assessment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un nouvel assessment"""
    try:
        if current_user.role.value != "teacher":
            raise HTTPException(status_code=403, detail="Seuls les professeurs peuvent créer des assessments")
        
        # Extraire les données
        title = assessment_data.get("title")
        description = assessment_data.get("description")
        subject_id = assessment_data.get("subject_id")
        class_id = assessment_data.get("class_id")
        difficulty = assessment_data.get("difficulty", "medium")
        estimated_time = assessment_data.get("estimated_time", 30)
        assessment_type = assessment_data.get("type", "formative")
        
        if not title or not class_id:
            raise HTTPException(status_code=400, detail="Titre et ID de classe requis")
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée ou accès non autorisé")
        
        # Créer le nouvel assessment
        new_assessment = Quiz(
            title=title,
            description=description,
            subject_id=subject_id,
            class_group_id=class_id,
            difficulty=difficulty,
            estimated_time=estimated_time,
            assessment_type=assessment_type,
            is_active=True,
            created_by=current_user.id,
            created_at=datetime.now()
        )
        
        db.add(new_assessment)
        db.commit()
        db.refresh(new_assessment)
        
        return {
            "status": "success",
            "message": f"Assessment '{title}' créé avec succès",
            "data": {
                "id": new_assessment.id,
                "title": new_assessment.title,
                "class_id": new_assessment.class_group_id,
                "created_at": new_assessment.created_at.isoformat()
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/{assessment_id}")
async def update_assessment(
    assessment_id: int,
    assessment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un assessment"""
    try:
        if current_user.role.value != "teacher":
            raise HTTPException(status_code=403, detail="Seuls les professeurs peuvent modifier des assessments")
        
        # Récupérer l'assessment
        assessment = db.query(Quiz).filter(Quiz.id == assessment_id).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment non trouvé")
        
        # Vérifier que le professeur peut modifier cet assessment
        if assessment.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cet assessment")
        
        # Mettre à jour les champs
        for field, value in assessment_data.items():
            if hasattr(assessment, field) and value is not None:
                setattr(assessment, field, value)
        
        assessment.updated_at = datetime.now()
        db.commit()
        
        return {
            "status": "success",
            "message": f"Assessment '{assessment.title}' mis à jour avec succès"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.delete("/{assessment_id}")
async def delete_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un assessment"""
    try:
        if current_user.role.value != "teacher":
            raise HTTPException(status_code=403, detail="Seuls les professeurs peuvent supprimer des assessments")
        
        # Récupérer l'assessment
        assessment = db.query(Quiz).filter(Quiz.id == assessment_id).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment non trouvé")
        
        # Vérifier que le professeur peut supprimer cet assessment
        if assessment.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cet assessment")
        
        # Vérifier qu'aucun étudiant n'a passé cet assessment
        existing_results = db.query(QuizResult).filter(QuizResult.quiz_id == assessment_id).count()
        if existing_results > 0:
            raise HTTPException(
                status_code=400, 
                detail="Impossible de supprimer un assessment déjà passé par des étudiants"
            )
        
        # Supprimer l'assessment
        db.delete(assessment)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Assessment '{assessment.title}' supprimé avec succès"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS POUR LES STATISTIQUES
# ============================================================================

@router.get("/stats/student/{student_id}")
async def get_student_assessment_stats(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les statistiques d'assessment d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer tous les résultats de l'étudiant
        all_results = db.query(QuizResult).filter(QuizResult.user_id == student_id).all()
        
        if not all_results:
            return {"status": "success", "data": {"message": "Aucun assessment trouvé"}}
        
        # Calculer les statistiques
        total_assessments = len(all_results)
        scores = [result.score for result in all_results if result.score is not None]
        average_score = round(sum(scores) / len(scores), 2) if scores else 0
        
        # Performance par sujet
        performance_by_subject = {}
        for result in all_results:
            if result.quiz and result.quiz.subject:
                subject = result.quiz.subject.name
                if subject not in performance_by_subject:
                    performance_by_subject[subject] = {"total": 0, "scores": []}
                
                performance_by_subject[subject]["total"] += 1
                if result.score is not None:
                    performance_by_subject[subject]["scores"].append(result.score)
        
        # Calculer les moyennes par sujet
        for subject in performance_by_subject:
            scores = performance_by_subject[subject]["scores"]
            if scores:
                performance_by_subject[subject]["average_score"] = round(sum(scores) / len(scores), 2)
            else:
                performance_by_subject[subject]["average_score"] = 0
        
        stats = {
            "student_id": student_id,
            "total_assessments": total_assessments,
            "average_score": average_score,
            "performance_by_subject": performance_by_subject,
            "last_assessment": max([result.created_at for result in all_results]).isoformat() if all_results else None
        }
        
        return {"status": "success", "data": stats}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
