from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User, UserRole
from models.organization import Homework, LearningGoal
from models.class_group import ClassGroup, ClassStudent

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["Teacher Assignments"])

# =====================================================
# SCHÉMAS PYDANTIC
# =====================================================

class StudentInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    
    class Config:
        from_attributes = True

class HomeworkCreate(BaseModel):
    title: str
    description: str
    subject: str
    class_id: Optional[int] = None  # Optionnel maintenant
    student_ids: Optional[List[int]] = None  # Nouveau: liste d'étudiants spécifiques
    due_date: datetime
    priority: str = "medium"  # low, medium, high
    estimated_time: Optional[int] = None  # minutes

class HomeworkResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    class_id: Optional[int]
    assigned_by: int
    assigned_to: int  # ID de l'étudiant
    due_date: datetime
    status: str
    priority: str
    estimated_time: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningGoalCreate(BaseModel):
    title: str
    description: str
    subject: str
    class_id: Optional[int] = None  # Optionnel maintenant
    student_ids: Optional[List[int]] = None  # Nouveau: liste d'étudiants spécifiques
    target_date: datetime
    milestones: List[dict] = []

class LearningGoalResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    target_date: datetime
    progress: float
    status: str
    milestones: List[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# ENDPOINTS POUR RÉCUPÉRER LES ÉTUDIANTS
# =====================================================

@router.get("/students/{class_id}", response_model=List[StudentInfo])
def get_class_students(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les étudiants d'une classe"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Vérifier que la classe appartient au professeur
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classe non trouvée ou vous n'êtes pas autorisé"
        )
    
    # Récupérer les étudiants de la classe
    students = db.query(User).join(ClassStudent).filter(
        ClassStudent.class_id == class_id,
        User.role == UserRole.student
    ).all()
    
    return students

@router.get("/students", response_model=List[StudentInfo])
def get_all_teacher_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les étudiants du professeur (toutes classes confondues)"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Récupérer les classes du professeur
    teacher_classes = db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()
    
    class_ids = [c.id for c in teacher_classes]
    
    if not class_ids:
        return []
    
    # Récupérer tous les étudiants de ces classes
    students = db.query(User).join(ClassStudent).filter(
        ClassStudent.class_id.in_(class_ids),
        User.role == UserRole.student
    ).distinct().all()
    
    return students

# =====================================================
# ENDPOINTS POUR LES DEVOIRS
# =====================================================

@router.post("/homework", response_model=List[HomeworkResponse])
def create_homework(
    homework: HomeworkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer et assigner un devoir à une classe ou à des étudiants spécifiques"""
    
    # Vérifier que l'utilisateur est un professeur
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent créer des devoirs"
        )
    
    # Déterminer les étudiants cibles
    target_students = []
    
    if homework.student_ids:
        # Assignation individuelle
        for student_id in homework.student_ids:
            # Vérifier que l'étudiant appartient à une classe du professeur
            student_in_class = db.query(ClassStudent).join(ClassGroup).filter(
                ClassStudent.student_id == student_id,
                ClassGroup.teacher_id == current_user.id
            ).first()
            
            if not student_in_class:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Étudiant {student_id} non trouvé ou non autorisé"
                )
            target_students.append(student_in_class)
    
    elif homework.class_id:
        # Assignation par classe
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == homework.class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Classe non trouvée ou vous n'êtes pas autorisé"
            )
        
        target_students = db.query(ClassStudent).filter(
            ClassStudent.class_id == homework.class_id
        ).all()
        
        if not target_students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucun étudiant dans cette classe"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous devez spécifier soit une classe soit des étudiants"
        )
    
    # Créer le devoir pour chaque étudiant cible
    created_homeworks = []
    for student in target_students:
        new_homework = Homework(
            title=homework.title,
            description=homework.description,
            subject=homework.subject,
            class_id=student.class_id,
            assigned_by=current_user.id,
            assigned_to=student.student_id,
            due_date=homework.due_date,
            priority=homework.priority,
            estimated_time=homework.estimated_time,
            status="pending"
        )
        db.add(new_homework)
        created_homeworks.append(new_homework)
    
    db.commit()
    
    return created_homeworks

@router.get("/homework", response_model=List[HomeworkResponse])
def get_teacher_homework(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    class_id: Optional[int] = None,
    status_filter: Optional[str] = None
):
    """Récupérer tous les devoirs créés par le professeur"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    query = db.query(Homework).filter(Homework.assigned_by == current_user.id)
    
    if class_id:
        query = query.filter(Homework.class_id == class_id)
    
    if status_filter:
        query = query.filter(Homework.status == status_filter)
    
    homeworks = query.order_by(Homework.due_date.desc()).all()
    return homeworks

@router.get("/homework/{homework_id}", response_model=HomeworkResponse)
def get_homework_details(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'un devoir spécifique"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.assigned_by == current_user.id
    ).first()
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    return homework

@router.put("/homework/{homework_id}")
def update_homework(
    homework_id: int,
    homework_update: HomeworkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un devoir"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Trouver tous les devoirs avec le même titre et classe (pour tous les étudiants)
    homeworks = db.query(Homework).filter(
        Homework.title == homework_update.title,
        Homework.class_id == homework_update.class_id,
        Homework.assigned_by == current_user.id
    ).all()
    
    if not homeworks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    # Mettre à jour tous les devoirs correspondants
    for homework in homeworks:
        homework.description = homework_update.description
        homework.subject = homework_update.subject
        homework.due_date = homework_update.due_date
        homework.priority = homework_update.priority
        homework.estimated_time = homework_update.estimated_time
    
    db.commit()
    
    return {"message": "Devoir mis à jour avec succès"}

@router.delete("/homework/{homework_id}")
def delete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un devoir"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Trouver le devoir
    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.assigned_by == current_user.id
    ).first()
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    # Supprimer tous les devoirs avec le même titre et classe
    db.query(Homework).filter(
        Homework.title == homework.title,
        Homework.class_id == homework.class_id,
        Homework.assigned_by == current_user.id
    ).delete()
    
    db.commit()
    
    return {"message": "Devoir supprimé avec succès"}

# =====================================================
# ENDPOINTS POUR LES OBJECTIFS D'APPRENTISSAGE
# =====================================================

@router.post("/learning-goals", response_model=List[LearningGoalResponse])
def create_learning_goal(
    goal: LearningGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un objectif d'apprentissage pour une classe ou des étudiants spécifiques"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent créer des objectifs"
        )
    
    # Déterminer les étudiants cibles
    target_students = []
    
    if goal.student_ids:
        # Assignation individuelle
        for student_id in goal.student_ids:
            # Vérifier que l'étudiant appartient à une classe du professeur
            student_in_class = db.query(ClassStudent).join(ClassGroup).filter(
                ClassStudent.student_id == student_id,
                ClassGroup.teacher_id == current_user.id
            ).first()
            
            if not student_in_class:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Étudiant {student_id} non trouvé ou non autorisé"
                )
            target_students.append(student_in_class)
    
    elif goal.class_id:
        # Assignation par classe
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == goal.class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Classe non trouvée ou vous n'êtes pas autorisé"
            )
        
        target_students = db.query(ClassStudent).filter(
            ClassStudent.class_id == goal.class_id
        ).all()
        
        if not target_students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucun étudiant dans cette classe"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous devez spécifier soit une classe soit des étudiants"
        )
    
    # Créer l'objectif pour chaque étudiant cible
    created_goals = []
    for student in target_students:
        new_goal = LearningGoal(
            user_id=student.student_id,
            title=goal.title,
            description=goal.description,
            subject=goal.subject,
            target_date=goal.target_date,
            status="active",
            progress=0.0
        )
        db.add(new_goal)
        created_goals.append(new_goal)
    
    db.commit()
    
    return created_goals

@router.get("/learning-goals", response_model=List[LearningGoalResponse])
def get_teacher_learning_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    class_id: Optional[int] = None
):
    """Récupérer les objectifs créés par le professeur"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Récupérer les classes du professeur
    teacher_classes = db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()
    
    class_ids = [c.id for c in teacher_classes]
    
    if class_id and class_id not in class_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas autorisé à accéder à cette classe"
        )
    
    # Récupérer les étudiants des classes du professeur
    if class_id:
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()
    else:
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id.in_(class_ids)
        ).all()
    
    student_ids = [s.student_id for s in students]
    
    # Récupérer les objectifs de ces étudiants
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id.in_(student_ids)
    ).order_by(LearningGoal.target_date.desc()).all()
    
    return goals

# =====================================================
# ENDPOINTS POUR LES STATISTIQUES
# =====================================================

@router.get("/homework/stats")
def get_homework_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    class_id: Optional[int] = None
):
    """Récupérer les statistiques des devoirs"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    query = db.query(Homework).filter(Homework.assigned_by == current_user.id)
    
    if class_id:
        query = query.filter(Homework.class_id == class_id)
    
    homeworks = query.all()
    
    total_homework = len(homeworks)
    completed_homework = len([h for h in homeworks if h.status == "completed"])
    pending_homework = len([h for h in homeworks if h.status == "pending"])
    overdue_homework = len([h for h in homeworks if h.due_date < datetime.utcnow() and h.status != "completed"])
    
    completion_rate = (completed_homework / total_homework * 100) if total_homework > 0 else 0
    
    return {
        "total_homework": total_homework,
        "completed_homework": completed_homework,
        "pending_homework": pending_homework,
        "overdue_homework": overdue_homework,
        "completion_rate": round(completion_rate, 2)
    }

@router.get("/learning-goals/stats")
def get_learning_goals_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    class_id: Optional[int] = None
):
    """Récupérer les statistiques des objectifs d'apprentissage"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Récupérer les classes du professeur
    teacher_classes = db.query(ClassGroup).filter(
        ClassGroup.teacher_id == current_user.id
    ).all()
    
    class_ids = [c.id for c in teacher_classes]
    
    if class_id and class_id not in class_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas autorisé à accéder à cette classe"
        )
    
    # Récupérer les étudiants
    if class_id:
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()
    else:
        students = db.query(ClassStudent).filter(
            ClassStudent.class_id.in_(class_ids)
        ).all()
    
    student_ids = [s.student_id for s in students]
    
    # Récupérer les objectifs
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id.in_(student_ids)
    ).all()
    
    total_goals = len(goals)
    active_goals = len([g for g in goals if g.status == "active"])
    completed_goals = len([g for g in goals if g.status == "completed"])
    avg_progress = sum(g.progress for g in goals) / len(goals) if goals else 0
    
    return {
        "total_goals": total_goals,
        "active_goals": active_goals,
        "completed_goals": completed_goals,
        "average_progress": round(avg_progress * 100, 2)
    } 