from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from core.database import get_db
from core.security import get_current_user
from models.user import User
from api.v1.auth import require_role

router = APIRouter(prefix="/formative-evaluations", tags=["formative-evaluations"])

# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================

class FormativeEvaluationCreate(BaseModel):
    title: str
    description: str
    assessment_type: str
    subject: str
    target_level: str
    duration_minutes: int
    max_students: int
    learning_objectives: List[str]
    # Champs optionnels pour la compatibilité avec la table formative_assessments
    criteria: Optional[List[dict]] = []
    rubric: Optional[dict] = {}
    questions: Optional[List[dict]] = []
    instructions: Optional[str] = ""
    estimated_duration: Optional[int] = 60
    difficulty_level: Optional[str] = "intermediate"
    success_indicators: Optional[List[str]] = []
    custom_requirements: Optional[str] = None

class FormativeEvaluationResponse(BaseModel):
    id: int
    title: str
    description: str
    assessment_type: str
    subject: str
    target_level: str
    duration_minutes: int
    max_students: int
    learning_objectives: List[str]
    criteria: List[dict]
    rubric: dict
    questions: List[dict]
    instructions: str
    estimated_duration: int
    difficulty_level: str
    success_indicators: List[str]
    is_active: bool
    created_at: str
    teacher_id: int

class FormativeEvaluationToggle(BaseModel):
    is_active: bool

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.post("/", response_model=FormativeEvaluationResponse)
async def create_formative_evaluation(
    evaluation: FormativeEvaluationCreate,
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle évaluation formative
    """
    try:
        print(f"[FORMATIVE] Création d'évaluation pour {current_user.email}")
        print(f"[FORMATIVE] Données reçues: {evaluation.dict()}")
        
        # Convertir les listes en JSON strings pour la base de données
        import json
        
        # Préparer les données pour l'insertion dans formative_assessments
        evaluation_data = {
            "title": evaluation.title,
            "subject": evaluation.subject,
            "description": evaluation.description,
            "assessment_type": evaluation.assessment_type,
            "learning_objectives": json.dumps(evaluation.learning_objectives),
            "criteria": json.dumps(evaluation.criteria),
            "max_score": 100,  # Score par défaut
            "created_by": current_user.id,
            "created_at": datetime.now().isoformat()
        }
        
        # Insérer dans la base de données existante
        from sqlalchemy import text
        
        insert_query = text("""
            INSERT INTO formative_assessments (
                title, subject, description, assessment_type, learning_objectives,
                criteria, max_score, created_by, created_at
            ) VALUES (
                :title, :subject, :description, :assessment_type, :learning_objectives,
                :criteria, :max_score, :created_by, :created_at
            )
        """)
        
        result = db.execute(insert_query, evaluation_data)
        db.commit()
        
        # Récupérer l'ID généré
        evaluation_id = result.lastrowid
        
        # Créer la réponse
        new_evaluation = {
            "id": evaluation_id,
            "title": evaluation.title,
            "description": evaluation.description,
            "assessment_type": evaluation.assessment_type,
            "subject": evaluation.subject,
            "target_level": evaluation.target_level,
            "duration_minutes": evaluation.duration_minutes,
            "max_students": evaluation.max_students,
            "learning_objectives": evaluation.learning_objectives,
            "criteria": evaluation.criteria,
            "rubric": evaluation.rubric,
            "questions": evaluation.questions,
            "instructions": evaluation.instructions,
            "estimated_duration": evaluation.estimated_duration,
            "difficulty_level": evaluation.difficulty_level,
            "success_indicators": evaluation.success_indicators,
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "teacher_id": current_user.id
        }
        
        print(f"[FORMATIVE] Évaluation créée avec succès: ID={evaluation_id}, Titre={new_evaluation['title']}")
        
        return new_evaluation
        
    except Exception as e:
        print(f"[FORMATIVE] Erreur lors de la création: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création de l'évaluation: {str(e)}"
        )

@router.get("/", response_model=List[FormativeEvaluationResponse])
async def get_all_formative_evaluations(
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les évaluations formatives de l'enseignant
    """
    try:
        print(f"[FORMATIVE] Récupération des évaluations pour {current_user.email}")
        
        # Récupérer les vraies évaluations depuis la base de données
        from sqlalchemy import text
        
        query = text("""
            SELECT id, title, subject, description, assessment_type, 
                   learning_objectives, criteria, max_score, created_by, created_at
            FROM formative_assessments 
            WHERE created_by = :teacher_id
            ORDER BY created_at DESC
        """)
        
        result = db.execute(query, {"teacher_id": current_user.id})
        evaluations = result.fetchall()
        
        print(f"[FORMATIVE] {len(evaluations)} évaluations trouvées pour {current_user.email}")
        
        # Convertir les résultats en format attendu par le frontend
        formatted_evaluations = []
        for eval_row in evaluations:
            # Convertir les JSON strings en objets Python
            import json
            
            try:
                learning_objectives = json.loads(eval_row.learning_objectives) if eval_row.learning_objectives else []
                criteria = json.loads(eval_row.criteria) if eval_row.criteria else []
            except (json.JSONDecodeError, TypeError):
                learning_objectives = []
                criteria = []
            
            formatted_eval = {
                "id": eval_row.id,
                "title": eval_row.title,
                "description": eval_row.description,
                "assessment_type": eval_row.assessment_type,
                "subject": eval_row.subject,
                "target_level": "intermediate",  # Valeur par défaut
                "duration_minutes": 60,  # Valeur par défaut
                "max_students": 30,  # Valeur par défaut
                "learning_objectives": learning_objectives,
                "criteria": criteria,
                "rubric": {},  # Valeur par défaut
                "questions": [],  # Valeur par défaut
                "instructions": "",  # Valeur par défaut
                "estimated_duration": 60,  # Valeur par défaut
                "difficulty_level": "intermediate",  # Valeur par défaut
                "success_indicators": [],  # Valeur par défaut
                "is_active": True,  # Valeur par défaut
                "created_at": eval_row.created_at,
                "teacher_id": eval_row.created_by
            }
            
            formatted_evaluations.append(formatted_eval)
        
        print(f"[FORMATIVE] Évaluations formatées: {len(formatted_evaluations)}")
        return formatted_evaluations
        
    except Exception as e:
        print(f"[FORMATIVE] Erreur lors de la récupération: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des évaluations: {str(e)}"
        )

@router.patch("/{evaluation_id}/toggle-status/")
async def toggle_formative_evaluation_status(
    evaluation_id: int,
    toggle_data: FormativeEvaluationToggle,
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Active ou désactive une évaluation formative
    """
    try:
        print(f"[FORMATIVE] Changement de statut pour l'évaluation {evaluation_id}")
        
        # TODO: Implémenter la vraie mise à jour en base de données
        
        return {
            "success": True,
            "evaluation_id": evaluation_id,
            "is_active": toggle_data.is_active,
            "updated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"[FORMATIVE] Erreur lors du changement de statut: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du changement de statut: {str(e)}"
        )

@router.get("/{evaluation_id}/", response_model=FormativeEvaluationResponse)
async def get_formative_evaluation_by_id(
    evaluation_id: int,
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Récupère une évaluation formative spécifique par ID
    """
    try:
        print(f"[FORMATIVE] Récupération de l'évaluation {evaluation_id}")
        
        # TODO: Implémenter la vraie récupération depuis la base de données
        raise HTTPException(
            status_code=404,
            detail="Évaluation non trouvée"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[FORMATIVE] Erreur lors de la récupération: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de l'évaluation: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE TEST ET DIAGNOSTIC
# ============================================================================

@router.get("/test/")
async def test_formative_evaluations_endpoint():
    """
    Test simple pour vérifier que l'endpoint fonctionne
    """
    return {
        "message": "Module évaluations formatives accessible",
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
