from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional
from datetime import datetime
import json
from pydantic import BaseModel
import logging

from core.database import get_db
from core.security import get_current_user
from models.user import User, UserRole
from models.adaptive_evaluation import (
    AdaptiveTest, AdaptiveQuestion, TestAssignment, 
    TestAttempt, QuestionResponse, CompetencyAnalysis,
    Class, AdaptiveClassStudent
)

# Configuration du logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Endpoint de test pour vérifier le routage
@router.get("/test-route")
async def test_route():
    """Test simple pour vérifier que le routage fonctionne"""
    print("[DEBUG] 🔥 test_route appelée")
    return {"message": "Route accessible", "status": "ok"}

# Endpoint de test POST pour vérifier l'authentification
@router.post("/test-post")
async def test_post(
    data: dict,
    current_user: User = Depends(get_current_user)
):
    """Test POST pour vérifier l'authentification"""
    print(f"[DEBUG] 🔥 test_post appelée avec user: {current_user.id}, role: {current_user.role}")
    return {"message": "POST route accessible", "user_id": current_user.id, "role": current_user.role.value}

# Endpoint de test spécifique pour /tests/
@router.post("/test-tests")
async def test_tests_endpoint(
    data: dict,
    current_user: User = Depends(get_current_user)
):
    """Test spécifique pour vérifier l'endpoint /tests/"""
    print(f"[DEBUG] 🔥 test_tests_endpoint appelée avec user: {current_user.id}, role: {current_user.role}")
    print(f"[DEBUG] 🔥 Données reçues: {data}")
    return {"message": "Test endpoint accessible", "user_id": current_user.id, "role": current_user.role.value}

@router.post("/debug-create-test")
async def debug_create_test(test_data: dict, current_user: User = Depends(get_current_user)):
    """Endpoint de debug pour création de test"""
    print(f"🔥 DEBUG ENDPOINT APPELÉ !")
    print(f"🔥 User: {current_user.id}, Role: {current_user.role}")
    print(f"🔥 Data: {test_data}")
    
    return {
        "success": True,
        "message": "Debug endpoint fonctionne !",
        "user_id": current_user.id,
        "role": str(current_user.role),
        "data_received": test_data
    }

# Modèle de réponse pour les tests adaptatifs
class AdaptiveTestResponse(BaseModel):
    id: int
    title: str
    subject: str
    description: Optional[str] = None
    difficulty_min: int
    difficulty_max: int
    estimated_duration: int
    total_questions: int
    adaptation_type: str
    learning_objectives: Optional[str] = None
    is_active: bool
    created_by: Optional[int] = None
    created_at: str  # Changé de datetime à str
    updated_at: Optional[str] = None  # Changé de datetime à str

    class Config:
        from_attributes = True

# Modèle pour la soumission des réponses
class QuizSubmissionRequest(BaseModel):
    answers: List[dict]

# ============================================================================
# ENDPOINTS POUR LES TESTS ADAPTATIFS
# ============================================================================

@router.post("/create")
async def create_adaptive_test(
    test_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau test adaptatif"""
    
    print(f"[DEBUG] 🔥 create_adaptive_test appelée - DÉBUT")
    print(f"[DEBUG] current_user.id: {current_user.id}")
    print(f"[DEBUG] current_user.role: {current_user.role}")
    print(f"[DEBUG] current_user.role type: {type(current_user.role)}")
    print(f"[DEBUG] UserRole.teacher: {UserRole.teacher}")
    print(f"[DEBUG] UserRole.teacher type: {type(UserRole.teacher)}")
    print(f"[DEBUG] Comparaison: {current_user.role != UserRole.teacher}")
    print(f"[DEBUG] test_data reçu: {test_data}")
    
    if current_user.role != UserRole.teacher:
        print(f"[DEBUG] ❌ Accès refusé: rôle {current_user.role} != {UserRole.teacher}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les enseignants peuvent créer des tests"
        )
    
    print(f"[DEBUG] ✅ Autorisation accordée, création du test...")
    
    try:
        # Créer le test
        new_test = AdaptiveTest(
            title=test_data["title"],
            subject=test_data["subject"],
            description=test_data.get("description", ""),
            difficulty_min=test_data.get("difficulty_min", 1),
            difficulty_max=test_data.get("difficulty_max", 10),
            estimated_duration=test_data.get("estimated_duration", 30),
            total_questions=test_data.get("total_questions", 20),
            adaptation_type=test_data.get("adaptation_type", "hybrid"),
            learning_objectives=test_data.get("learning_objectives", ""),
            created_by=test_data.get("created_by", current_user.id)
        )
        
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        
        # Créer les questions si fournies
        if "questions" in test_data:
            for i, question_data in enumerate(test_data["questions"]):
                question = AdaptiveQuestion(
                    test_id=new_test.id,
                    question_text=question_data["question_text"],
                    question_type=question_data.get("question_type", "multiple_choice"),
                    difficulty_level=question_data["difficulty_level"],
                    learning_objective=question_data.get("learning_objective", ""),
                    options=json.dumps(question_data.get("options", [])),
                    correct_answer=question_data.get("correct_answer", ""),
                    explanation=question_data.get("explanation", ""),
                    question_order=i + 1
                )
                db.add(question)
            
            db.commit()
        
        return {
            "success": True,
            "message": "Test adaptatif créé avec succès",
            "test": {
                "id": new_test.id,
                "title": new_test.title,
                "subject": new_test.subject,
                "description": new_test.description,
                "difficulty_min": new_test.difficulty_min,
                "difficulty_max": new_test.difficulty_max,
                "estimated_duration": new_test.estimated_duration,
                "total_questions": new_test.total_questions,
                "adaptation_type": new_test.adaptation_type,
                "learning_objectives": new_test.learning_objectives,
                "is_active": new_test.is_active,
                "created_by": new_test.created_by,
                "created_at": new_test.created_at
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du test: {str(e)}"
        )

@router.get("/tests/", response_model=List[AdaptiveTestResponse])
async def get_all_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les tests adaptatifs actifs"""
    try:
        # Récupérer seulement les tests actifs
        tests = db.query(AdaptiveTest).filter(AdaptiveTest.is_active == True).all()
        
        # Convertir en réponse
        test_responses = []
        for test in tests:
            try:
                # Compter les questions actives
                question_count = db.query(AdaptiveQuestion).filter(
                    AdaptiveQuestion.test_id == test.id,
                    AdaptiveQuestion.is_active == True
                ).count()
                
                # Créer la réponse avec des valeurs par défaut sécurisées
                test_response = AdaptiveTestResponse(
                    id=test.id,
                    title=test.title or "Sans titre",
                    subject=test.subject or "Général",
                    description=test.description or "",
                    difficulty_min=test.difficulty_min if test.difficulty_min is not None else 1,
                    difficulty_max=test.difficulty_max if test.difficulty_max is not None else 10,
                    estimated_duration=test.estimated_duration if test.estimated_duration is not None else 30,
                    total_questions=question_count,
                    adaptation_type=test.adaptation_type or "difficulty",
                    learning_objectives=test.learning_objectives or "",
                    is_active=test.is_active if test.is_active is not None else True,
                    created_by=test.created_by,
                    created_at=test.created_at.isoformat() if test.created_at else datetime.now().isoformat(),
                    updated_at=test.updated_at.isoformat() if test.updated_at else datetime.now().isoformat()
                )
                test_responses.append(test_response)
                
                # Debug log
                logger.info(f"Test {test.id} traité: {test.title} - {question_count} questions")
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement du test {test.id}: {e}")
                continue
        
        logger.info(f"Total tests retournés: {len(test_responses)}")
        
        # Debug: Log de chaque réponse
        for i, response in enumerate(test_responses):
            logger.info(f"Réponse {i+1}: id={response.id}, title='{response.title}', questions={response.total_questions}")
        
        return test_responses
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tests actifs: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/tests/all/", response_model=List[AdaptiveTestResponse])
async def get_all_tests_including_inactive(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les tests adaptatifs (actifs et inactifs)"""
    try:
        # Récupérer tous les tests sans filtre sur is_active
        tests = db.query(AdaptiveTest).all()
        
        # Convertir en réponse
        test_responses = []
        for test in tests:
            try:
                # Compter les questions actives
                question_count = db.query(AdaptiveQuestion).filter(
                    AdaptiveQuestion.test_id == test.id,
                    AdaptiveQuestion.is_active == True
                ).count()
                
                # Créer la réponse avec des valeurs par défaut sécurisées
                test_response = AdaptiveTestResponse(
                    id=test.id,
                    title=test.title or "Sans titre",
                    subject=test.subject or "Général",
                    description=test.description or "",
                    difficulty_min=test.difficulty_min if test.difficulty_min is not None else 1,
                    difficulty_max=test.difficulty_max if test.difficulty_max is not None else 10,
                    estimated_duration=test.estimated_duration if test.estimated_duration is not None else 30,
                    total_questions=question_count,
                    adaptation_type=test.adaptation_type or "difficulty",
                    learning_objectives=test.learning_objectives or "",
                    is_active=test.is_active if test.is_active is not None else True,
                    created_by=test.created_by,
                    created_at=test.created_at.isoformat() if test.created_at else datetime.now().isoformat(),
                    updated_at=test.updated_at.isoformat() if test.updated_at else datetime.now().isoformat()
                )
                test_responses.append(test_response)
                
                # Debug log
                logger.info(f"Test {test.id} traité: {test.title} - {question_count} questions")
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement du test {test.id}: {e}")
                continue
        
        logger.info(f"Total tests retournés: {len(test_responses)}")
        
        # Debug: Log de chaque réponse
        for i, response in enumerate(test_responses):
            logger.info(f"Réponse {i+1}: id={response.id}, title='{response.title}', questions={response.total_questions}")
        
        return test_responses
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de tous les tests: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.patch("/tests/{test_id}/activate/")
async def activate_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activer un test adaptatif"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Récupérer le test
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier que le professeur est le créateur du test
        if test.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Vous ne pouvez modifier que vos propres tests")
        
        # Activer le test
        test.is_active = True
        test.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"message": f"Test '{test.title}' activé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'activation du test {test_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.patch("/tests/{test_id}/deactivate/")
async def deactivate_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Désactiver un test adaptatif"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Récupérer le test
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier que le professeur est le créateur du test
        if test.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Vous ne pouvez modifier que vos propres tests")
        
        # Désactiver le test
        test.is_active = False
        test.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"message": f"Test '{test.title}' désactivé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la désactivation du test {test_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/tests/{test_id}")
async def get_test_details(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'un test avec ses questions"""
    
    test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test non trouvé"
        )
    
    questions = db.query(AdaptiveQuestion).filter(
        AdaptiveQuestion.test_id == test_id
    ).order_by(AdaptiveQuestion.question_order).all()
    
    return {
        "success": True,
        "test": {
            "id": test.id,
            "title": test.title,
            "subject": test.subject,
            "description": test.description,
            "difficulty_min": test.difficulty_min,
            "difficulty_max": test.difficulty_max,
            "estimated_duration": test.estimated_duration,
            "total_questions": test.total_questions,
            "adaptation_type": test.adaptation_type,
            "learning_objectives": test.learning_objectives,
            "is_active": test.is_active,
            "created_by": test.created_by,
            "created_at": test.created_at,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "question_type": q.question_type,
                    "difficulty_level": q.difficulty_level,
                    "learning_objective": q.learning_objective,
                    "options": json.loads(q.options) if q.options else [],
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "order_index": q.question_order
                }
                for q in questions
            ]
        }
    }

# ============================================================================
# ENDPOINTS POUR LES ASSIGNATIONS
# ============================================================================

@router.post("/tests/{test_id}/assign")
async def assign_test(
    test_id: int,
    assignment_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assigner un test à des classes ou des étudiants"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les enseignants peuvent assigner des tests"
        )
    
    # Vérifier que le test existe
    test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test non trouvé"
        )
    
    # Vérifier que l'enseignant est le créateur du test
    if test.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez assigner que vos propres tests"
        )
    
    assignments = []
    
    try:
        # Assigner aux classes
        for class_id in assignment_data.get("class_ids", []):
            assignment = TestAssignment(
                test_id=test_id,
                assignment_type="class",
                target_id=class_id,
                assigned_by=current_user.id,
                due_date=datetime.fromisoformat(assignment_data["due_date"]) if assignment_data.get("due_date") else None
            )
            db.add(assignment)
            assignments.append(assignment)
        
        # Assigner aux étudiants individuels
        for student_id in assignment_data.get("student_ids", []):
            assignment = TestAssignment(
                test_id=test_id,
                assignment_type="student",
                target_id=student_id,
                assigned_by=current_user.id,
                due_date=datetime.fromisoformat(assignment_data["due_date"]) if assignment_data.get("due_date") else None
            )
            db.add(assignment)
            assignments.append(assignment)
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Test assigné avec succès à {len(assignments)} cibles",
            "assignments": [
                {
                    "id": a.id,
                    "test_id": a.test_id,
                    "assignment_type": a.assignment_type,
                    "target_id": a.target_id,
                    "assigned_by": a.assigned_by,
                    "assigned_at": a.assigned_at,
                    "due_date": a.due_date,
                    "status": a.status
                }
                for a in assignments
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'assignation: {str(e)}"
        )

# ============================================================================
# ENDPOINTS POUR LES ÉTUDIANTS
# ============================================================================

@router.get("/student/{student_id}/assigned")
async def get_student_adaptive_tests(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les tests adaptatifs assignés à un étudiant"""
    
    # Vérifier que l'utilisateur est l'étudiant ou un enseignant
    if current_user.id != student_id and current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Récupérer les assignations directes
    direct_assignments = db.query(TestAssignment).filter(
        TestAssignment.assignment_type == "student",
        TestAssignment.target_id == student_id,
        TestAssignment.status == "active"
    ).all()
    
    # Récupérer les assignations via les classes
    class_assignments = db.query(TestAssignment).join(
        AdaptiveClassStudent, TestAssignment.target_id == AdaptiveClassStudent.class_id
    ).filter(
        TestAssignment.assignment_type == "class",
        AdaptiveClassStudent.student_id == student_id,
        TestAssignment.status == "active"
    ).all()
    
    all_assignments = direct_assignments + class_assignments
    
    # Récupérer les détails des tests
    tests = []
    for assignment in all_assignments:
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == assignment.test_id).first()
        if test and test.is_active:
            # Vérifier s'il y a déjà une tentative
            attempt = db.query(TestAttempt).filter(
                TestAttempt.test_id == test.id,
                TestAttempt.student_id == student_id
            ).first()
            
            tests.append({
                "id": test.id,
                "title": test.title,
                "subject": test.subject,
                "description": test.description,
                "difficulty_min": test.difficulty_min,
                "difficulty_max": test.difficulty_max,
                "estimated_duration": test.estimated_duration,
                "total_questions": test.total_questions,
                "adaptation_type": test.adaptation_type,
                "assignment_id": assignment.id,
                "due_date": assignment.due_date,
                "status": attempt.status if attempt else "not_started",
                "progress": attempt.current_question_index if attempt else 0
            })
    
    return {
        "success": True,
        "tests": tests
    }

# ============================================================================
# ENDPOINTS POUR LES TENTATIVES DE TEST
# ============================================================================

@router.post("/tests/{test_id}/start")
async def start_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Commencer un test adaptatif"""
    
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent commencer des tests"
        )
    
    # Vérifier que le test est assigné à l'étudiant
    assignment = db.query(TestAssignment).filter(
        TestAssignment.test_id == test_id,
        TestAssignment.target_id == current_user.id,
        TestAssignment.status == "active"
    ).first()
    
    if not assignment:
        # Vérifier l'assignation via les classes
        assignment = db.query(TestAssignment).join(
            AdaptiveClassStudent, TestAssignment.target_id == AdaptiveClassStudent.class_id
        ).filter(
            TestAssignment.test_id == test_id,
            AdaptiveClassStudent.student_id == current_user.id,
            TestAssignment.status == "active"
        ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce test ne vous est pas assigné"
        )
    
    # Vérifier s'il y a déjà une tentative en cours
    existing_attempt = db.query(TestAttempt).filter(
        TestAttempt.test_id == test_id,
        TestAttempt.student_id == current_user.id,
        TestAttempt.status == "in_progress"
    ).first()
    
    if existing_attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous avez déjà une tentative en cours pour ce test"
        )
    
    # Créer une nouvelle tentative
    attempt = TestAttempt(
        test_id=test_id,
        student_id=current_user.id,
        assignment_id=assignment.id,
        status="in_progress",
        current_question_index=0
    )
    
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return {
        "success": True,
        "attempt_id": attempt.id,
        "message": "Test commencé avec succès"
    }

@router.post("/attempts/{attempt_id}/submit")
async def submit_test_attempt(
    attempt_id: int,
    responses: List[dict],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soumettre les réponses d'un test"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent soumettre des tests"
        )
    
    # Récupérer la tentative
    attempt = db.query(TestAttempt).filter(
        TestAttempt.id == attempt_id,
        TestAttempt.student_id == current_user.id
    ).first()
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tentative non trouvée"
        )
    
    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette tentative ne peut plus être modifiée"
        )
    
    try:
        total_score = 0
        max_score = 0
        
        # Traiter chaque réponse
        for response_data in responses:
            question = db.query(AdaptiveQuestion).filter(
                AdaptiveQuestion.id == response_data["question_id"]
            ).first()
            
            if question:
                is_correct = response_data["answer"] == question.correct_answer
                score = 1.0 if is_correct else 0.0
                total_score += score
                max_score += 1.0
                
                # Enregistrer la réponse
                response = QuestionResponse(
                    attempt_id=attempt_id,
                    question_id=question.id,
                    student_answer=response_data["answer"],
                    is_correct=is_correct,
                    score=score,
                    response_time=response_data.get("response_time", 0)
                )
                db.add(response)
        
        # Mettre à jour la tentative
        attempt.status = "completed"
        attempt.completed_at = datetime.now()
        attempt.total_score = total_score
        attempt.max_score = max_score
        
        db.commit()
        
        # TODO: Analyser les compétences avec l'IA
        # await analyze_competencies(attempt_id, db)
        
        return {
            "success": True,
            "message": "Test soumis avec succès",
            "score": total_score,
            "max_score": max_score,
            "percentage": (total_score / max_score * 100) if max_score > 0 else 0
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la soumission: {str(e)}"
        )

# ============================================================================
# ENDPOINTS POUR L'ANALYSE DES COMPÉTENCES
# ============================================================================

@router.get("/attempts/{attempt_id}/analysis")
async def get_competency_analysis(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer l'analyse des compétences d'une tentative"""
    
    # Vérifier que l'utilisateur a accès à cette tentative
    attempt = db.query(TestAttempt).filter(
        TestAttempt.id == attempt_id
    ).first()
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tentative non trouvée"
        )
    
    if current_user.id != attempt.student_id and current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Récupérer l'analyse des compétences
    competencies = db.query(CompetencyAnalysis).filter(
        CompetencyAnalysis.attempt_id == attempt_id
    ).all()
    
    return {
        "success": True,
        "attempt_id": attempt_id,
        "competencies": [
            {
                "name": c.competency_name,
                "level": c.competency_level,
                "confidence": c.confidence_score,
                "recommendations": c.ai_recommendations,
                "analyzed_at": c.analyzed_at
            }
            for c in competencies
        ]
    }

@router.get("/tests/simple/")
async def get_tests_simple(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les tests de manière simple"""
    try:
        # Requête SQL directe et simple
        result = db.execute(text("""
            SELECT 
                t.id,
                t.title,
                t.subject,
                t.description,
                t.difficulty_min,
                t.difficulty_max,
                t.estimated_duration,
                t.adaptation_type,
                t.learning_objectives,
                t.is_active,
                t.created_by,
                t.created_at,
                t.updated_at,
                COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id AND q.is_active = 1
            WHERE t.is_active = 1
            GROUP BY t.id
            ORDER BY t.id
        """))
        
        results = result.fetchall()
        
        # Convertir en dictionnaires simples
        tests = []
        for row in results:
            # Gérer les dates de manière sécurisée
            created_at = row[11]
            updated_at = row[12]
            
            # Convertir en string si c'est un datetime, sinon garder tel quel
            if hasattr(created_at, 'isoformat'):
                created_at_str = created_at.isoformat()
            else:
                created_at_str = str(created_at) if created_at else None
                
            if hasattr(updated_at, 'isoformat'):
                updated_at_str = updated_at.isoformat()
            else:
                updated_at_str = str(updated_at) if updated_at else None
            
            test = {
                "id": row[0],
                "title": row[1] or "Sans titre",
                "subject": row[2] or "Général",
                "description": row[3] or "",
                "difficulty_min": row[4] or 1,
                "difficulty_max": row[5] or 10,
                "estimated_duration": row[6] or 30,
                "adaptation_type": row[7] or "difficulty",
                "learning_objectives": row[8] or "",
                "is_active": bool(row[9]),
                "created_by": row[10],
                "created_at": created_at_str,
                "updated_at": updated_at_str,
                "total_questions": row[13] or 0
            }
            tests.append(test)
        
        logger.info(f"Endpoint simple: {len(tests)} tests retournés")
        return {"tests": tests, "count": len(tests)}
        
    except Exception as e:
        logger.error(f"Erreur endpoint simple: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/assignments")
async def get_student_assignments(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer tous les tests adaptatifs assignés à un étudiant (version test sans auth)"""
    try:
        print(f"🔥 [DEBUG] Récupération des assignations pour l'étudiant {student_id}")
        
        # Récupérer les assignations directes à l'étudiant
        student_assignments = db.query(TestAssignment).filter(
            TestAssignment.target_id == student_id,
            TestAssignment.assignment_type == 'student',
            TestAssignment.status == 'active'
        ).all()
        
        print(f"🔥 [DEBUG] Assignations directes trouvées: {len(student_assignments)}")
        
        # Récupérer les assignations via les classes (si l'étudiant est dans une classe)
        # TODO: Implémenter la logique des classes
        
        all_assignments = []
        
        for assignment in student_assignments:
            # Récupérer les détails du test
            test = db.query(AdaptiveTest).filter(AdaptiveTest.id == assignment.test_id).first()
            if test and test.is_active:
                assignment_data = {
                    "id": assignment.id,
                    "test_id": test.id,
                    "title": test.title,
                    "subject": test.subject,
                    "description": test.description,
                    "estimated_duration": test.estimated_duration,
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status,
                    "assigned_at": assignment.assigned_at.isoformat() if assignment.assigned_at else None,
                    "assigned_by": assignment.assigned_by
                }
                all_assignments.append(assignment_data)
                print(f"🔥 [DEBUG] Test assigné: {test.title} (ID: {test.id})")
        
        print(f"🔥 [DEBUG] Total des tests assignés: {len(all_assignments)}")
        return all_assignments
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des assignations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/teacher/{teacher_id}/results")
async def get_teacher_test_results(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer tous les résultats des tests adaptatifs créés par un professeur (version test sans auth)"""
    try:
        print(f"🔥 [DEBUG] Récupération des résultats pour le professeur {teacher_id}")
        
        # Récupérer tous les tests créés par le professeur
        teacher_tests = db.query(AdaptiveTest).filter(
            AdaptiveTest.created_by == teacher_id,
            AdaptiveTest.is_active == True
        ).all()
        
        print(f"🔥 [DEBUG] Tests du professeur trouvés: {len(teacher_tests)}")
        
        all_results = []
        
        for test in teacher_tests:
            # Récupérer toutes les tentatives pour ce test
            test_attempts = db.query(TestAttempt).filter(
                TestAttempt.test_id == test.id,
                TestAttempt.status == 'completed'
            ).all()
            
            print(f"🔥 [DEBUG] Test {test.title}: {len(test_attempts)} tentatives complétées")
            
            for attempt in test_attempts:
                # Récupérer les informations de l'étudiant
                student = db.query(User).filter(User.id == attempt.student_id).first()
                
                if student:
                    result_data = {
                        "id": attempt.id,
                        "test_id": test.id,
                        "test_title": test.title,
                        "test_subject": test.subject,
                        "student_id": student.id,
                        "student_name": student.username or f"Étudiant {student.id}",
                        "student_email": student.email,
                        "score": attempt.total_score,
                        "max_score": 100,
                        "percentage": attempt.total_score,
                        "status": attempt.status,
                        "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
                        "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
                        "quiz_type": "adaptive"
                    }
                    all_results.append(result_data)
        
        print(f"🔥 [DEBUG] Total des résultats: {len(all_results)}")
        return all_results
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des résultats: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/results")
async def get_student_adaptive_results(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les résultats des tests adaptatifs d'un étudiant"""
    try:
        logger.info(f"📊 Récupération des résultats adaptatifs pour étudiant {student_id}")
        
        # Récupérer tous les tests adaptatifs de l'étudiant
        test_attempts = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id
        ).all()
        
        results = []
        for attempt in test_attempts:
            # Récupérer les réponses aux questions
            responses = db.query(QuestionResponse).filter(
                QuestionResponse.attempt_id == attempt.id
            ).all()
            
            # Calculer le score
            correct_answers = sum(1 for r in responses if r.is_correct)
            total_questions = len(responses)
            score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            # Récupérer les détails du test
            test = db.query(AdaptiveTest).filter(AdaptiveTest.id == attempt.test_id).first()
            
            result = {
                "id": attempt.id,
                "test_id": attempt.test_id,
                "test_title": test.title if test else "Test adaptatif",
                "student_id": attempt.student_id,
                "started_at": attempt.started_at,
                "completed_at": attempt.completed_at,
                "status": "completed" if attempt.completed_at else "in_progress",
                "total_score": correct_answers,
                "max_score": total_questions,
                "score_percentage": round(score_percentage, 2),
                "points": int(score_percentage / 10),  # 10 points par 10% de réussite
                "type": "adaptive"
            }
            
            results.append(result)
        
        logger.info(f"✅ {len(results)} résultats adaptatifs récupérés pour étudiant {student_id}")
        return {"results": results}
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération résultats adaptatifs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des résultats: {str(e)}"
        )

@router.post("/tests/{test_id}/submit")
async def submit_test_directly(
    test_id: int,
    submission: QuizSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soumettre directement un test adaptatif sans passer par /start"""
    
    print(f"🔥 [DEBUG] Soumission reçue pour le test {test_id}")
    print(f"🔥 [DEBUG] Données reçues: {submission}")
    print(f"🔥 [DEBUG] Nombre de réponses: {len(submission.answers)}")
    print(f"🔥 [DEBUG] Structure des réponses: {submission.answers}")
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent soumettre des tests"
        )
    
    # Vérifier que le test existe
    test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test non trouvé"
        )
    
    # Vérifier l'assignation ou si l'étudiant a créé le test lui-même
    assignment = db.query(TestAssignment).filter(
        TestAssignment.test_id == test_id,
        TestAssignment.target_id == current_user.id,
        TestAssignment.status == "active"
    ).first()
    
    if not assignment:
        # Vérifier l'assignation via les classes
        assignment = db.query(TestAssignment).join(
            AdaptiveClassStudent, TestAssignment.target_id == AdaptiveClassStudent.class_id
        ).filter(
            TestAssignment.test_id == test_id,
            AdaptiveClassStudent.student_id == current_user.id,
            TestAssignment.status == "active"
        ).first()
    
    # Si pas d'assignation, vérifier si l'étudiant a créé le test lui-même
    if not assignment:
        # Vérifier si l'étudiant a créé ce test (cas des quiz créés depuis learning-path)
        test_creator = db.query(AdaptiveTest).filter(
            AdaptiveTest.id == test_id,
            AdaptiveTest.created_by == current_user.id
        ).first()
        
        if test_creator:
            print(f"🔥 [DEBUG] Test créé par l'étudiant {current_user.id}, assignation non requise")
            assignment = None  # Pas d'assignation nécessaire
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ce test ne vous est pas assigné et vous ne l'avez pas créé"
            )
    
    try:
        print(f"🔥 [DEBUG] Création de la tentative de test...")
        
        # Créer une tentative complétée directement
        attempt = TestAttempt(
            test_id=test_id,
            student_id=current_user.id,
            assignment_id=assignment.id if assignment else None,  # Peut être None si créé par l'étudiant
            status="completed",
            current_question_index=len(submission.answers),
            total_score=0,
            max_score=len(submission.answers)
        )
        
        print(f"🔥 [DEBUG] Tentative créée: {attempt}")
        db.add(attempt)
        print(f"🔥 [DEBUG] Tentative ajoutée à la session")
        
        db.commit()
        print(f"🔥 [DEBUG] Première transaction commitée")
        
        db.refresh(attempt)
        print(f"🔥 [DEBUG] Tentative rafraîchie, ID: {attempt.id}")
        
        total_score = 0
        
        # Traiter chaque réponse
        for i, response_data in enumerate(submission.answers):
            print(f"🔥 [DEBUG] Traitement de la réponse {i+1}: {response_data}")
            
            question = db.query(AdaptiveQuestion).filter(
                AdaptiveQuestion.id == response_data["question_id"]
            ).first()
            
            if question:
                is_correct = response_data["answer"] == question.correct_answer
                score = 1.0 if is_correct else 0.0
                total_score += score
                
                print(f"🔥 [DEBUG] Question {response_data['question_id']}: Correct={is_correct}, Score={score}")
                
                # Enregistrer la réponse
                response = QuestionResponse(
                    attempt_id=attempt.id,
                    question_id=response_data["question_id"],
                    student_answer=response_data["answer"],
                    is_correct=is_correct,
                    score=score,
                    answered_at=func.now()
                )
                db.add(response)
                print(f"🔥 [DEBUG] Réponse ajoutée à la session")
            else:
                print(f"❌ [DEBUG] Question {response_data['question_id']} non trouvée !")
        
        print(f"🔥 [DEBUG] Score total calculé: {total_score}")
        
        # Mettre à jour le score total
        attempt.total_score = total_score
        attempt.completed_at = func.now()
        
        print(f"🔥 [DEBUG] Tentative mise à jour, score: {attempt.total_score}")
        
        db.commit()
        print(f"🔥 [DEBUG] Deuxième transaction commitée avec succès")
        
        return {
            "success": True,
            "score": total_score,
            "max_score": len(submission.answers),
            "percentage": round((total_score / len(submission.answers)) * 100, 2),
            "quiz_type": "adaptive"
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la soumission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la soumission: {str(e)}"
        )

@router.get("/results/all")
async def get_all_test_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les résultats des tests adaptatifs (pour les professeurs)"""
    try:
        print(f"🔥 [DEBUG] Récupération de tous les résultats pour le professeur {current_user.id}")
        print(f"🔥 [DEBUG] Type du rôle: {type(current_user.role)}")
        print(f"🔥 [DEBUG] Valeur du rôle: {current_user.role}")
        print(f"🔥 [DEBUG] UserRole.teacher: {UserRole.teacher}")
        
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
        
        # Récupérer toutes les tentatives de test
        all_attempts = db.query(TestAttempt).filter(
            TestAttempt.status == 'completed'
        ).all()
        
        print(f"🔥 [DEBUG] Tentatives trouvées: {len(all_attempts)}")
        
        all_results = []
        
        for attempt in all_attempts:
            # Récupérer les informations du test
            test = db.query(AdaptiveTest).filter(AdaptiveTest.id == attempt.test_id).first()
            
            if test:
                # Récupérer le nom de l'étudiant (simulation pour l'instant)
                student_name = f"Étudiant {attempt.student_id}"
                
                result_data = {
                    "id": attempt.id,
                    "test_id": test.id,
                    "test_title": test.title,
                    "test_subject": test.subject,
                    "student_id": attempt.student_id,
                    "student_name": student_name,
                    "score": attempt.total_score,
                    "max_score": attempt.max_score,
                    "percentage": round((attempt.total_score / attempt.max_score) * 100, 2) if attempt.max_score > 0 else 0,
                    "status": attempt.status,
                    "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
                    "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
                    "quiz_type": "adaptive"
                }
                all_results.append(result_data)
        
        print(f"🔥 [DEBUG] Total des résultats: {len(all_results)}")
        return all_results
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de tous les résultats: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/tests/{test_id}/student/{student_id}/responses")
async def get_student_test_responses(
    test_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les réponses détaillées d'un étudiant pour un test spécifique"""
    try:
        print(f"🔥 [DEBUG] Récupération des réponses pour le test {test_id} et l'étudiant {student_id}")
        
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
        
        # Récupérer la tentative de l'étudiant
        attempt = db.query(TestAttempt).filter(
            TestAttempt.test_id == test_id,
            TestAttempt.student_id == student_id,
            TestAttempt.status == 'completed'
        ).first()
        
        if not attempt:
            raise HTTPException(status_code=404, detail="Tentative de test non trouvée")
        
        # Récupérer les réponses aux questions
        responses = db.query(QuestionResponse).filter(
            QuestionResponse.attempt_id == attempt.id
        ).all()
        
        print(f"🔥 [DEBUG] Réponses trouvées: {len(responses)}")
        if responses:
            print(f"🔥 [DEBUG] Première réponse: {responses[0]}")
            print(f"🔥 [DEBUG] Attributs disponibles: {dir(responses[0])}")
        
        detailed_responses = []
        
        for response in responses:
            # Récupérer les détails de la question
            question = db.query(AdaptiveQuestion).filter(
                AdaptiveQuestion.id == response.question_id
            ).first()
            
            if question:
                response_data = {
                    "question_id": question.id,
                    "question_text": question.question_text,
                    "student_answer": response.student_answer,
                    "correct_answer": question.correct_answer,
                    "is_correct": response.is_correct,
                    "points_earned": response.score,
                    "max_points": 1.0  # Chaque question vaut 1 point dans les tests adaptatifs
                }
                detailed_responses.append(response_data)
        
        print(f"🔥 [DEBUG] Réponses détaillées: {len(detailed_responses)}")
        return detailed_responses
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des réponses: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINT POUR GÉNÉRER UN QUIZ ADAPTATIF POUR UN ÉTUDIANT
# ============================================================================

@router.post("/generate-test/{student_id}")
async def generate_adaptive_test_for_student(
    student_id: int,
    quiz_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer un quiz adaptatif pour un étudiant spécifique"""
    try:
        print(f"🔥 [DEBUG] Génération de quiz adaptatif pour l'étudiant {student_id}")
        print(f"🔥 [DEBUG] Données reçues: {quiz_data}")
        
        # Vérifier que l'utilisateur est l'étudiant lui-même ou un professeur
        if current_user.id != student_id and current_user.role != UserRole.teacher:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Extraire les paramètres du quiz
        subject = quiz_data.get('subject', 'Français')
        difficulty_level = quiz_data.get('difficulty_level', 5)
        num_questions = quiz_data.get('num_questions', 10)
        
        # Créer un nouveau test adaptatif
        new_test = AdaptiveTest(
            title=f"Quiz {subject} - Niveau {difficulty_level}",
            subject=subject,
            description=f"Quiz adaptatif généré automatiquement pour {subject}",
            difficulty_min=max(1, difficulty_level - 2),
            difficulty_max=min(10, difficulty_level + 2),
            estimated_duration=num_questions * 2,  # 2 minutes par question
            total_questions=num_questions,
            adaptation_type="automatic",
            learning_objectives=f"Évaluer le niveau en {subject}",
            is_active=True,
            created_by=current_user.id
        )
        
        db.add(new_test)
        db.flush()  # Pour obtenir l'ID du test
        
        # Générer des vraies questions en français
        french_questions = [
            {
                "question": "Quel est le genre du mot 'table' en français ?",
                "options": ["Masculin", "Féminin", "Neutre", "Variable"],
                "correct": "Féminin",
                "explanation": "Le mot 'table' est un nom féminin en français. On dit 'une table'."
            },
            {
                "question": "Conjuguez le verbe 'être' à la première personne du singulier au présent :",
                "options": ["Je suis", "Je es", "Je être", "Je suis être"],
                "correct": "Je suis",
                "explanation": "Le verbe 'être' se conjugue 'je suis' au présent de l'indicatif."
            },
            {
                "question": "Quel est le pluriel de 'journal' ?",
                "options": ["Journaux", "Journals", "Journales", "Journauxs"],
                "correct": "Journaux",
                "explanation": "Les mots en '-al' font leur pluriel en '-aux' : journal → journaux."
            },
            {
                "question": "Complétez : 'Il faut que tu _____ à l'heure.'",
                "options": ["sois", "es", "seras", "soit"],
                "correct": "sois",
                "explanation": "Après 'il faut que', on utilise le subjonctif présent : 'que tu sois'."
            },
            {
                "question": "Quel est l'antonyme de 'grand' ?",
                "options": ["Petit", "Gros", "Large", "Haut"],
                "correct": "Petit",
                "explanation": "L'antonyme de 'grand' est 'petit'."
            },
            {
                "question": "Identifiez la fonction du mot 'rapidement' dans la phrase : 'Il court rapidement.'",
                "options": ["Sujet", "Verbe", "Adverbe", "Adjectif"],
                "correct": "Adverbe",
                "explanation": "'Rapidement' est un adverbe qui modifie le verbe 'court'."
            },
            {
                "question": "Quel temps verbal exprime une action passée et terminée ?",
                "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
                "correct": "Passé composé",
                "explanation": "Le passé composé exprime une action passée et terminée."
            },
            {
                "question": "Quel est le genre du mot 'livre' ?",
                "options": ["Masculin", "Féminin", "Neutre", "Variable"],
                "correct": "Masculin",
                "explanation": "Le mot 'livre' est un nom masculin. On dit 'un livre'."
            },
            {
                "question": "Complétez : 'Les enfants _____ dans le jardin.'",
                "options": ["jouent", "joue", "jouons", "jouez"],
                "correct": "jouent",
                "explanation": "Avec le sujet 'les enfants' (3e personne du pluriel), on utilise 'jouent'."
            },
            {
                "question": "Quel est le synonyme de 'beau' ?",
                "options": ["Joli", "Grand", "Bon", "Vieux"],
                "correct": "Joli",
                "explanation": "'Joli' est un synonyme de 'beau'."
            }
        ]
        
        # Créer les questions avec le contenu réel
        for i in range(min(num_questions, len(french_questions))):
            q_data = french_questions[i]
            print(f"🔥 [DEBUG] Création de la question {i+1}: {q_data['question'][:50]}...")
            
            question = AdaptiveQuestion(
                test_id=new_test.id,
                question_text=q_data["question"],
                question_type="multiple_choice",
                options=json.dumps(q_data["options"]),
                correct_answer=q_data["correct"],
                explanation=q_data["explanation"],
                difficulty_level=min(10, max(1, difficulty_level + (i % 3) - 1)),
                question_order=i+1
            )
            print(f"🔥 [DEBUG] Question créée: {question.question_text}")
            db.add(question)
        
        # Créer une tentative de test pour l'étudiant
        test_attempt = TestAttempt(
            test_id=new_test.id,
            student_id=student_id,
            started_at=datetime.now(),
            status='in_progress',
            current_question_index=0,
            total_score=0,
            max_score=num_questions
        )
        
        db.add(test_attempt)
        db.commit()
        
        print(f"🔥 [DEBUG] Quiz adaptatif créé avec succès: {new_test.id}")
        
        return {
            "success": True,
            "message": "Quiz adaptatif généré avec succès",
            "test_id": new_test.id,
            "title": new_test.title,
            "total_questions": num_questions,
            "estimated_duration": new_test.estimated_duration
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du quiz adaptatif: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

# ============================================================================
# ENDPOINT POUR RÉCUPÉRER LES DÉTAILS D'UNE TENTATIVE
# ============================================================================

@router.get("/attempts/{attempt_id}")
async def get_test_attempt_details(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'une tentative de test adaptatif"""
    try:
        logger.info(f"📊 Récupération des détails de la tentative {attempt_id}")
        
        # Récupérer la tentative
        attempt = db.query(TestAttempt).filter(TestAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tentative non trouvée"
            )
        
        # Vérifier que l'utilisateur a accès à cette tentative
        if current_user.role == UserRole.student and attempt.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé à cette tentative"
            )
        
        # Récupérer les réponses aux questions
        responses = db.query(QuestionResponse).filter(
            QuestionResponse.attempt_id == attempt_id
        ).all()
        
        # Calculer le score total
        total_score = sum(response.score for response in responses)
        max_score = len(responses) if responses else 0
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Récupérer les informations du test
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == attempt.test_id).first()
        
        result = {
            "id": attempt.id,
            "test_id": attempt.test_id,
            "student_id": attempt.student_id,
            "status": attempt.status,
            "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
            "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "current_question_index": attempt.current_question_index,
            "test_title": test.title if test else None,
            "test_subject": test.subject if test else None,
            "responses": [
                {
                    "question_id": response.question_id,
                    "student_answer": response.student_answer,
                    "is_correct": response.is_correct,
                    "score": response.score,
                    "answered_at": response.answered_at.isoformat() if response.answered_at else None
                }
                for response in responses
            ]
        }
        
        logger.info(f"✅ Détails de la tentative {attempt_id} récupérés avec succès")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des détails de la tentative {attempt_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des détails: {str(e)}"
        )

# ============================================================================
# ENDPOINTS POUR LES ASSIGNATIONS
# ============================================================================

@router.get("/assignments/")
async def get_adaptive_test_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer toutes les assignations de tests adaptatifs"""
    try:
        # Récupérer les assignations depuis test_assignments
        assignments = db.execute(text("""
            SELECT 
                ta.id,
                ta.test_id,
                ta.assignment_type,
                ta.target_id,
                ta.assigned_by,
                ta.assigned_at,
                ta.due_date,
                ta.is_active,
                t.title as test_title,
                t.subject as test_subject,
                u.username as student_name,
                u.email as student_email
            FROM test_assignments ta
            LEFT JOIN adaptive_tests t ON ta.test_id = t.id
            LEFT JOIN users u ON ta.target_id = u.id
            WHERE ta.is_active = 1
            ORDER BY ta.assigned_at DESC
        """)).fetchall()
        
        # Convertir en dictionnaires
        assignments_list = []
        for row in assignments:
            assignment = {
                "id": row[0],
                "test_id": row[1],
                "assignment_type": row[2],
                "target_id": row[3],
                "assigned_by": row[4],
                "assigned_at": row[5].isoformat() if row[5] else None,
                "due_date": row[6].isoformat() if row[6] else None,
                "is_active": bool(row[7]),
                "test_title": row[8] or "Test inconnu",
                "test_subject": row[9] or "Matière inconnue",
                "student_name": row[10] or f"Étudiant {row[3]}",
                "student_email": row[11] or f"etudiant{row[3]}@najah.ai"
            }
            assignments_list.append(assignment)
        
        logger.info(f"✅ {len(assignments_list)} assignations récupérées")
        return {
            "assignments": assignments_list,
            "count": len(assignments_list)
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des assignations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des assignations: {str(e)}"
        )

@router.get("/assignments/teacher/{teacher_id}")
async def get_teacher_assignments(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les assignations d'un professeur spécifique"""
    try:
        # Vérifier que l'utilisateur est le professeur ou un admin
        if current_user.id != teacher_id and current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé"
            )
        
        # Récupérer les assignations du professeur
        assignments = db.execute(text("""
            SELECT 
                ta.id,
                ta.test_id,
                ta.assignment_type,
                ta.target_id,
                ta.assigned_by,
                ta.assigned_at,
                ta.due_date,
                ta.is_active,
                t.title as test_title,
                t.subject as test_subject,
                u.username as student_name,
                u.email as student_email
            FROM test_assignments ta
            LEFT JOIN adaptive_tests t ON ta.test_id = t.id
            LEFT JOIN users u ON ta.target_id = u.id
            WHERE ta.assigned_by = :teacher_id AND ta.is_active = 1
            ORDER BY ta.assigned_at DESC
        """), {"teacher_id": teacher_id}).fetchall()
        
        # Convertir en dictionnaires
        assignments_list = []
        for row in assignments:
            assignment = {
                "id": row[0],
                "test_id": row[1],
                "assignment_type": row[2],
                "target_id": row[3],
                "assigned_by": row[4],
                "assigned_at": row[5].isoformat() if row[5] else None,
                "due_date": row[6].isoformat() if row[6] else None,
                "is_active": bool(row[7]),
                "test_title": row[8] or "Test inconnu",
                "test_subject": row[9] or "Matière inconnue",
                "student_name": row[10] or f"Étudiant {row[3]}",
                "student_email": row[11] or f"etudiant{row[3]}@najah.ai"
            }
            assignments_list.append(assignment)
        
        logger.info(f"✅ {len(assignments_list)} assignations récupérées pour le professeur {teacher_id}")
        return {
            "teacher_id": teacher_id,
            "assignments": assignments_list,
            "count": len(assignments_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des assignations du professeur {teacher_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des assignations: {str(e)}"
        )

@router.get("/teacher/{teacher_id}/results")
async def get_teacher_results(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les résultats des tests adaptatifs d'un professeur"""
    try:
        # Vérifier que l'utilisateur est le professeur ou un admin
        if current_user.id != teacher_id and current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé"
            )
        
        # Récupérer les résultats depuis quiz_results pour les tests adaptatifs
        logger.info(f"🔍 Recherche des résultats pour le professeur {teacher_id}")
        
        # D'abord, vérifier les tests adaptatifs du professeur
        teacher_tests = db.execute(text("""
            SELECT id, title, created_by FROM adaptive_tests WHERE created_by = :teacher_id
        """), {"teacher_id": teacher_id}).fetchall()
        logger.info(f"📋 Tests adaptatifs du professeur: {len(teacher_tests)}")
        
        # Ensuite, récupérer les résultats
        results = db.execute(text("""
            SELECT 
                qr.id,
                qr.user_id,
                qr.quiz_id,
                qr.score,
                qr.time_spent,
                qr.created_at,
                u.username as student_name,
                u.email as student_email,
                t.title as test_title,
                t.subject as test_subject,
                t.total_questions as max_score
            FROM quiz_results qr
            LEFT JOIN users u ON qr.user_id = u.id
            LEFT JOIN adaptive_tests t ON qr.quiz_id = t.id
            WHERE t.created_by = :teacher_id
            ORDER BY qr.created_at DESC
        """), {"teacher_id": teacher_id}).fetchall()
        
        logger.info(f"📊 Résultats trouvés: {len(results)}")
        
        # Convertir en dictionnaires
        results_list = []
        for row in results:
            percentage = round((row[3] / row[10]) * 100) if row[10] and row[10] > 0 else 0
            result = {
                "id": row[0],
                "test_id": row[2],
                "test_title": row[8] or "Test inconnu",
                "test_subject": row[9] or "Matière inconnue",
                "student_id": row[1],
                "student_name": row[6] or f"Étudiant {row[1]}",
                "student_email": row[7] or f"etudiant{row[1]}@najah.ai",
                "score": int(row[3]),
                "max_score": row[10] or 20,
                "percentage": percentage,
                "status": "completed",
                "started_at": row[5].isoformat() if row[5] else None,
                "completed_at": row[5].isoformat() if row[5] else None,
                "quiz_type": "Test Adaptatif"
            }
            results_list.append(result)
        
        logger.info(f"✅ {len(results_list)} résultats récupérés pour le professeur {teacher_id}")
        return results_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des résultats du professeur {teacher_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des résultats: {str(e)}"
        )
