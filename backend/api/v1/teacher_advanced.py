from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.advanced_learning import (
    LearningPathStep, StudentProgress, ClassAnalytics, 
    StudentAnalytics, RealTimeActivity
)
from models.learning_path import LearningPath
from models.class_group import ClassGroup
from models.class_group import ClassStudent
from models.quiz import QuizResult, Quiz
from schemas.advanced_learning import (
    LearningPathStepCreate, LearningPathStepRead,
    StudentProgressCreate, StudentProgressRead,
    ClassAnalyticsCreate, ClassAnalyticsRead,
    StudentAnalyticsCreate, StudentAnalyticsRead,
    RealTimeActivityCreate, RealTimeActivityRead,
    TeacherDashboardData, LearningPathCreateAdvanced,
    LearningPathReadAdvanced, ClassGroupCreateAdvanced,
    ClassGroupReadAdvanced, RealTimeDashboard,
    StudentReport, ClassReport
)
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import asyncio
from collections import defaultdict

router = APIRouter()

# ============================================================================
# GESTION AVANCÉE DES CLASSES
# ============================================================================

@router.get("/classes/", response_model=List[ClassGroupReadAdvanced])
def get_teacher_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer toutes les classes d'un enseignant avec analytics"""
    classes = db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id,
        ClassGroup.is_active == True
    ).all()
    
    result = []
    for class_group in classes:
        # Compter les étudiants
        student_count = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id
        ).count()
        
        # Calculer la progression moyenne
        student_ids = [cs.student_id for cs in db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id
        ).all()]
        
        if student_ids:
            avg_progress = db.query(func.avg(StudentProgress.progress_percentage)).filter(
                StudentProgress.student_id.in_(student_ids)
            ).scalar() or 0.0
        else:
            avg_progress = 0.0
        
        result.append(ClassGroupReadAdvanced(
            **class_group.__dict__,
            student_count=student_count,
            average_progress=avg_progress
        ))
    
    return result

@router.post("/classes/", response_model=ClassGroupReadAdvanced)
def create_advanced_class(
    class_data: ClassGroupCreateAdvanced,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer une nouvelle classe avec paramètres avancés"""
    db_class = ClassGroup(
        name=class_data.name,
        description=class_data.description,
        teacher_id=current_user.id,
        level=class_data.level,
        subject=class_data.subject,
        max_students=class_data.max_students
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    
    return ClassGroupReadAdvanced(
        **db_class.__dict__,
        student_count=0,
        average_progress=0.0
    )

@router.put("/classes/{class_id}", response_model=ClassGroupReadAdvanced)
def update_advanced_class(
    class_id: int,
    class_data: ClassGroupCreateAdvanced,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Modifier une classe existante"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Mettre à jour les champs
    class_group.name = class_data.name
    class_group.description = class_data.description
    class_group.level = class_data.level
    class_group.subject = class_data.subject
    class_group.max_students = class_data.max_students
    
    db.commit()
    db.refresh(class_group)
    
    # Compter les étudiants
    student_count = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_group.id
    ).count()
    
    return ClassGroupReadAdvanced(
        **class_group.__dict__,
        student_count=student_count,
        average_progress=0.0
    )

@router.delete("/classes/{class_id}")
def delete_advanced_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer une classe (désactivation)"""
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Désactiver la classe au lieu de la supprimer
    class_group.is_active = False
    db.commit()
    
    return {"message": "Classe désactivée avec succès"}

@router.post("/classes/{class_id}/students/{student_id}")
def assign_student_to_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Assigner un étudiant à une classe"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id,
        ClassGroup.is_active == True
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Vérifier que l'étudiant existe
    student = db.query(User).filter(
        User.id == student_id,
        User.role == 'student'
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    # Vérifier la capacité de la classe
    current_students = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id
    ).count()
    
    if current_students >= class_group.max_students:
        raise HTTPException(status_code=400, detail="Classe pleine")
    
    # Vérifier si l'étudiant n'est pas déjà dans la classe
    existing_assignment = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id,
        ClassStudent.student_id == student_id
    ).first()
    
    if existing_assignment:
        raise HTTPException(status_code=400, detail="Étudiant déjà dans cette classe")
    
    # Créer l'assignation
    assignment = ClassStudent(
        class_id=class_id,
        student_id=student_id
    )
    db.add(assignment)
    db.commit()
    
    return {"message": "Étudiant assigné avec succès"}

@router.delete("/classes/{class_id}/students/{student_id}")
def remove_student_from_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Retirer un étudiant d'une classe"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Trouver l'assignation
    assignment = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id,
        ClassStudent.student_id == student_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé dans cette classe")
    
    db.delete(assignment)
    db.commit()
    
    return {"message": "Étudiant retiré avec succès"}

@router.get("/classes/{class_id}/students", response_model=List[Dict[str, Any]])
def get_class_students(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer tous les étudiants d'une classe avec leurs données"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Récupérer les étudiants avec leurs données
    students_data = db.query(ClassStudent, User).join(User).filter(
        ClassStudent.class_id == class_id
    ).all()
    
    result = []
    for assignment, student in students_data:
        # Récupérer la progression de l'étudiant
        progress = db.query(StudentProgress).filter(
            StudentProgress.student_id == student.id
        ).first()
        
        # Récupérer les résultats de quiz récents
        recent_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == student.id
        ).order_by(QuizResult.completed_at.desc()).limit(5).all()
        
        result.append({
            "student_id": student.id,
            "username": student.username,
            "email": student.email,
            "progress_percentage": progress.progress_percentage if progress else 0.0,
            "recent_quizzes": [
                {
                    "quiz_id": quiz.quiz_id,
                    "score": quiz.score,
                    "completed_at": quiz.completed_at
                } for quiz in recent_quizzes
            ],
            "last_activity": progress.last_activity if progress else None
        })
    
    return result

@router.get("/classes/{class_id}/analytics", response_model=ClassAnalyticsRead)
def get_class_analytics(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les analytics détaillés d'une classe"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Récupérer les étudiants de la classe
    students = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id
    ).all()
    
    student_ids = [s.student_id for s in students]
    
    # Calculer les analytics
    total_students = len(students)
    active_students = db.query(StudentProgress).filter(
        StudentProgress.student_id.in_(student_ids),
        StudentProgress.is_active == True,
        StudentProgress.last_activity >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    # Progression moyenne
    avg_progress = db.query(func.avg(StudentProgress.progress_percentage)).filter(
        StudentProgress.student_id.in_(student_ids)
    ).scalar() or 0.0
    
    # Quiz complétés
    completed_quizzes = db.query(QuizResult).filter(
        QuizResult.student_id.in_(student_ids),
        QuizResult.is_completed == True
    ).count()
    
    # Score moyen
    avg_score = db.query(func.avg(QuizResult.score)).filter(
        QuizResult.student_id.in_(student_ids),
        QuizResult.is_completed == True
    ).scalar() or 0.0
    
    # Sujets faibles/forts (basé sur les scores)
    subject_scores = db.query(QuizResult.sujet, func.avg(QuizResult.score)).filter(
        QuizResult.student_id.in_(student_ids),
        QuizResult.is_completed == True
    ).group_by(QuizResult.sujet).all()
    
    weak_subjects = [subject for subject, score in subject_scores if score < 60]
    strong_subjects = [subject for subject, score in subject_scores if score >= 80]
    
    analytics = ClassAnalytics(
        class_id=class_id,
        total_students=total_students,
        active_students=active_students,
        average_progress=avg_progress,
        completed_quizzes=completed_quizzes,
        average_score=avg_score,
        weak_subjects=weak_subjects,
        strong_subjects=strong_subjects
    )
    
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    
    return analytics

# ============================================================================
# GESTION AVANCÉE DES PARCOURS
# ============================================================================

@router.post("/learning-paths/", response_model=LearningPathReadAdvanced)
def create_advanced_learning_path(
    path_data: LearningPathCreateAdvanced,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer un parcours d'apprentissage avancé avec étapes"""
    # Créer le parcours
    learning_path = LearningPath(
        name=path_data.name,
        description=path_data.description,
        objectives=path_data.objectives,
        level=path_data.level,
        estimated_duration=path_data.estimated_duration,
        is_adaptive=path_data.is_adaptive,
        created_by=current_user.id
    )
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    
    # Créer les étapes
    steps = []
    for i, step_data in enumerate(path_data.steps):
        step = LearningPathStep(
            learning_path_id=learning_path.id,
            title=step_data.title,
            description=step_data.description,
            step_type=step_data.step_type,
            content_id=step_data.content_id,
            quiz_id=step_data.quiz_id,
            order=step_data.order,
            estimated_duration=step_data.estimated_duration,
            is_required=step_data.is_required,
            prerequisites=step_data.prerequisites
        )
        db.add(step)
        steps.append(step)
    
    db.commit()
    
    # Retourner le parcours avec les étapes
    return LearningPathReadAdvanced(
        **learning_path.__dict__,
        steps=[LearningPathStepRead(**step.__dict__) for step in steps]
    )

@router.get("/learning-paths/", response_model=List[LearningPathReadAdvanced])
def get_teacher_learning_paths(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer tous les parcours créés par l'enseignant"""
    paths = db.query(LearningPath).filter(
        LearningPath.created_by == current_user.id
    ).all()
    
    result = []
    for path in paths:
        steps = db.query(LearningPathStep).filter(
            LearningPathStep.learning_path_id == path.id
        ).order_by(LearningPathStep.order).all()
        
        result.append(LearningPathReadAdvanced(
            **path.__dict__,
            steps=[LearningPathStepRead(**step.__dict__) for step in steps]
        ))
    
    return result

@router.put("/learning-paths/{path_id}", response_model=LearningPathReadAdvanced)
def update_advanced_learning_path(
    path_id: int,
    path_data: LearningPathCreateAdvanced,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Modifier un parcours d'apprentissage existant"""
    # Vérifier que le parcours appartient à l'enseignant
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Mettre à jour les champs du parcours
    learning_path.name = path_data.name
    learning_path.description = path_data.description
    learning_path.objectives = path_data.objectives
    learning_path.level = path_data.level
    learning_path.estimated_duration = path_data.estimated_duration
    learning_path.is_adaptive = path_data.is_adaptive
    
    # Supprimer les anciennes étapes
    db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == path_id
    ).delete()
    
    # Créer les nouvelles étapes
    steps = []
    for i, step_data in enumerate(path_data.steps):
        step = LearningPathStep(
            learning_path_id=learning_path.id,
            title=step_data.title,
            description=step_data.description,
            step_type=step_data.step_type,
            content_id=step_data.content_id,
            quiz_id=step_data.quiz_id,
            order=step_data.order,
            estimated_duration=step_data.estimated_duration,
            is_required=step_data.is_required,
            prerequisites=step_data.prerequisites
        )
        db.add(step)
        steps.append(step)
    
    db.commit()
    
    return LearningPathReadAdvanced(
        **learning_path.__dict__,
        steps=[LearningPathStepRead(**step.__dict__) for step in steps]
    )

@router.delete("/learning-paths/{path_id}")
def delete_advanced_learning_path(
    path_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer un parcours d'apprentissage"""
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Supprimer les étapes associées
    db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == path_id
    ).delete()
    
    # Supprimer le parcours
    db.delete(learning_path)
    db.commit()
    
    return {"message": "Parcours supprimé avec succès"}

@router.put("/learning-paths/{path_id}/steps/reorder")
def reorder_learning_path_steps(
    path_id: int,
    step_orders: List[Dict[str, int]],  # [{"step_id": 1, "new_order": 2}, ...]
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Réordonner les étapes d'un parcours (drag & drop)"""
    # Vérifier que le parcours appartient à l'enseignant
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Mettre à jour l'ordre des étapes
    for order_data in step_orders:
        step = db.query(LearningPathStep).filter(
            LearningPathStep.id == order_data["step_id"],
            LearningPathStep.learning_path_id == path_id
        ).first()
        
        if step:
            step.order = order_data["new_order"]
    
    db.commit()
    
    return {"message": "Ordre des étapes mis à jour"}

@router.post("/learning-paths/{path_id}/steps/{step_id}/assign-quiz")
def assign_quiz_to_step(
    path_id: int,
    step_id: int,
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Assigner un quiz à une étape de parcours"""
    # Vérifier que le parcours appartient à l'enseignant
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Vérifier que l'étape existe
    step = db.query(LearningPathStep).filter(
        LearningPathStep.id == step_id,
        LearningPathStep.learning_path_id == path_id
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Étape non trouvée")
    
    # Vérifier que le quiz existe
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    
    # Assigner le quiz à l'étape
    step.quiz_id = quiz_id
    db.commit()
    
    return {"message": "Quiz assigné à l'étape avec succès"}

@router.delete("/learning-paths/{path_id}/steps/{step_id}/assign-quiz")
def remove_quiz_from_step(
    path_id: int,
    step_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Retirer un quiz d'une étape de parcours"""
    # Vérifier que le parcours appartient à l'enseignant
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Vérifier que l'étape existe
    step = db.query(LearningPathStep).filter(
        LearningPathStep.id == step_id,
        LearningPathStep.learning_path_id == path_id
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Étape non trouvée")
    
    # Retirer le quiz de l'étape
    step.quiz_id = None
    db.commit()
    
    return {"message": "Quiz retiré de l'étape avec succès"}

@router.get("/learning-paths/{path_id}/steps", response_model=List[LearningPathStepRead])
def get_learning_path_steps(
    path_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer toutes les étapes d'un parcours avec leurs détails"""
    # Vérifier que le parcours appartient à l'enseignant
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.created_by == current_user.id
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Parcours non trouvé")
    
    # Récupérer les étapes ordonnées
    steps = db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == path_id
    ).order_by(LearningPathStep.order).all()
    
    return [LearningPathStepRead(**step.__dict__) for step in steps]

# ============================================================================
# SUIVI TEMPS RÉEL
# ============================================================================

@router.get("/realtime/dashboard", response_model=RealTimeDashboard)
def get_realtime_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir le dashboard temps réel pour l'enseignant"""
    # Récupérer les classes de l'enseignant
    class_ids = [c.id for c in db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()]
    
    # Étudiants actifs (activité dans les dernières 24h)
    active_students = db.query(StudentProgress).filter(
        StudentProgress.is_active == True,
        StudentProgress.last_activity >= datetime.utcnow() - timedelta(hours=24)
    ).count()
    
    # Activités récentes (dernières 2 heures)
    recent_activities = db.query(RealTimeActivity).filter(
        RealTimeActivity.timestamp >= datetime.utcnow() - timedelta(hours=2)
    ).order_by(RealTimeActivity.timestamp.desc()).limit(20).all()
    
    # Performances des classes
    class_performances = []
    for class_id in class_ids:
        analytics = db.query(ClassAnalytics).filter(
            ClassAnalytics.class_id == class_id
        ).order_by(ClassAnalytics.date.desc()).first()
        
        if analytics:
            class_performances.append(analytics)
    
    # Alertes (étudiants en difficulté)
    alerts = []
    for class_id in class_ids:
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()
        
        for student in students:
            progress = db.query(StudentProgress).filter(
                StudentProgress.student_id == student.student_id
            ).first()
            
            if progress and progress.progress_percentage < 30:
                alerts.append({
                    "type": "warning",
                    "message": f"Étudiant en difficulté dans la classe {class_id}",
                    "student_id": student.student_id
                })
    
    return RealTimeDashboard(
        active_students=active_students,
        current_activities=recent_activities,
        class_performances=class_performances,
        alerts=alerts,
        notifications=[]
    )

# ============================================================================
# RAPPORTS AVANCÉS
# ============================================================================

@router.get("/reports/student/{student_id}", response_model=StudentReport)
def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Générer un rapport détaillé pour un étudiant"""
    # Vérifier que l'étudiant appartient à une classe de l'enseignant
    student_class = db.query(ClassStudent).join(ClassGroup).filter(
        ClassStudent.student_id == student_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not student_class:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    # Récupérer les données de l'étudiant
    student = db.query(User).filter(User.id == student_id).first()
    progress = db.query(StudentProgress).filter(
        StudentProgress.student_id == student_id
    ).first()
    
    # Résultats de quiz
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id
    ).all()
    
    total_quizzes = len(quiz_results)
    avg_score = sum(r.score for r in quiz_results) / total_quizzes if quiz_results else 0
    
    # Sujets faibles/forts
    subject_scores = defaultdict(list)
    for result in quiz_results:
        subject_scores[result.sujet].append(result.score)
    
    weak_subjects = [subject for subject, scores in subject_scores.items() 
                    if sum(scores) / len(scores) < 60]
    strong_subjects = [subject for subject, scores in subject_scores.items() 
                      if sum(scores) / len(scores) >= 80]
    
    # Recommandations basées sur les performances
    recommendations = []
    if avg_score < 60:
        recommendations.append("Travail de remédiation recommandé")
    if len(weak_subjects) > 0:
        recommendations.append(f"Focus sur les sujets: {', '.join(weak_subjects)}")
    if progress and progress.progress_percentage < 50:
        recommendations.append("Accélération du rythme d'apprentissage nécessaire")
    
    return StudentReport(
        student_id=student_id,
        student_name=student.username,
        class_name=student_class.class_group.name,
        progress_percentage=progress.progress_percentage if progress else 0,
        average_score=avg_score,
        total_quizzes=total_quizzes,
        time_spent=0,  # À implémenter avec tracking du temps
        weak_subjects=weak_subjects,
        strong_subjects=strong_subjects,
        recommendations=recommendations
    )

@router.get("/reports/class/{class_id}", response_model=ClassReport)
def get_class_report(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Générer un rapport détaillé pour une classe"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Récupérer les étudiants
    students = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id
    ).all()
    
    student_reports = []
    for student in students:
        report = get_student_report(student.student_id, db, current_user)
        student_reports.append(report)
    
    # Calculer les moyennes
    avg_progress = sum(r.progress_percentage for r in student_reports) / len(student_reports) if student_reports else 0
    avg_score = sum(r.average_score for r in student_reports) / len(student_reports) if student_reports else 0
    
    # Top performers et étudiants en difficulté
    top_performers = sorted(student_reports, key=lambda x: x.average_score, reverse=True)[:3]
    students_needing_help = [r for r in student_reports if r.average_score < 60]
    
    # Performance par sujet
    subject_performance = defaultdict(list)
    for report in student_reports:
        for subject in report.strong_subjects:
            subject_performance[subject].append(100)  # Score fort
        for subject in report.weak_subjects:
            subject_performance[subject].append(30)   # Score faible
    
    subject_avg = {subject: sum(scores) / len(scores) 
                  for subject, scores in subject_performance.items()}
    
    return ClassReport(
        class_id=class_id,
        class_name=class_group.name,
        teacher_name=current_user.username,
        total_students=len(students),
        average_progress=avg_progress,
        average_score=avg_score,
        top_performers=top_performers,
        students_needing_help=students_needing_help,
        subject_performance=subject_avg
    )

# ============================================================================
# NOTIFICATIONS ET ÉVÉNEMENTS IMPORTANTS
# ============================================================================

@router.get("/notifications/", response_model=List[Dict[str, Any]])
def get_teacher_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les notifications importantes pour l'enseignant"""
    notifications = []
    
    # Récupérer les classes de l'enseignant
    class_ids = [c.id for c in db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()]
    
    for class_id in class_ids:
        # Étudiants en difficulté (progression < 30%)
        struggling_students = db.query(StudentProgress).join(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            StudentProgress.progress_percentage < 30
        ).all()
        
        for progress in struggling_students:
            student = db.query(User).filter(User.id == progress.student_id).first()
            notifications.append({
                "type": "warning",
                "title": "Étudiant en difficulté",
                "message": f"{student.username} a une progression de {progress.progress_percentage}%",
                "student_id": progress.student_id,
                "class_id": class_id,
                "timestamp": datetime.utcnow()
            })
        
        # Quiz échoués récemment
        failed_quizzes = db.query(QuizResult).join(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            QuizResult.score < 60,
            QuizResult.completed_at >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        for quiz_result in failed_quizzes:
            student = db.query(User).filter(User.id == quiz_result.student_id).first()
            notifications.append({
                "type": "alert",
                "title": "Quiz échoué",
                "message": f"{student.username} a échoué un quiz avec {quiz_result.score}%",
                "student_id": quiz_result.student_id,
                "class_id": class_id,
                "quiz_id": quiz_result.quiz_id,
                "timestamp": quiz_result.completed_at
            })
    
    # Trier par timestamp (plus récent en premier)
    notifications.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return notifications[:20]  # Limiter à 20 notifications

@router.post("/notifications/mark-read/{notification_id}")
def mark_notification_as_read(
    notification_id: str,  # UUID ou identifiant de notification
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Marquer une notification comme lue"""
    # Ici on pourrait implémenter un système de marquage des notifications
    # Pour l'instant, on retourne juste un succès
    return {"message": "Notification marquée comme lue"}

# ============================================================================
# MONITORING AVANCÉ DES PERFORMANCES
# ============================================================================

@router.get("/performance/overview", response_model=Dict[str, Any])
def get_performance_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir un aperçu global des performances de toutes les classes"""
    # Récupérer toutes les classes de l'enseignant
    classes = db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id,
        ClassGroup.is_active == True
    ).all()
    
    total_students = 0
    total_progress = 0.0
    total_quizzes = 0
    total_score = 0.0
    active_students = 0
    
    class_performances = []
    
    for class_group in classes:
        # Compter les étudiants
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id
        ).all()
        
        student_ids = [s.student_id for s in students]
        class_student_count = len(students)
        total_students += class_student_count
        
        if student_ids:
            # Progression moyenne de la classe
            avg_progress = db.query(func.avg(StudentProgress.progress_percentage)).filter(
                StudentProgress.student_id.in_(student_ids)
            ).scalar() or 0.0
            
            # Quiz complétés
            quiz_count = db.query(QuizResult).filter(
                QuizResult.student_id.in_(student_ids),
                QuizResult.is_completed == True
            ).count()
            
            # Score moyen
            avg_score = db.query(func.avg(QuizResult.score)).filter(
                QuizResult.student_id.in_(student_ids),
                QuizResult.is_completed == True
            ).scalar() or 0.0
            
            # Étudiants actifs (activité dans les 7 derniers jours)
            active_count = db.query(StudentProgress).filter(
                StudentProgress.student_id.in_(student_ids),
                StudentProgress.last_activity >= datetime.utcnow() - timedelta(days=7)
            ).count()
            
            total_progress += avg_progress
            total_quizzes += quiz_count
            total_score += avg_score
            active_students += active_count
            
            class_performances.append({
                "class_id": class_group.id,
                "class_name": class_group.name,
                "student_count": class_student_count,
                "average_progress": avg_progress,
                "quiz_count": quiz_count,
                "average_score": avg_score,
                "active_students": active_count
            })
    
    # Calculer les moyennes globales
    class_count = len(classes)
    overall_progress = total_progress / class_count if class_count > 0 else 0.0
    overall_score = total_score / class_count if class_count > 0 else 0.0
    
    return {
        "total_classes": class_count,
        "total_students": total_students,
        "active_students": active_students,
        "overall_progress": overall_progress,
        "total_quizzes_completed": total_quizzes,
        "overall_average_score": overall_score,
        "class_performances": class_performances
    }

@router.get("/performance/trends/{class_id}", response_model=Dict[str, Any])
def get_class_performance_trends(
    class_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les tendances de performance d'une classe sur une période"""
    # Vérifier que la classe appartient à l'enseignant
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Récupérer les étudiants de la classe
    students = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id
    ).all()
    
    student_ids = [s.student_id for s in students]
    
    # Générer les dates pour la période
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    trends = {
        "dates": [],
        "progress": [],
        "quiz_scores": [],
        "active_students": []
    }
    
    current_date = start_date
    while current_date <= end_date:
        trends["dates"].append(current_date.strftime("%Y-%m-%d"))
        
        # Progression moyenne pour cette date
        avg_progress = db.query(func.avg(StudentProgress.progress_percentage)).filter(
            StudentProgress.student_id.in_(student_ids),
            func.date(StudentProgress.last_activity) == current_date.date()
        ).scalar() or 0.0
        
        trends["progress"].append(avg_progress)
        
        # Score moyen des quiz pour cette date
        avg_score = db.query(func.avg(QuizResult.score)).filter(
            QuizResult.student_id.in_(student_ids),
            func.date(QuizResult.completed_at) == current_date.date()
        ).scalar() or 0.0
        
        trends["quiz_scores"].append(avg_score)
        
        # Nombre d'étudiants actifs pour cette date
        active_count = db.query(StudentProgress).filter(
            StudentProgress.student_id.in_(student_ids),
            func.date(StudentProgress.last_activity) == current_date.date()
        ).count()
        
        trends["active_students"].append(active_count)
        
        current_date += timedelta(days=1)
    
    return trends

@router.get("/performance/alerts", response_model=List[Dict[str, Any]])
def get_performance_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les alertes de performance pour l'enseignant"""
    alerts = []
    
    # Récupérer les classes de l'enseignant
    class_ids = [c.id for c in db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()]
    
    for class_id in class_ids:
        # Étudiants avec progression très faible (< 20%)
        low_progress = db.query(StudentProgress).join(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            StudentProgress.progress_percentage < 20
        ).count()
        
        if low_progress > 0:
            alerts.append({
                "type": "critical",
                "title": "Progression très faible",
                "message": f"{low_progress} étudiant(s) avec progression < 20%",
                "class_id": class_id,
                "count": low_progress
            })
        
        # Étudiants inactifs (> 7 jours)
        inactive_students = db.query(StudentProgress).join(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            StudentProgress.last_activity < datetime.utcnow() - timedelta(days=7)
        ).count()
        
        if inactive_students > 0:
            alerts.append({
                "type": "warning",
                "title": "Étudiants inactifs",
                "message": f"{inactive_students} étudiant(s) inactif(s) depuis 7 jours",
                "class_id": class_id,
                "count": inactive_students
            })
        
        # Quiz échoués récemment
        failed_quizzes = db.query(QuizResult).join(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            QuizResult.score < 50,
            QuizResult.completed_at >= datetime.utcnow() - timedelta(days=3)
        ).count()
        
        if failed_quizzes > 0:
            alerts.append({
                "type": "alert",
                "title": "Quiz échoués",
                "message": f"{failed_quizzes} quiz échoué(s) récemment",
                "class_id": class_id,
                "count": failed_quizzes
            })
    
    return alerts

# ============================================================================
# WEBSOCKET POUR TEMPS RÉEL
# ============================================================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/teacher/{teacher_id}")
async def websocket_endpoint(websocket: WebSocket, teacher_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Envoyer les mises à jour temps réel
            await asyncio.sleep(5)  # Mise à jour toutes les 5 secondes
            
            # Ici on pourrait envoyer des données temps réel
            # comme les activités des étudiants, les alertes, etc.
            
    except WebSocketDisconnect:
        manager.disconnect(websocket) 