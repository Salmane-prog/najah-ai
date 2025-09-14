from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from core.database import get_db
from models.content_sharing import ContentSharing, ContentAccess
from models.content import Content
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from api.v1.auth import get_current_user, require_role
from schemas.content_sharing import (
    ContentSharingCreate, ContentSharingUpdate, ContentSharingRead,
    ContentAccessRead, ContentSharingStats, SharingTargetsResponse, SharingTarget
)
from typing import List, Optional
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.post("/", response_model=ContentSharingRead)
def share_content(
    sharing_data: ContentSharingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Partager un contenu avec des classes ou des étudiants"""
    
    # Vérifier que le contenu existe et appartient à l'enseignant
    content = db.query(Content).filter(Content.id == sharing_data.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    if content.created_by != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Vous ne pouvez partager que vos propres contenus")
    
    # Calculer le nombre d'étudiants cibles
    student_count = 0
    target_ids = sharing_data.target_ids or []
    
    if sharing_data.target_type == "class":
        # Compter les étudiants dans les classes sélectionnées
        for class_id in target_ids:
            class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).count()
            student_count += class_students
    elif sharing_data.target_type == "student":
        student_count = len(target_ids)
    elif sharing_data.target_type == "all_students":
        # Compter tous les étudiants de l'enseignant
        student_count = db.query(ClassStudent).join(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).distinct(ClassStudent.student_id).count()
    
    # Créer le partage
    sharing = ContentSharing(
        content_id=sharing_data.content_id,
        shared_by=current_user.id,
        target_type=sharing_data.target_type,
        target_ids=target_ids,
        allow_download=sharing_data.allow_download,
        allow_view=sharing_data.allow_view,
        expiration_date=sharing_data.expiration_date,
        notify_students=sharing_data.notify_students,
        custom_message=sharing_data.custom_message,
        student_count=student_count
    )
    
    db.add(sharing)
    db.commit()
    db.refresh(sharing)
    
    # Créer les accès pour chaque étudiant
    if sharing_data.target_type == "class":
        for class_id in target_ids:
            class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
            for class_student in class_students:
                access = ContentAccess(
                    content_id=sharing_data.content_id,
                    student_id=class_student.student_id,
                    sharing_id=sharing.id
                )
                db.add(access)
    
    elif sharing_data.target_type == "student":
        for student_id in target_ids:
            access = ContentAccess(
                content_id=sharing_data.content_id,
                student_id=student_id,
                sharing_id=sharing.id
            )
            db.add(access)
    
    elif sharing_data.target_type == "all_students":
        # Récupérer tous les étudiants de l'enseignant
        teacher_students = db.query(ClassStudent.student_id).join(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).distinct().all()
        
        for student in teacher_students:
            access = ContentAccess(
                content_id=sharing_data.content_id,
                student_id=student.student_id,
                sharing_id=sharing.id
            )
            db.add(access)
    
    db.commit()
    
    # Retourner le partage créé avec les informations complètes
    return get_sharing_with_details(sharing.id, db)

@router.get("/", response_model=List[ContentSharingRead])
def get_teacher_sharings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = Query(True)
):
    """Récupérer l'historique des partages d'un enseignant"""
    
    query = db.query(ContentSharing).filter(ContentSharing.shared_by == current_user.id)
    
    if active_only:
        query = query.filter(ContentSharing.is_active == True)
    
    sharings = query.order_by(ContentSharing.shared_at.desc()).offset(skip).limit(limit).all()
    
    # Enrichir avec les détails
    return [get_sharing_with_details(sharing.id, db) for sharing in sharings]

@router.get("/stats", response_model=ContentSharingStats)
def get_sharing_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les statistiques de partage d'un enseignant"""
    
    # Statistiques globales
    total_sharings = db.query(ContentSharing).filter(
        ContentSharing.shared_by == current_user.id
    ).count()
    
    active_sharings = db.query(ContentSharing).filter(
        and_(
            ContentSharing.shared_by == current_user.id,
            ContentSharing.is_active == True
        )
    ).count()
    
    # Statistiques des vues et téléchargements
    total_views = db.query(func.sum(ContentSharing.view_count)).filter(
        ContentSharing.shared_by == current_user.id
    ).scalar() or 0
    
    total_downloads = db.query(func.sum(ContentSharing.download_count)).filter(
        ContentSharing.shared_by == current_user.id
    ).scalar() or 0
    
    total_students_reached = db.query(func.sum(ContentSharing.student_count)).filter(
        ContentSharing.shared_by == current_user.id
    ).scalar() or 0
    
    # Statistiques de cette semaine
    week_ago = datetime.now() - timedelta(days=7)
    sharings_this_week = db.query(ContentSharing).filter(
        and_(
            ContentSharing.shared_by == current_user.id,
            ContentSharing.shared_at >= week_ago
        )
    ).count()
    
    # Statistiques de ce mois
    month_ago = datetime.now() - timedelta(days=30)
    sharings_this_month = db.query(ContentSharing).filter(
        and_(
            ContentSharing.shared_by == current_user.id,
            ContentSharing.shared_at >= month_ago
        )
    ).count()
    
    return ContentSharingStats(
        total_sharings=total_sharings,
        active_sharings=active_sharings,
        total_views=total_views,
        total_downloads=total_downloads,
        total_students_reached=total_students_reached,
        sharings_this_week=sharings_this_week,
        sharings_this_month=sharings_this_month,
        views_this_week=0,  # À implémenter avec ContentAccess
        downloads_this_week=0  # À implémenter avec ContentAccess
    )

@router.get("/targets", response_model=SharingTargetsResponse)
def get_sharing_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les classes et étudiants disponibles pour le partage"""
    
    # Classes de l'enseignant
    classes = db.query(ClassGroup).filter(ClassGroup.teacher_id == current_user.id).all()
    class_targets = []
    
    for class_group in classes:
        student_count = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id
        ).count()
        
        class_targets.append(SharingTarget(
            id=class_group.id,
            name=class_group.name,
            type="class",
            student_count=student_count
        ))
    
    # Étudiants individuels (tous les étudiants de l'enseignant)
    teacher_students = db.query(User).join(ClassStudent).join(ClassGroup).filter(
        and_(
            ClassGroup.teacher_id == current_user.id,
            User.role == UserRole.student
        )
    ).distinct().all()
    
    student_targets = [
        SharingTarget(
            id=student.id,
            name=f"{student.first_name or ''} {student.last_name or ''}".strip() or student.email,
            type="student"
        )
        for student in teacher_students
    ]
    
    # Nombre total d'étudiants
    all_students_count = len(student_targets)
    
    return SharingTargetsResponse(
        classes=class_targets,
        students=student_targets,
        all_students_count=all_students_count
    )

@router.get("/accesses/{sharing_id}", response_model=List[ContentAccessRead])
def get_sharing_accesses(
    sharing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les accès d'un partage spécifique"""
    
    # Vérifier que le partage appartient à l'enseignant
    sharing = db.query(ContentSharing).filter(
        and_(
            ContentSharing.id == sharing_id,
            ContentSharing.shared_by == current_user.id
        )
    ).first()
    
    if not sharing:
        raise HTTPException(status_code=404, detail="Partage non trouvé")
    
    # Récupérer les accès avec les détails des étudiants
    accesses = db.query(ContentAccess).filter(ContentAccess.sharing_id == sharing_id).all()
    
    # Enrichir avec les détails
    enriched_accesses = []
    for access in accesses:
        student = db.query(User).filter(User.id == access.student_id).first()
        content = db.query(Content).filter(Content.id == access.content_id).first()
        
        enriched_accesses.append(ContentAccessRead(
            id=access.id,
            content_id=access.content_id,
            student_id=access.student_id,
            sharing_id=access.sharing_id,
            first_accessed=access.first_accessed,
            last_accessed=access.last_accessed,
            access_count=access.access_count,
            can_view=access.can_view,
            can_download=access.can_download,
            student_name=f"{student.first_name or ''} {student.last_name or ''}".strip() or student.email if student else "Inconnu",
            student_email=student.email if student else "",
            content_title=content.title if content else "Contenu inconnu"
        ))
    
    return enriched_accesses

@router.put("/{sharing_id}", response_model=ContentSharingRead)
def update_sharing(
    sharing_id: int,
    sharing_update: ContentSharingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Mettre à jour un partage existant"""
    
    # Vérifier que le partage appartient à l'enseignant
    sharing = db.query(ContentSharing).filter(
        and_(
            ContentSharing.id == sharing_id,
            ContentSharing.shared_by == current_user.id
        )
    ).first()
    
    if not sharing:
        raise HTTPException(status_code=404, detail="Partage non trouvé")
    
    # Mettre à jour les champs
    for field, value in sharing_update.dict(exclude_unset=True).items():
        setattr(sharing, field, value)
    
    db.commit()
    db.refresh(sharing)
    
    return get_sharing_with_details(sharing.id, db)

@router.delete("/{sharing_id}")
def delete_sharing(
    sharing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Supprimer un partage (désactiver)"""
    
    # Vérifier que le partage appartient à l'enseignant
    sharing = db.query(ContentSharing).filter(
        and_(
            ContentSharing.id == sharing_id,
            ContentSharing.shared_by == current_user.id
        )
    ).first()
    
    if not sharing:
        raise HTTPException(status_code=404, detail="Partage non trouvé")
    
    # Désactiver le partage
    sharing.is_active = False
    db.commit()
    
    return {"message": "Partage supprimé avec succès"}

@router.get("/student/{student_id}/contents", response_model=List[ContentSharingRead])
def get_student_shared_contents(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les contenus partagés avec un étudiant"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant ou un enseignant/admin
    if current_user.id != student_id and current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer tous les accès de l'étudiant
    student_accesses = db.query(ContentAccess).filter(
        and_(
            ContentAccess.student_id == student_id,
            ContentAccess.can_view == True
        )
    ).all()
    
    # Récupérer les partages correspondants
    shared_contents = []
    for access in student_accesses:
        sharing = db.query(ContentSharing).filter(
            and_(
                ContentSharing.id == access.sharing_id,
                ContentSharing.is_active == True
            )
        ).first()
        
        if sharing:
            # Vérifier si le partage n'a pas expiré
            if sharing.expiration_date is None or sharing.expiration_date > datetime.now():
                shared_contents.append(get_sharing_with_details(sharing.id, db))
    
    return shared_contents

@router.get("/my-contents", response_model=List[ContentSharingRead])
def get_my_shared_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer tous les contenus partagés avec l'étudiant connecté"""
    
    # Récupérer tous les accès de l'étudiant connecté
    student_accesses = db.query(ContentAccess).filter(
        and_(
            ContentAccess.student_id == current_user.id,
            ContentAccess.can_view == True
        )
    ).all()
    
    # Récupérer les partages correspondants
    shared_contents = []
    for access in student_accesses:
        sharing = db.query(ContentSharing).filter(
            and_(
                ContentSharing.id == access.sharing_id,
                ContentSharing.is_active == True
            )
        ).first()
        
        if sharing:
            # Vérifier si le partage n'a pas expiré
            if sharing.expiration_date is None or sharing.expiration_date > datetime.now():
                shared_contents.append(get_sharing_with_details(sharing.id, db))
    
    return shared_contents

@router.post("/update-access")
def update_content_access(
    access_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour les statistiques d'accès d'un contenu partagé"""
    
    content_id = access_data.get("content_id")
    action = access_data.get("action")  # "view" ou "download"
    
    if not content_id or not action:
        raise HTTPException(status_code=400, detail="Données manquantes")
    
    # Vérifier que l'étudiant a accès à ce contenu
    access = db.query(ContentAccess).filter(
        and_(
            ContentAccess.content_id == content_id,
            ContentAccess.student_id == current_user.id
        )
    ).first()
    
    if not access:
        raise HTTPException(status_code=403, detail="Accès non autorisé à ce contenu")
    
    # Mettre à jour les statistiques
    if action == "view":
        access.last_accessed = datetime.now()
        access.access_count += 1
        if not access.first_accessed:
            access.first_accessed = datetime.now()
        
        # Mettre à jour le compteur de vues du partage
        sharing = db.query(ContentSharing).filter(ContentSharing.id == access.sharing_id).first()
        if sharing:
            sharing.view_count += 1
    
    elif action == "download":
        # Vérifier que le téléchargement est autorisé
        sharing = db.query(ContentSharing).filter(ContentSharing.id == access.sharing_id).first()
        if not sharing or not sharing.allow_download:
            raise HTTPException(status_code=403, detail="Téléchargement non autorisé pour ce contenu")
        
        access.last_accessed = datetime.now()
        access.access_count += 1
        if not access.first_accessed:
            access.first_accessed = datetime.now()
        
        # Mettre à jour le compteur de téléchargements du partage
        sharing.download_count += 1
    
    db.commit()
    
    return {"message": f"Accès {action} mis à jour avec succès"}

@router.get("/download/{content_id}")
def download_shared_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Télécharger un contenu partagé"""
    
    # Vérifier que l'étudiant a accès à ce contenu
    access = db.query(ContentAccess).filter(
        and_(
            ContentAccess.content_id == content_id,
            ContentAccess.student_id == current_user.id
        )
    ).first()
    
    if not access:
        raise HTTPException(status_code=403, detail="Accès non autorisé à ce contenu")
    
    # Vérifier que le téléchargement est autorisé
    sharing = db.query(ContentSharing).filter(ContentSharing.id == access.sharing_id).first()
    if not sharing or not sharing.allow_download:
        raise HTTPException(status_code=403, detail="Téléchargement non autorisé pour ce contenu")
    
    # Récupérer le contenu
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    # Mettre à jour les statistiques de téléchargement
    access.last_accessed = datetime.now()
    access.access_count += 1
    if not access.first_accessed:
        access.first_accessed = datetime.now()
    
    sharing.download_count += 1
    db.commit()
    
    # Retourner les informations du contenu pour le téléchargement
    return {
        "content_id": content.id,
        "title": content.title,
        "content_type": content.content_type,
        "file_url": content.file_url,
        "content_data": content.content_data
    }

# Fonction utilitaire pour enrichir un partage avec les détails
def get_sharing_with_details(sharing_id: int, db: Session) -> ContentSharingRead:
    """Enrichir un partage avec les détails du contenu et de l'enseignant"""
    
    sharing = db.query(ContentSharing).filter(ContentSharing.id == sharing_id).first()
    if not sharing:
        raise HTTPException(status_code=404, detail="Partage non trouvé")
    
    content = db.query(Content).filter(Content.id == sharing.content_id).first()
    teacher = db.query(User).filter(User.id == sharing.shared_by).first()
    
    return ContentSharingRead(
        id=sharing.id,
        content_id=sharing.content_id,
        shared_by=sharing.shared_by,
        shared_at=sharing.shared_at,
        is_active=sharing.is_active,
        target_type=sharing.target_type,
        target_ids=sharing.target_ids,
        allow_download=sharing.allow_download,
        allow_view=sharing.allow_view,
        expiration_date=sharing.expiration_date,
        notify_students=sharing.notify_students,
        custom_message=sharing.custom_message,
        view_count=sharing.view_count,
        download_count=sharing.download_count,
        student_count=sharing.student_count,
        content_title=content.title if content else "Contenu inconnu",
        content_subject=content.subject if content else "",
        content_type=content.content_type if content else "",
        teacher_name=f"{teacher.first_name or ''} {teacher.last_name or ''}".strip() or teacher.email if teacher else "Enseignant inconnu"
    )
