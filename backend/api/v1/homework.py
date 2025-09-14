from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from core.database import get_db
from core.security import get_current_user
from models.homework import AdvancedHomework, AdvancedHomeworkSubmission, AdvancedHomeworkAssignment
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(tags=["homework"])

# ============================================================================
# ENDPOINT DE TEST PUBLIC
# ============================================================================

@router.get("/test")
def test_homework_endpoint():
    """Endpoint de test public pour vérifier que l'API des devoirs fonctionne"""
    return {
        "message": "API Homework fonctionne correctement",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "endpoints_available": [
            "/api/v1/homework/",
            "/api/v1/homework/test"
        ]
    }

# Pydantic models
class HomeworkCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    class_id: Optional[int] = None
    due_date: datetime
    priority: str = "medium"
    estimated_time: Optional[int] = None
    max_score: float = 100.0
    instructions: Optional[str] = None
    attachments: Optional[List[str]] = None

class HomeworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    estimated_time: Optional[int] = None
    max_score: Optional[float] = None
    instructions: Optional[str] = None
    attachments: Optional[List[str]] = None

class HomeworkSubmissionCreate(BaseModel):
    content: Optional[str] = None
    attachments: Optional[List[str]] = None

class HomeworkSubmissionUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: Optional[str] = None

class HomeworkResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    subject: str
    class_id: Optional[int]
    due_date: datetime
    priority: str
    estimated_time: Optional[int]
    max_score: float
    instructions: Optional[str]
    attachments: Optional[List[str]]
    created_by: int
    created_at: datetime
    submissions_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class HomeworkSubmissionResponse(BaseModel):
    id: int
    homework_id: int
    student_id: int
    submitted_at: datetime
    content: Optional[str]
    attachments: Optional[List[str]]
    score: Optional[float]
    max_score: Optional[float]
    feedback: Optional[str]
    status: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=HomeworkResponse)
async def create_homework(
    homework: HomeworkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau devoir (professeur uniquement)"""
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent créer des devoirs"
        )
    
    # Vérifier si la classe existe si class_id est fourni
    if homework.class_id:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == homework.class_id).first()
        if not class_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Classe non trouvée"
            )
    
    db_homework = AdvancedHomework(
        title=homework.title,
        description=homework.description,
        subject=homework.subject,
        class_id=homework.class_id,
        created_by=current_user.id,
        due_date=homework.due_date,
        priority=homework.priority,
        estimated_time=homework.estimated_time,
        max_score=homework.max_score,
        instructions=homework.instructions,
        attachments=homework.attachments
    )
    
    db.add(db_homework)
    db.commit()
    db.refresh(db_homework)
    
    return HomeworkResponse(
        **db_homework.__dict__,
        submissions_count=0
    )

@router.get("/", response_model=List[HomeworkResponse])
async def get_homeworks(
    subject: Optional[str] = None,
    class_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les devoirs (filtrés par rôle)"""
    query = db.query(AdvancedHomework)
    
    if current_user.role == UserRole.student:
        # Étudiants : voir seulement les devoirs assignés à leur classe
        student_classes = db.query(ClassStudent.class_id).filter(
            ClassStudent.student_id == current_user.id
        ).subquery()
        
        query = query.filter(
            (AdvancedHomework.class_id.in_(student_classes)) |
            (AdvancedHomework.class_id.is_(None))  # Devoirs généraux
        )
    elif current_user.role == UserRole.teacher:
        # Professeurs : voir leurs propres devoirs
        query = query.filter(AdvancedHomework.created_by == current_user.id)
    
    if subject:
        query = query.filter(AdvancedHomework.subject == subject)
    if class_id:
        query = query.filter(AdvancedHomework.class_id == class_id)
    if status:
        if status == "active":
            query = query.filter(AdvancedHomework.is_active == True)
        elif status == "inactive":
            query = query.filter(AdvancedHomework.is_active == False)
    
    homeworks = query.all()
    
    # Ajouter le nombre de soumissions pour chaque devoir
    result = []
    for homework in homeworks:
        submissions_count = db.query(AdvancedHomeworkSubmission).filter(
            AdvancedHomeworkSubmission.homework_id == homework.id
        ).count()
        
        result.append(HomeworkResponse(
            **homework.__dict__,
            submissions_count=submissions_count
        ))
    
    return result

@router.get("/{homework_id}", response_model=HomeworkResponse)
async def get_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un devoir spécifique"""
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    # Vérifier les permissions
    if current_user.role == UserRole.student:
        # Vérifier si l'étudiant est dans la classe du devoir
        if homework.class_id:
            student_in_class = db.query(ClassStudent).filter(
                ClassStudent.student_id == current_user.id,
                ClassStudent.class_id == homework.class_id
            ).first()
            if not student_in_class:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accès refusé à ce devoir"
                )
    elif current_user.role == UserRole.teacher:
        if homework.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé à ce devoir"
            )
    
    submissions_count = db.query(AdvancedHomeworkSubmission).filter(
        AdvancedHomeworkSubmission.homework_id == homework.id
    ).count()
    
    return HomeworkResponse(
        **homework.__dict__,
        submissions_count=submissions_count
    )

@router.put("/{homework_id}", response_model=HomeworkResponse)
async def update_homework(
    homework_id: int,
    homework_update: HomeworkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un devoir (créateur uniquement)"""
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    if homework.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur peut modifier ce devoir"
        )
    
    for field, value in homework_update.dict(exclude_unset=True).items():
        setattr(homework, field, value)
    
    db.commit()
    db.refresh(homework)
    
    submissions_count = db.query(AdvancedHomeworkSubmission).filter(
        AdvancedHomeworkSubmission.homework_id == homework.id
    ).count()
    
    return HomeworkResponse(
        **homework.__dict__,
        submissions_count=submissions_count
    )

@router.delete("/{homework_id}")
async def delete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un devoir (créateur uniquement)"""
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    if homework.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur peut supprimer ce devoir"
        )
    
    db.delete(homework)
    db.commit()
    
    return {"message": "Devoir supprimé avec succès"}

@router.post("/{homework_id}/submit", response_model=HomeworkSubmissionResponse)
async def submit_homework(
    homework_id: int,
    submission: HomeworkSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soumettre un devoir (étudiant uniquement)"""
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent soumettre des devoirs"
        )
    
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    # Vérifier si l'étudiant peut soumettre ce devoir
    if homework.class_id:
        student_in_class = db.query(ClassStudent).filter(
            ClassStudent.student_id == current_user.id,
            ClassStudent.class_id == homework.class_id
        ).first()
        if not student_in_class:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé à ce devoir"
            )
    
    # Vérifier si l'étudiant a déjà soumis ce devoir
    existing_submission = db.query(AdvancedHomeworkSubmission).filter(
        AdvancedHomeworkSubmission.homework_id == homework_id,
        AdvancedHomeworkSubmission.student_id == current_user.id
    ).first()
    
    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous avez déjà soumis ce devoir"
        )
    
    # Vérifier si le devoir n'est pas en retard
    if datetime.now() > homework.due_date:
        status_submission = "late"
    else:
        status_submission = "submitted"
    
    db_submission = AdvancedHomeworkSubmission(
        homework_id=homework_id,
        student_id=current_user.id,
        content=submission.content,
        attachments=submission.attachments,
        max_score=homework.max_score,
        status=status_submission
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return HomeworkSubmissionResponse(**db_submission.__dict__)

@router.get("/{homework_id}/submissions", response_model=List[HomeworkSubmissionResponse])
async def get_homework_submissions(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les soumissions d'un devoir (créateur uniquement)"""
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == homework_id).first()
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    if homework.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur peut voir les soumissions"
        )
    
    submissions = db.query(AdvancedHomeworkSubmission).filter(
        AdvancedHomeworkSubmission.homework_id == homework_id
    ).all()
    
    return [HomeworkSubmissionResponse(**submission.__dict__) for submission in submissions]

@router.put("/submissions/{submission_id}/grade", response_model=HomeworkSubmissionResponse)
async def grade_submission(
    submission_id: int,
    grade_update: HomeworkSubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Noter une soumission (professeur uniquement)"""
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent noter les devoirs"
        )
    
    submission = db.query(AdvancedHomeworkSubmission).filter(AdvancedHomeworkSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soumission non trouvée"
        )
    
    # Vérifier si le professeur est le créateur du devoir
    homework = db.query(AdvancedHomework).filter(AdvancedHomework.id == submission.homework_id).first()
    if homework.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur du devoir peut le noter"
        )
    
    for field, value in grade_update.dict(exclude_unset=True).items():
        setattr(submission, field, value)
    
    submission.graded_by = current_user.id
    submission.graded_at = datetime.now()
    
    db.commit()
    db.refresh(submission)
    
    return HomeworkSubmissionResponse(**submission.__dict__)

@router.get("/student/{student_id}", response_model=List[HomeworkResponse])
async def get_student_homeworks(
    student_id: int,
    subject: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les devoirs d'un étudiant spécifique"""
    # Vérifier que l'utilisateur peut accéder à cet étudiant
    if current_user.id != student_id and current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Construire la requête de base
    query = db.query(AdvancedHomework)
    
    # Filtrer par étudiant (via les classes)
    if current_user.role == UserRole.student:
        # Pour les étudiants, récupérer les devoirs de leurs classes
        student_classes = db.query(ClassStudent.class_id).filter(
            ClassStudent.student_id == student_id
        ).subquery()
        
        query = query.filter(AdvancedHomework.class_id.in_(student_classes))
    else:
        # Pour les professeurs/admin, récupérer tous les devoirs
        pass
    
    # Appliquer les filtres optionnels
    if subject:
        query = query.filter(AdvancedHomework.subject == subject)
    
    if status:
        query = query.filter(AdvancedHomework.status == status)
    
    # Récupérer les devoirs
    homeworks = query.order_by(AdvancedHomework.due_date.desc()).all()
    
    # Ajouter le nombre de soumissions pour chaque devoir
    for homework in homeworks:
        submissions_count = db.query(AdvancedHomeworkSubmission).filter(
            AdvancedHomeworkSubmission.homework_id == homework.id
        ).count()
        homework.submissions_count = submissions_count
    
    return homeworks

# ============================================================================
# ENDPOINT MANQUANT - LISTE DES DEVOIRS
# ============================================================================

@router.get("/")
def get_advanced_homeworks(
    subject: str = None,
    class_id: int = None,
    limit: int = 20,
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer la liste des devoirs avancés (développement sans authentification)"""
    try:
        query = db.query(AdvancedHomework)
        
        # Filtrer par matière si spécifiée
        if subject:
            query = query.filter(AdvancedHomework.subject == subject)
        
        # Filtrer par classe si spécifiée
        if class_id:
            query = query.filter(AdvancedHomework.class_id == class_id)
        
        # Trier par date d'échéance et limiter les résultats
        homeworks = query.order_by(AdvancedHomework.due_date.asc()).limit(limit).all()
        
        return {
            "homeworks": homeworks,
            "total": len(homeworks),
            "filters": {
                "subject": subject,
                "class_id": class_id,
                "limit": limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des devoirs: {str(e)}")

# ============================================================================
# IMPORT NÉCESSAIRE
# ============================================================================

from models.class_group import ClassStudent
