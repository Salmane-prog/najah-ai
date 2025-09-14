from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.learning_path import LearningPath
from models.student_learning_path import StudentLearningPath
from models.user import User
from models.assessment import Assessment, AssessmentResult
from models.content import Content
from models.quiz import Quiz
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.post("/generate/{student_id}")
def generate_adaptive_learning_path(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Générer un parcours d'apprentissage adaptatif pour un étudiant."""
    
    # Vérifier que l'étudiant existe
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    # Récupérer l'évaluation initiale
    assessment = db.query(Assessment).filter(
        Assessment.student_id == student_id,
        Assessment.assessment_type == "initial"
    ).order_by(Assessment.completed_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Aucune évaluation initiale trouvée")
    
    # Récupérer le résultat d'évaluation
    result = db.query(AssessmentResult).filter(
        AssessmentResult.assessment_id == assessment.id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Résultat d'évaluation non trouvé")
    
    # Analyser les forces et faiblesses
    subject_scores = json.loads(result.subject_scores)
    
    # Déterminer le niveau global
    if result.percentage >= 80:
        global_level = "advanced"
    elif result.percentage >= 60:
        global_level = "intermediate"
    else:
        global_level = "beginner"
    
    # Créer le parcours adaptatif
    learning_path = LearningPath(
        title=f"Parcours personnalisé - {student.username}",
        description=f"Parcours adaptatif basé sur l'évaluation initiale",
        level=global_level,
        estimated_duration=30,  # jours
        created_by=current_user.id,
        is_adaptive=True
    )
    
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    
    # Assigner le parcours à l'étudiant
    student_path = StudentLearningPath(
        student_id=student_id,
        learning_path_id=learning_path.id,
        started_at=datetime.utcnow(),
        current_step=0,
        progress=0
    )
    
    db.add(student_path)
    db.commit()
    
    # Générer les étapes du parcours basées sur les difficultés
    steps = []
    
    # Ajouter des contenus de remédiation pour les sujets faibles
    for subject, scores in subject_scores.items():
        if scores["correct"] / scores["total"] < 0.7:  # Sujet faible
            # Trouver du contenu de remédiation
            remediation_content = db.query(Content).filter(
                Content.subject == subject,
                Content.level == "beginner"
            ).limit(2).all()
            
            for content in remediation_content:
                steps.append({
                    "type": "content",
                    "content_id": content.id,
                    "title": f"Remédiation - {content.title}",
                    "description": f"Renforcement en {subject}",
                    "estimated_time": 15
                })
    
    # Ajouter des quiz de consolidation
    consolidation_quizzes = db.query(Quiz).filter(
        Quiz.level == global_level,
        Quiz.is_active == True
    ).limit(3).all()
    
    for quiz in consolidation_quizzes:
        steps.append({
            "type": "quiz",
            "quiz_id": quiz.id,
            "title": f"Quiz de consolidation - {quiz.title}",
            "description": "Évaluation des acquis",
            "estimated_time": quiz.time_limit or 15
        })
    
    # Sauvegarder les étapes
    learning_path.steps = json.dumps(steps)
    db.commit()
    
    return {
        "learning_path": learning_path,
        "steps": steps,
        "analysis": {
            "global_level": global_level,
            "weak_subjects": [s for s, scores in subject_scores.items() if scores["correct"] / scores["total"] < 0.7],
            "strong_subjects": [s for s, scores in subject_scores.items() if scores["correct"] / scores["total"] >= 0.8]
        }
    }

@router.get("/")
def list_learning_paths(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Lister tous les parcours d'apprentissage."""
    try:
        learning_paths = db.query(LearningPath).all()
        
        result = []
        for path in learning_paths:
            # Récupérer les étudiants assignés
            try:
                student_assignments = db.query(StudentLearningPath).filter(
                    StudentLearningPath.learning_path_id == path.id
                ).all()
                
                students = []
                for assignment in student_assignments:
                    student = db.query(User).filter(User.id == assignment.student_id).first()
                    if student:
                        students.append({
                            "id": student.id,
                            "name": student.username or student.email
                        })
            except Exception:
                students = []
            
            result.append({
                "id": path.id,
                "name": path.title,
                "description": path.description,
                "objectives": path.objectives,
                "students": students
            })
        
        return result
        
    except Exception as e:
        print(f"Erreur dans list_learning_paths: {str(e)}")
        return []

@router.get("/student/{student_id}/current")
def get_student_current_path(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer le parcours actuel d'un étudiant."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer le parcours actuel
    student_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.is_active == True
    ).first()
    
    if not student_path:
        raise HTTPException(status_code=404, detail="Aucun parcours actif trouvé")
    
    # Récupérer les détails du parcours
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == student_path.learning_path_id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Parser les étapes
    steps = json.loads(learning_path.steps) if learning_path.steps else []
    
    # Enrichir les étapes avec les détails
    enriched_steps = []
    for i, step in enumerate(steps):
        enriched_step = {
            **step,
            "step_number": i + 1,
            "is_completed": i < student_path.current_step,
            "is_current": i == student_path.current_step
        }
        
        # Ajouter les détails selon le type
        if step["type"] == "content":
            content = db.query(Content).filter(Content.id == step["content_id"]).first()
            if content:
                enriched_step["content_details"] = {
                    "title": content.title,
                    "description": content.description,
                    "type": content.content_type
                }
        elif step["type"] == "quiz":
            quiz = db.query(Quiz).filter(Quiz.id == step["quiz_id"]).first()
            if quiz:
                enriched_step["quiz_details"] = {
                    "title": quiz.title,
                    "subject": quiz.subject,
                    "questions_count": len(quiz.questions) if quiz.questions else 0
                }
        
        enriched_steps.append(enriched_step)
    
    return {
        "learning_path": learning_path,
        "student_progress": student_path,
        "steps": enriched_steps,
        "progress_percentage": (student_path.current_step / len(steps) * 100) if steps else 0
    }

@router.post("/student/{student_id}/advance")
def advance_student_path(
    student_id: int,
    step_result: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Faire avancer un étudiant dans son parcours."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer le parcours actuel
    student_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.is_active == True
    ).first()
    
    if not student_path:
        raise HTTPException(status_code=404, detail="Aucun parcours actif trouvé")
    
    # Récupérer les détails du parcours
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == student_path.learning_path_id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Parser les étapes
    steps = json.loads(learning_path.steps) if learning_path.steps else []
    
    if student_path.current_step >= len(steps):
        raise HTTPException(status_code=400, detail="Parcours déjà terminé")
    
    # Mettre à jour la progression
    student_path.current_step += 1
    student_path.progress = (student_path.current_step / len(steps)) * 100
    
    # Si c'est un quiz, enregistrer le résultat
    current_step = steps[student_path.current_step - 1]
    if current_step["type"] == "quiz" and "score" in step_result:
        # Enregistrer le résultat du quiz
        from models.quiz import QuizResult
        quiz_result = QuizResult(
            student_id=student_id,
            quiz_id=current_step["quiz_id"],
            score=step_result["score"],
            max_score=step_result.get("max_score", 100),
            percentage=step_result["score"],
            is_completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(quiz_result)
    
    # Vérifier si le parcours est terminé
    if student_path.current_step >= len(steps):
        student_path.completed_at = datetime.utcnow()
        student_path.is_active = False
    
    db.commit()
    db.refresh(student_path)
    
    return {
        "message": "Progression mise à jour",
        "current_step": student_path.current_step,
        "progress_percentage": student_path.progress,
        "is_completed": student_path.current_step >= len(steps)
    }

@router.get("/recommendations/{student_id}")
def get_learning_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Obtenir des recommandations d'apprentissage personnalisées."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Analyser les performances récentes
    recent_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id,
        QuizResult.is_completed == True
    ).order_by(QuizResult.created_at.desc()).limit(10).all()
    
    if not recent_results:
        return {"recommendations": []}
    
    # Analyser les difficultés
    subject_performance = {}
    for result in recent_results:
        if result.sujet not in subject_performance:
            subject_performance[result.sujet] = []
        subject_performance[result.sujet].append(result.score)
    
    # Identifier les sujets faibles
    weak_subjects = []
    for subject, scores in subject_performance.items():
        avg_score = sum(scores) / len(scores)
        if avg_score < 70:  # Seuil de difficulté
            weak_subjects.append(subject)
    
    # Générer des recommandations
    recommendations = []
    
    # Recommandations de remédiation
    for subject in weak_subjects:
        remediation_content = db.query(Content).filter(
            Content.subject == subject,
            Content.level == "beginner"
        ).limit(2).all()
        
        for content in remediation_content:
            recommendations.append({
                "type": "remediation",
                "title": f"Remédiation en {subject}",
                "description": content.description,
                "content_id": content.id,
                "priority": "high"
            })
    
    # Recommandations de consolidation
    if len(recent_results) >= 3:
        avg_recent_score = sum(r.score for r in recent_results[:3]) / 3
        if avg_recent_score >= 80:
            # L'étudiant performe bien, proposer des défis
            advanced_quizzes = db.query(Quiz).filter(
                Quiz.level == "advanced",
                Quiz.is_active == True
            ).limit(2).all()
            
            for quiz in advanced_quizzes:
                recommendations.append({
                    "type": "challenge",
                    "title": f"Défi - {quiz.title}",
                    "description": "Quiz avancé pour tester vos limites",
                    "quiz_id": quiz.id,
                    "priority": "medium"
                })
    
    return {"recommendations": recommendations} 