from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from models.class_group import ClassGroup, ClassStudent
from models.user import User, UserRole
from api.v1.auth import get_current_user, require_role
from schemas.class_group import ClassGroupCreate, ClassGroupRead
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter()

@router.get("/")
def get_teacher_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer toutes les classes d'un enseignant"""
    try:
        classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
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
            
            # Récupérer la dernière activité
            last_activity = None
            if student_ids:
                # Chercher la dernière activité dans les quiz résultats
                from models.quiz import QuizResult
                last_quiz = db.query(QuizResult).filter(
                    QuizResult.student_id.in_(student_ids)
                ).order_by(QuizResult.completed_at.desc()).first()
                
                if last_quiz:
                    last_activity = last_quiz.completed_at.isoformat()
            
            class_data = {
                "id": class_group.id,
                "name": class_group.name,
                "description": class_group.description or "",
                "subject": getattr(class_group, 'subject', 'Non spécifié'),
                "level": getattr(class_group, 'level', 'Non spécifié'),
                "teacher_id": class_group.teacher_id,
                "created_at": class_group.created_at.isoformat() if class_group.created_at else None,
                "student_count": student_count,
                "last_activity": last_activity or "Aucune activité"
            }
            result.append(class_data)
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_teacher_classes: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des classes: {str(e)}"
        )

@router.post("/")
def create_teacher_class(
    class_data: ClassGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer une nouvelle classe pour l'enseignant"""
    try:
        db_class = ClassGroup(
            name=class_data.name,
            description=class_data.description,
            teacher_id=current_user.id,  # Toujours utiliser l'utilisateur connecté
            level=getattr(class_data, 'level', 'middle'),
            subject=getattr(class_data, 'subject', 'Général'),
            max_students=getattr(class_data, 'max_students', 30)
        )
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        
        return {
            "id": db_class.id,
            "name": db_class.name,
            "description": db_class.description,
            "subject": getattr(db_class, 'subject', 'Général'),
            "level": getattr(db_class, 'level', 'middle'),
            "teacher_id": db_class.teacher_id,
            "created_at": db_class.created_at.isoformat() if db_class.created_at else None,
            "student_count": 0,
            "last_activity": "Aucune activité"
        }
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erreur dans create_teacher_class: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création de la classe: {str(e)}"
        )

@router.put("/{class_id}")
def update_teacher_class(
    class_id: int,
    class_data: ClassGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Mettre à jour une classe de l'enseignant"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        db_class = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not db_class:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Mettre à jour les champs
        for field, value in class_data.dict(exclude_unset=True).items():
            setattr(db_class, field, value)
        
        db.commit()
        db.refresh(db_class)
        
        # Compter les étudiants
        student_count = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).count()
        
        return {
            "id": db_class.id,
            "name": db_class.name,
            "description": db_class.description,
            "subject": getattr(db_class, 'subject', 'Général'),
            "level": getattr(db_class, 'level', 'middle'),
            "teacher_id": db_class.teacher_id,
            "created_at": db_class.created_at.isoformat() if db_class.created_at else None,
            "student_count": student_count,
            "last_activity": "Aucune activité"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erreur dans update_teacher_class: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la mise à jour de la classe: {str(e)}"
        )

@router.delete("/{class_id}")
def delete_teacher_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer une classe de l'enseignant"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        db_class = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not db_class:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Supprimer d'abord les assignations d'étudiants
        db.query(ClassStudent).filter(ClassStudent.class_id == class_id).delete()
        
        # Supprimer la classe
        db.delete(db_class)
        db.commit()
        
        return {"message": "Classe supprimée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erreur dans delete_teacher_class: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression de la classe: {str(e)}"
        )

@router.get("/{class_id}/students")
def get_class_students(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer tous les étudiants d'une classe"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Récupérer les étudiants
        students_data = db.query(ClassStudent, User).join(User).filter(
            ClassStudent.class_id == class_id
        ).all()
        
        result = []
        for assignment, student in students_data:
            # Récupérer la progression de l'étudiant
            from models.student_analytics import StudentProgress
            progress = db.query(StudentProgress).filter(
                StudentProgress.student_id == student.id
            ).first()
            
            result.append({
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}" if hasattr(student, 'first_name') else student.username,
                "email": student.email,
                "username": student.username,
                "progress": progress.progress_percentage if progress else 0,
                "last_activity": progress.last_activity.isoformat() if progress and progress.last_activity else "Aucune activité"
            })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Erreur dans get_class_students: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des étudiants: {str(e)}"
        )

@router.post("/{class_id}/students/{student_id}")
def add_student_to_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Ajouter un étudiant à une classe"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Vérifier que l'étudiant existe et a le bon rôle
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Vérifier que l'étudiant n'est pas déjà dans cette classe
        existing_assignment = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            ClassStudent.student_id == student_id
        ).first()
        
        if existing_assignment:
            raise HTTPException(status_code=400, detail="L'étudiant est déjà dans cette classe")
        
        # Vérifier la capacité de la classe
        current_student_count = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).count()
        
        if current_student_count >= getattr(class_group, 'max_students', 30):
            raise HTTPException(status_code=400, detail="La classe a atteint sa capacité maximale")
        
        # Créer l'assignation
        new_assignment = ClassStudent(
            class_id=class_id,
            student_id=student_id
        )
        
        db.add(new_assignment)
        db.commit()
        
        return {"message": f"Étudiant {student.username} ajouté à la classe avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erreur dans add_student_to_class: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'ajout de l'étudiant: {str(e)}"
        )

@router.delete("/{class_id}/students/{student_id}")
def remove_student_from_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Retirer un étudiant d'une classe"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Vérifier que l'assignation existe
        assignment = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            ClassStudent.student_id == student_id
        ).first()
        
        if not assignment:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé dans cette classe")
        
        # Supprimer l'assignation
        db.delete(assignment)
        db.commit()
        
        return {"message": "Étudiant retiré de la classe avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erreur dans remove_student_from_class: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du retrait de l'étudiant: {str(e)}"
        )

@router.get("/students/all")
def get_all_teacher_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer tous les étudiants de toutes les classes d'un professeur"""
    try:
        # Récupérer toutes les classes du professeur
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        if not teacher_classes:
            return []
        
        # Récupérer tous les étudiants de toutes ces classes
        all_students = set()  # Pour éviter les doublons
        result = []
        
        for class_group in teacher_classes:
            students_data = db.query(ClassStudent, User).join(User).filter(
                ClassStudent.class_id == class_group.id
            ).all()
            
            for assignment, student in students_data:
                if student.id not in all_students:
                    all_students.add(student.id)
                    
                    result.append({
                        "id": student.id,
                        "first_name": student.first_name or "",
                        "last_name": student.last_name or "",
                        "email": student.email,
                        "username": student.username,
                        "role": "student",
                        "progress": 0,  # Valeur par défaut
                        "last_activity": "Aucune activité"  # Valeur par défaut
                    })
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_all_teacher_students: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des étudiants: {str(e)}"
        )
