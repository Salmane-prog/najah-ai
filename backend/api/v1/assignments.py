from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from core.database import get_db
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from models.assignment import Assignment
from api.v1.auth import get_current_user, require_role
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import String
from models.assignment_submission import AssignmentSubmission
from models.student_assignment import StudentAssignment
from pathlib import Path
import uuid
import shutil
from models.organization import LearningGoal

router = APIRouter()

# Schémas Pydantic
class AssignmentCreate(BaseModel):
    title: str
    description: str
    subject: str
    assignment_type: str  # "class" ou "student"
    target_ids: List[int]  # IDs des classes ou étudiants
    due_date: Optional[datetime] = None
    priority: str = "medium"  # "low", "medium", "high"
    estimated_time: Optional[int] = None  # en minutes
    attachment: Optional[dict] = None  # Métadonnées du fichier

class AssignmentRead(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    assignment_type: str
    target_ids: List[int]
    due_date: Optional[datetime]
    priority: str
    estimated_time: Optional[int]
    status: str
    created_at: datetime
    created_by: int
    teacher_name: str
    target_names: List[str]  # Noms des classes ou étudiants ciblés
    attachment: Optional[dict] = None  # Métadonnées du fichier
    submission: Optional[dict] = None  # Informations de soumission de l'étudiant

    class Config:
        from_attributes = True

class TeacherTargetsResponse(BaseModel):
    classes: List[dict]
    students: List[dict]
    total_students: int

@router.get("/teacher/targets", response_model=TeacherTargetsResponse)
def get_teacher_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les classes et étudiants disponibles pour l'enseignant"""
    
    # Classes de l'enseignant
    classes = db.query(ClassGroup).filter(ClassGroup.teacher_id == current_user.id).all()
    class_targets = []
    
    for class_group in classes:
        student_count = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id
        ).count()
        
        class_targets.append({
            "id": class_group.id,
            "name": class_group.name,
            "subject": class_group.subject or "Général",
            "student_count": student_count
        })
    
    # Étudiants individuels (tous les étudiants de l'enseignant)
    teacher_students = db.query(User).join(ClassStudent).join(ClassGroup).filter(
        and_(
            ClassGroup.teacher_id == current_user.id,
            User.role == UserRole.student
        )
    ).distinct().all()
    
    student_targets = [
        {
            "id": student.id,
            "name": f"{student.first_name or ''} {student.last_name or ''}".strip() or student.email,
            "email": student.email,
            "class_name": get_student_class_name(student.id, db)
        }
        for student in teacher_students
    ]
    
    total_students = len(student_targets)
    
    return TeacherTargetsResponse(
        classes=class_targets,
        students=student_targets,
        total_students=total_students
    )

def get_student_class_name(student_id: int, db: Session) -> str:
    """Récupérer le nom de la classe d'un étudiant"""
    class_student = db.query(ClassStudent).filter(ClassStudent.student_id == student_id).first()
    if class_student:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == class_student.class_id).first()
        if class_group:
            return class_group.name
    return "Classe inconnue"

@router.post("/", response_model=AssignmentRead)
def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer une nouvelle assignation"""
    
    # Vérifier que les cibles existent et appartiennent à l'enseignant
    if assignment_data.assignment_type == "class":
        for class_id in assignment_data.target_ids:
            class_group = db.query(ClassGroup).filter(
                and_(
                    ClassGroup.id == class_id,
                    ClassGroup.teacher_id == current_user.id
                )
            ).first()
            if not class_group:
                raise HTTPException(status_code=404, detail=f"Classe {class_id} non trouvée ou non autorisée")
    
    elif assignment_data.assignment_type == "student":
        for student_id in assignment_data.target_ids:
            # Vérifier que l'étudiant appartient à une classe de l'enseignant
            student_access = db.query(ClassStudent).join(ClassGroup).filter(
                and_(
                    ClassStudent.student_id == student_id,
                    ClassGroup.teacher_id == current_user.id
                )
            ).first()
            if not student_access:
                raise HTTPException(status_code=404, detail=f"Étudiant {student_id} non trouvé ou non autorisé")
    
    # Créer l'assignation dans la base de données
    db_assignment = Assignment(
        title=assignment_data.title,
        description=assignment_data.description,
        subject=assignment_data.subject,
        assignment_type=assignment_data.assignment_type,
        target_ids=assignment_data.target_ids,
        due_date=assignment_data.due_date,
        priority=assignment_data.priority,
        estimated_time=assignment_data.estimated_time,
        attachment=assignment_data.attachment,  # Ajouter le fichier
        created_by=current_user.id
    )
    
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    # Retourner la réponse avec les noms des cibles
    target_names = get_target_names(db_assignment.target_ids, db_assignment.assignment_type, db)
    teacher_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip() or current_user.email
    
    return AssignmentRead(
        id=db_assignment.id,
        title=db_assignment.title,
        description=db_assignment.description,
        subject=db_assignment.subject,
        assignment_type=db_assignment.assignment_type,
        target_ids=db_assignment.target_ids,
        due_date=db_assignment.due_date,
        priority=db_assignment.priority,
        estimated_time=db_assignment.estimated_time,
        status=db_assignment.status,
        created_at=db_assignment.created_at,
        created_by=db_assignment.created_by,
        teacher_name=teacher_name,
        target_names=target_names,
        attachment=db_assignment.attachment  # Ajouter le fichier
    )

def get_target_names(target_ids: List[int], assignment_type: str, db: Session) -> List[str]:
    """Récupérer les noms des cibles (classes ou étudiants)"""
    names = []
    
    if assignment_type == "class":
        for class_id in target_ids:
            class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
            if class_group:
                names.append(class_group.name)
    
    elif assignment_type == "student":
        for student_id in target_ids:
            student = db.query(User).filter(User.id == student_id).first()
            if student:
                name = f"{student.first_name or ''} {student.last_name or ''}".strip() or student.email
                names.append(name)
    
    return names

@router.get("/teacher/assignments", response_model=List[AssignmentRead])
def get_teacher_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer toutes les assignations d'un enseignant"""
    
    assignments = db.query(Assignment).filter(Assignment.created_by == current_user.id).all()
    
    result = []
    for assignment in assignments:
        target_names = get_target_names(assignment.target_ids, assignment.assignment_type, db)
        teacher_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip() or current_user.email
        
        result.append(AssignmentRead(
            id=assignment.id,
            title=assignment.title,
            description=assignment.description,
            subject=assignment.subject,
            assignment_type=assignment.assignment_type,
            target_ids=assignment.target_ids,
            due_date=assignment.due_date,
            priority=assignment.priority,
            estimated_time=assignment.estimated_time,
            status=assignment.status,
            created_at=assignment.created_at,
            created_by=assignment.created_by,
            teacher_name=teacher_name,
            target_names=target_names,
            attachment=assignment.attachment  # Ajouter le fichier
        ))
    
    return result

@router.put("/{assignment_id}", response_model=AssignmentRead)
def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Mettre à jour une assignation"""
    
    # Vérifier que l'assignation existe et appartient à l'enseignant
    assignment = db.query(Assignment).filter(
        and_(
            Assignment.id == assignment_id,
            Assignment.created_by == current_user.id
        )
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignation non trouvée ou non autorisée")
    
    # Vérifier que les nouvelles cibles existent et appartiennent à l'enseignant
    if assignment_data.assignment_type == "class":
        for class_id in assignment_data.target_ids:
            class_group = db.query(ClassGroup).filter(
                and_(
                    ClassGroup.id == class_id,
                    ClassGroup.teacher_id == current_user.id
                )
            ).first()
            if not class_group:
                raise HTTPException(status_code=404, detail=f"Classe {class_id} non trouvée ou non autorisée")
    
    elif assignment_data.assignment_type == "student":
        for student_id in assignment_data.target_ids:
            student_access = db.query(ClassStudent).join(ClassGroup).filter(
                and_(
                    ClassStudent.student_id == student_id,
                    ClassGroup.teacher_id == current_user.id
                )
            ).first()
            if not student_access:
                raise HTTPException(status_code=404, detail=f"Étudiant {student_id} non trouvé ou non autorisé")
    
    # Mettre à jour l'assignation
    assignment.title = assignment_data.title
    assignment.description = assignment_data.description
    assignment.subject = assignment_data.subject
    assignment.assignment_type = assignment_data.assignment_type
    assignment.target_ids = assignment_data.target_ids
    assignment.due_date = assignment_data.due_date
    assignment.priority = assignment_data.priority
    assignment.estimated_time = assignment_data.estimated_time
    assignment.attachment = assignment_data.attachment  # Ajouter le fichier
    
    db.commit()
    db.refresh(assignment)
    
    # Retourner la réponse mise à jour
    target_names = get_target_names(assignment.target_ids, assignment.assignment_type, db)
    teacher_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip() or current_user.email
    
    return AssignmentRead(
        id=assignment.id,
        title=assignment.title,
        description=assignment.description,
        subject=assignment.subject,
        assignment_type=assignment.assignment_type,
        target_ids=assignment.target_ids,
        due_date=assignment.due_date,
        priority=assignment.priority,
        estimated_time=assignment.estimated_time,
        status=assignment.status,
        created_at=assignment.created_at,
        created_by=assignment.created_by,
        teacher_name=teacher_name,
        target_names=target_names,
        attachment=assignment.attachment  # Ajouter le fichier
    )

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer une assignation"""
    
    # Vérifier que l'assignation existe et appartient à l'enseignant
    assignment = db.query(Assignment).filter(
        and_(
            Assignment.id == assignment_id,
            Assignment.created_by == current_user.id
        )
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignation non trouvée ou non autorisée")
    
    db.delete(assignment)
    db.commit()
    
    return {"message": "Assignation supprimée avec succès"}

@router.get("/student/{student_id}/assigned", response_model=List[AssignmentRead])
def get_student_assignments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les devoirs assignés à un étudiant spécifique"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres devoirs"
        )
    
    # Récupérer les devoirs assignés à l'étudiant
    assignments = db.query(Assignment).filter(
        and_(
            Assignment.assignment_type == "student",
            Assignment.target_ids.cast(String).contains(str(student_id))
        )
    ).all()
    
    # Récupérer aussi les devoirs assignés aux classes dont l'étudiant fait partie
    student_classes = db.query(ClassStudent.class_id).filter(
        ClassStudent.student_id == student_id
    ).all()
    
    class_ids = [sc.class_id for sc in student_classes]
    
    # Pour SQLite, utiliser une approche différente pour vérifier si un ID de classe est dans target_ids
    class_assignments = []
    for assignment in db.query(Assignment).filter(
        and_(
            Assignment.assignment_type == "class"
        )
    ).all():
        # Vérifier manuellement si l'un des IDs de classe de l'étudiant est dans target_ids
        if assignment.target_ids and any(class_id in assignment.target_ids for class_id in class_ids):
            class_assignments.append(assignment)
    
    # Combiner et dédupliquer les devoirs
    all_assignments = assignments + class_assignments
    unique_assignments = {a.id: a for a in all_assignments}.values()
    
    result = []
    for assignment in unique_assignments:
        # Récupérer le nom de l'enseignant
        teacher = db.query(User).filter(User.id == assignment.created_by).first()
        teacher_name = f"{teacher.first_name or ''} {teacher.last_name or ''}".strip() or teacher.email if teacher else "Enseignant inconnu"
        
        # Récupérer les noms des cibles
        target_names = get_target_names(assignment.target_ids, assignment.assignment_type, db)
        
        # Récupérer les informations de soumission de l'étudiant
        submission = db.query(AssignmentSubmission).filter(
            and_(
                AssignmentSubmission.assignment_id == assignment.id,
                AssignmentSubmission.student_id == student_id
            )
        ).first()
        
        submission_data = None
        if submission:
            submission_data = {
                "id": submission.id,
                "submitted_file": submission.submitted_file,
                "submitted_at": submission.submitted_at,
                "status": submission.status,
                "grade": submission.grade,
                "feedback": submission.feedback
            }
        
        result.append(AssignmentRead(
            id=assignment.id,
            title=assignment.title,
            description=assignment.description,
            subject=assignment.subject,
            assignment_type=assignment.assignment_type,
            target_ids=assignment.target_ids,
            due_date=assignment.due_date,
            priority=assignment.priority,
            estimated_time=assignment.estimated_time,
            status=assignment.status,
            created_at=assignment.created_at,
            created_by=assignment.created_by,
            teacher_name=teacher_name,
            target_names=target_names,
            attachment=assignment.attachment,  # Ajouter le fichier attaché
            submission=submission_data  # Ajouter les informations de soumission
        ))
    
    return result

@router.get("/student/{student_id}/learning-goals", response_model=List[dict])
def get_student_learning_goals(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les objectifs d'apprentissage d'un étudiant"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres objectifs"
        )
    
    # Pour l'instant, retourner une liste vide (à implémenter plus tard)
    return []

@router.get("/student/{student_id}/study-sessions", response_model=List[dict])
def get_student_study_sessions(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les sessions d'étude d'un étudiant"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres sessions d'étude"
        )
    
    # Pour l'instant, retourner une liste vide (à implémenter plus tard)
    return []

@router.get("/homework/assigned/{student_id}", response_model=List[AssignmentRead])
def get_homework_assigned_to_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Alias pour la compatibilité avec l'ancien endpoint homework"""
    return get_student_assignments(student_id, db, current_user)

# Endpoint pour l'upload de fichier avec un devoir
@router.post("/upload-file")
async def upload_assignment_file(
    assignment_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Upload un fichier pour un devoir existant"""
    from services.file_service import file_service
    
    # Vérifier que le devoir existe et appartient à l'enseignant
    assignment = db.query(Assignment).filter(
        and_(
            Assignment.id == assignment_id,
            Assignment.created_by == current_user.id
        )
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé ou vous n'êtes pas autorisé à le modifier"
        )
    
    # Sauvegarder le fichier
    file_metadata = await file_service.save_assignment_file(file, assignment_id)
    
    # Mettre à jour le devoir avec les métadonnées du fichier
    assignment.attachment = file_metadata
    db.commit()
    
    return {
        "message": "Fichier uploadé avec succès",
        "file_metadata": file_metadata
    }

@router.post("/student/{student_id}/submit/{assignment_id}")
async def submit_assignment(
    assignment_id: int,
    student_id: int,
    submission_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'admin']))
):
    """Soumettre un devoir terminé par un étudiant"""
    try:
        # Vérifier que l'étudiant est bien assigné à ce devoir
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Devoir non trouvé")
        
        # Vérifier que l'étudiant est bien ciblé par ce devoir
        if assignment.assignment_type == 'class':
            # Vérifier si l'étudiant est dans la classe
            class_student = db.query(ClassStudent).filter(
                ClassStudent.student_id == student_id,
                ClassStudent.class_id.in_(assignment.target_ids)
            ).first()
            if not class_student:
                raise HTTPException(status_code=403, detail="Vous n'êtes pas assigné à ce devoir")
        else:
            # Vérifier si l'étudiant est dans la liste des étudiants ciblés
            if student_id not in assignment.target_ids:
                raise HTTPException(status_code=403, detail="Vous n'êtes pas assigné à ce devoir")
        
        # Sauvegarder le fichier de soumission
        submission_filename = f"submission_{assignment_id}_{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{Path(submission_file.filename).suffix}"
        submission_path = Path("data/uploads/submissions")
        submission_path.mkdir(parents=True, exist_ok=True)
        
        file_path = submission_path / submission_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(submission_file.file, buffer)
        
        # Créer ou mettre à jour la soumission
        submission = db.query(AssignmentSubmission).filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student_id
        ).first()
        
        if submission:
            # Mettre à jour la soumission existante
            submission.submitted_file = str(file_path)
            submission.submitted_at = datetime.utcnow()
            submission.status = 'submitted'
        else:
            # Créer une nouvelle soumission
            submission = AssignmentSubmission(
                assignment_id=assignment_id,
                student_id=student_id,
                submitted_file=str(file_path),
                submitted_at=datetime.utcnow(),
                status='submitted'
            )
            db.add(submission)
        
        # Mettre à jour le statut du devoir pour cet étudiant
        student_assignment = db.query(StudentAssignment).filter(
            StudentAssignment.assignment_id == assignment_id,
            StudentAssignment.student_id == student_id
        ).first()
        
        if student_assignment:
            student_assignment.status = 'submitted'
            student_assignment.submitted_at = datetime.utcnow()
        else:
            # Créer un enregistrement de suivi
            student_assignment = StudentAssignment(
                assignment_id=assignment_id,
                student_id=student_id,
                status='submitted',
                submitted_at=datetime.utcnow()
            )
            db.add(student_assignment)
        
        db.commit()
        
        return {
            "message": "Devoir soumis avec succès",
            "submission_id": submission.id,
            "status": "submitted",
            "submitted_at": submission.submitted_at.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la soumission: {str(e)}")

@router.put("/student/{student_id}/status/{assignment_id}")
async def update_assignment_status(
    assignment_id: int,
    student_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'admin']))
):
    """Mettre à jour le statut d'un devoir pour un étudiant"""
    try:
        # Vérifier que l'étudiant est bien assigné à ce devoir
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Devoir non trouvé")
        
        # Vérifier que l'étudiant est bien ciblé par ce devoir
        if assignment.assignment_type == 'class':
            class_student = db.query(ClassStudent).filter(
                ClassStudent.student_id == student_id,
                ClassStudent.class_id.in_(assignment.target_ids)
            ).first()
            if not class_student:
                raise HTTPException(status_code=403, detail="Vous n'êtes pas assigné à ce devoir")
        else:
            if student_id not in assignment.target_ids:
                raise HTTPException(status_code=403, detail="Vous n'êtes pas assigné à ce devoir")
        
        # Mettre à jour ou créer le statut
        student_assignment = db.query(StudentAssignment).filter(
            StudentAssignment.assignment_id == assignment_id,
            StudentAssignment.student_id == student_id
        ).first()
        
        if student_assignment:
            student_assignment.status = status_update.get('status', 'in_progress')
            if status_update.get('status') == 'completed':
                student_assignment.completed_at = datetime.utcnow()
        else:
            student_assignment = StudentAssignment(
                assignment_id=assignment_id,
                student_id=student_id,
                status=status_update.get('status', 'in_progress')
            )
            if status_update.get('status') == 'completed':
                student_assignment.completed_at = datetime.utcnow()
            db.add(student_assignment)
        
        db.commit()
        
        return {
            "message": "Statut mis à jour avec succès",
            "status": student_assignment.status
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour du statut: {str(e)}")

# ENDPOINTS POUR LES OBJECTIFS D'APPRENTISSAGE (PROFESSEURS)
@router.post("/learning-goals", response_model=dict)
def create_learning_goal_for_students(
    goal_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un objectif d'apprentissage pour des étudiants (professeur)"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Seuls les professeurs peuvent créer des objectifs d'apprentissage")
        
        # Extraire les données
        title = goal_data.get("title")
        description = goal_data.get("description")
        subject = goal_data.get("subject")
        target_date = goal_data.get("target_date")
        student_ids = goal_data.get("student_ids", [])
        class_ids = goal_data.get("class_ids", [])
        
        if not title or not description or not subject:
            raise HTTPException(status_code=400, detail="Titre, description et matière sont requis")
        
        created_goals = []
        
        # Créer l'objectif pour chaque étudiant ciblé
        target_students = []
        
        # Si des classes sont spécifiées, récupérer tous les étudiants de ces classes
        if class_ids:
            for class_id in class_ids:
                class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
                target_students.extend([cs.student_id for cs in class_students])
        
        # Ajouter les étudiants spécifiques
        target_students.extend(student_ids)
        
        # Supprimer les doublons
        target_students = list(set(target_students))
        
        if not target_students:
            raise HTTPException(status_code=400, detail="Aucun étudiant ciblé")
        
        # Créer l'objectif pour chaque étudiant
        for student_id in target_students:
            # Vérifier que l'étudiant existe
            student = db.query(User).filter(User.id == student_id, User.role == "student").first()
            if not student:
                continue
            
            # Créer l'objectif
            new_goal = LearningGoal(
                title=title,
                description=description,
                subject=subject,
                target_date=datetime.fromisoformat(target_date) if target_date else None,
                progress=0.0,
                status="active",
                user_id=student_id,
                created_by=current_user.id  # Ajouter qui a créé l'objectif
            )
            
            db.add(new_goal)
            db.flush()  # Pour obtenir l'ID
            
            created_goals.append({
                "id": new_goal.id,
                "title": new_goal.title,
                "description": new_goal.description,
                "subject": new_goal.subject,
                "target_date": new_goal.target_date.isoformat() if new_goal.target_date else None,
                "progress": new_goal.progress,
                "status": new_goal.status,
                "student_id": student_id,
                "student_name": f"{student.first_name} {student.last_name}",
                "created_at": new_goal.created_at.isoformat()
            })
        
        db.commit()
        
        return {
            "message": f"{len(created_goals)} objectif(s) créé(s) avec succès",
            "goals": created_goals
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la création de l'objectif d'apprentissage: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/learning-goals", response_model=List[dict])
def get_learning_goals_for_teacher(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les objectifs d'apprentissage créés par le professeur"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Récupérer tous les objectifs créés par ce professeur
        goals = db.query(LearningGoal).filter(LearningGoal.created_by == current_user.id).all()
        
        # Enrichir avec les informations des étudiants
        enriched_goals = []
        for goal in goals:
            student = db.query(User).filter(User.id == goal.user_id).first()
            enriched_goals.append({
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "subject": goal.subject,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "progress": goal.progress,
                "status": goal.status,
                "student_id": goal.user_id,
                "student_name": f"{student.first_name} {student.last_name}" if student else "Étudiant inconnu",
                "student_email": student.email if student else "",
                "created_at": goal.created_at.isoformat()
            })
        
        return enriched_goals
        
    except Exception as e:
        print(f"Erreur lors de la récupération des objectifs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.put("/learning-goals/{goal_id}", response_model=dict)
def update_learning_goal_for_teacher(
    goal_id: int,
    goal_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modifier un objectif d'apprentissage (professeur)"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Vérifier que l'objectif existe et a été créé par ce professeur
        goal = db.query(LearningGoal).filter(
            LearningGoal.id == goal_id,
            LearningGoal.created_by == current_user.id
        ).first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Objectif non trouvé")
        
        # Mettre à jour les champs
        if "title" in goal_data:
            goal.title = goal_data["title"]
        if "description" in goal_data:
            goal.description = goal_data["description"]
        if "subject" in goal_data:
            goal.subject = goal_data["subject"]
        if "target_date" in goal_data:
            goal.target_date = datetime.fromisoformat(goal_data["target_date"]) if goal_data["target_date"] else None
        if "status" in goal_data:
            goal.status = goal_data["status"]
        
        db.commit()
        
        # Récupérer l'étudiant pour enrichir la réponse
        student = db.query(User).filter(User.id == goal.user_id).first()
        
        return {
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "subject": goal.subject,
            "target_date": goal.target_date.isoformat() if goal.target_date else None,
            "progress": goal.progress,
            "status": goal.status,
            "student_id": goal.user_id,
            "student_name": f"{student.first_name} {student.last_name}" if student else "Étudiant inconnu",
            "created_at": goal.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la modification de l'objectif: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification: {str(e)}")

@router.delete("/learning-goals/{goal_id}")
def delete_learning_goal_for_teacher(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un objectif d'apprentissage (professeur)"""
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Vérifier que l'objectif existe et a été créé par ce professeur
        goal = db.query(LearningGoal).filter(
            LearningGoal.id == goal_id,
            LearningGoal.created_by == current_user.id
        ).first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Objectif non trouvé")
        
        db.delete(goal)
        db.commit()
        
        return {"message": "Objectif supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la suppression de l'objectif: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")
