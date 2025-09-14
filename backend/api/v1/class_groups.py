from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from models.class_group import ClassGroup, ClassStudent
from models.user import User, UserRole
from api.v1.auth import get_current_user, require_role
from schemas.class_group import ClassGroupCreate, ClassGroupRead, ClassStudentCreate, ClassStudentRead, ClassStudentWithUserRead
from typing import List
from datetime import datetime, timedelta

# Imports pour analytics
from models.quiz import QuizResult
from models.student_analytics import StudentProgress
from models.badge import UserBadge

router = APIRouter()

@router.get("/")
def list_class_groups(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Lister toutes les classes/groupes avec leurs statistiques."""
    try:
        classes = db.query(ClassGroup).all()
        result = []
        
        for class_group in classes:
            # Compter le nombre d'élèves dans cette classe
            student_count = db.query(ClassStudent).filter(
                ClassStudent.class_id == class_group.id
            ).count()
            
            # Calculer le niveau moyen (basé sur les scores des quiz)
            student_ids = [cs.student_id for cs in db.query(ClassStudent).filter(
                ClassStudent.class_id == class_group.id
            ).all()]
            
            average_score = 0
            if student_ids:
                try:
                    quiz_results = db.query(QuizResult).filter(
                        QuizResult.student_id.in_(student_ids),
                        QuizResult.is_completed == True,
                        QuizResult.score.isnot(None)
                    ).all()
                    
                    if quiz_results:
                        average_score = sum(r.score for r in quiz_results) / len(quiz_results)
                except Exception as e:
                    print(f"[WARNING] Erreur calcul score pour classe {class_group.id}: {e}")
                    average_score = 0
            
            # Déterminer le niveau basé sur le score moyen
            level = "Débutant"
            if average_score >= 80:
                level = "Avancé"
            elif average_score >= 60:
                level = "Intermédiaire"
            elif average_score >= 40:
                level = "Débutant"
            else:
                level = "Débutant"
            
            # Retourner le format attendu par le frontend
            class_data = {
                "id": class_group.id,
                "name": class_group.name,
                "description": class_group.description or "",
                "teacher_id": class_group.teacher_id,
                "created_at": class_group.created_at,
                "level": level,
                "student_count": student_count,
                "average_score": round(average_score, 1)
            }
            result.append(class_data)
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans list_class_groups: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des classes: {str(e)}"
        )

@router.get("/{class_id}", response_model=ClassGroupRead)
def get_class_group(class_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Obtenir une classe/groupe par ID (tous utilisateurs connectés)."""
    group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Class not found")
    return group

@router.post("/", response_model=ClassGroupRead, status_code=201)
def create_class_group(group: ClassGroupCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Créer une classe/groupe (enseignant ou admin uniquement)."""
    db_group = ClassGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.put("/{class_id}", response_model=ClassGroupRead)
def update_class_group(class_id: int, group: ClassGroupCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Mettre à jour une classe/groupe (enseignant ou admin uniquement)."""
    db_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Class not found")
    db_group.name = group.name
    db_group.description = group.description
    db_group.teacher_id = group.teacher_id
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/{class_id}", status_code=204)
def delete_class_group(class_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Supprimer une classe/groupe (enseignant ou admin uniquement)."""
    db_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(db_group)
    db.commit()
    return None

@router.post("/{class_id}/students/", response_model=ClassStudentRead, status_code=201)
def add_student_to_class(class_id: int, student: ClassStudentCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Associer un élève à une classe (enseignant ou admin uniquement)."""
    db_student = ClassStudent(class_id=class_id, student_id=student.student_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/{class_id}/students/{student_id}", status_code=204)
def remove_student_from_class(class_id: int, student_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Dissocier un élève d'une classe (enseignant ou admin uniquement)."""
    db_student = db.query(ClassStudent).filter(ClassStudent.class_id == class_id, ClassStudent.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found in class")
    db.delete(db_student)
    db.commit()
    return None

@router.get("/{class_id}/students/", response_model=List[ClassStudentWithUserRead])
def list_students_in_class(class_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Lister les élèves d'une classe (tous utilisateurs connectés)."""
    students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
    result = []
    for cs in students:
        user = db.query(User).filter(User.id == cs.student_id).first()
        if user:
            result.append(ClassStudentWithUserRead(
                id=cs.id,
                student_id=cs.student_id,
                username=user.username,
                email=user.email
            ))
    return result 

@router.get("/{class_id}/analytics")
def get_class_analytics(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les analytics détaillés d'une classe"""
    try:
        # Vérifier que la classe existe
        class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Obtenir les IDs des étudiants de cette classe
        class_students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()
        student_ids = [cs.student_id for cs in class_students]
        
        if not student_ids:
            # Données par défaut si pas d'étudiants
            return {
                "total_students": 0,
                "active_students": 0,
                "average_progress": 0,
                "average_score": 0,
                "total_quizzes": 0,
                "completed_quizzes": 0,
                "total_badges": 0,
                "recent_activity": 0,
                "top_performers": 0,
                "struggling_students": 0,
                "data_source": "real_database"
            }
        
        # Statistiques de base
        total_students = len(student_ids)
        
        # Étudiants actifs (quiz dans les 7 derniers jours)
        week_ago = datetime.utcnow() - timedelta(days=7)
        active_students = db.query(QuizResult.student_id).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.created_at >= week_ago
        ).distinct().count()
        
        # Progression moyenne
        progress_results = db.query(func.avg(StudentProgress.progress_percentage)).filter(
            StudentProgress.student_id.in_(student_ids)
        ).scalar()
        average_progress = round(progress_results or 0, 1)
        
        # Score moyen
        score_results = db.query(func.avg(QuizResult.score)).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.is_completed == True
        ).scalar()
        average_score = round(score_results or 0, 1)
        
        # Statistiques de quiz
        total_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids)
        ).count()
        completed_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.is_completed == True
        ).count()
        
        # Badges totaux
        total_badges = db.query(UserBadge).filter(
            UserBadge.user_id.in_(student_ids)
        ).count()
        
        # Activité récente (quiz complétés cette semaine)
        recent_activity = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.is_completed == True,
            QuizResult.created_at >= week_ago
        ).count()
        
        # Top performers (score > 80%)
        top_performers = db.query(QuizResult.student_id).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.is_completed == True,
            QuizResult.score >= 80
        ).distinct().count()
        
        # Étudiants en difficulté (score < 60%)
        struggling_students = db.query(QuizResult.student_id).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.is_completed == True,
            QuizResult.score < 60
        ).distinct().count()
        
        return {
            "total_students": total_students,
            "active_students": active_students,
            "average_progress": average_progress,
            "average_score": average_score,
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes,
            "total_badges": total_badges,
            "recent_activity": recent_activity,
            "top_performers": top_performers,
            "struggling_students": struggling_students,
            "data_source": "real_database"
        }
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_class_analytics: {e}")
        import traceback
        traceback.print_exc()
        # Retourner une erreur au lieu de données par défaut
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la récupération des analytics: {str(e)}"
        ) 