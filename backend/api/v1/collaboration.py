from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from core.database import get_db
from core.security import get_current_user
from models.collaboration import (
    StudyGroup, StudyGroupMember, GroupMessage, GroupResource,
    CollaborationProject, ProjectMember, ProjectTask
)
from models.user import User, UserRole
from pydantic import BaseModel

router = APIRouter(tags=["collaboration"])

# Pydantic models
class StudyGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    subject: Optional[str] = None
    max_members: int = 10
    is_public: bool = True

class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    max_members: Optional[int] = None
    is_public: Optional[bool] = None

class GroupMessageCreate(BaseModel):
    content: str
    message_type: str = "text"
    attachments: Optional[List[str]] = None

class GroupResourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    resource_type: str
    file_url: Optional[str] = None
    file_size: Optional[int] = None

class CollaborationProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[datetime] = None

class ProjectTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None

class StudyGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    subject: Optional[str]
    max_members: int
    is_public: bool
    created_by: int
    created_at: datetime
    members_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class GroupMessageResponse(BaseModel):
    id: int
    group_id: int
    user_id: int
    content: str
    message_type: str
    attachments: Optional[List[str]]
    created_at: datetime
    user_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class GroupResourceResponse(BaseModel):
    id: int
    group_id: int
    title: str
    description: Optional[str]
    resource_type: str
    file_url: Optional[str]
    file_size: Optional[int]
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CollaborationProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    subject: Optional[str]
    status: str
    due_date: Optional[datetime]
    created_by: int
    created_at: datetime
    members_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ProjectTaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    assigned_to: Optional[int]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Study Groups
@router.post("/study-groups", response_model=StudyGroupResponse)
async def create_study_group(
    group: StudyGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un groupe d'étude"""
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent créer des groupes d'étude"
        )
    
    db_group = StudyGroup(
        name=group.name,
        description=group.description,
        subject=group.subject,
        max_members=group.max_members,
        is_public=group.is_public,
        created_by=current_user.id
    )
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    # Ajouter le créateur comme membre
    member = StudyGroupMember(
        group_id=db_group.id,
        user_id=current_user.id,
        role="admin"
    )
    db.add(member)
    db.commit()
    
    return StudyGroupResponse(
        **db_group.__dict__,
        members_count=1
    )

@router.get("/study-groups", response_model=List[StudyGroupResponse])
async def get_study_groups(
    subject: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les groupes d'étude"""
    query = db.query(StudyGroup)
    
    if current_user.role == UserRole.student:
        # Étudiants : voir les groupes publics et leurs groupes
        user_groups = db.query(StudyGroupMember.group_id).filter(
            StudyGroupMember.user_id == current_user.id
        ).subquery()
        
        query = query.filter(
            (StudyGroup.is_public == True) |
            (StudyGroup.id.in_(user_groups)) |
            (StudyGroup.created_by == current_user.id)
        )
    
    if subject:
        query = query.filter(StudyGroup.subject == subject)
    if is_public is not None:
        query = query.filter(StudyGroup.is_public == is_public)
    
    groups = query.all()
    
    # Ajouter le nombre de membres
    result = []
    for group in groups:
        members_count = db.query(StudyGroupMember).filter(
            StudyGroupMember.group_id == group.id,
            StudyGroupMember.is_active == True
        ).count()
        
        result.append(StudyGroupResponse(
            **group.__dict__,
            members_count=members_count
        ))
    
    return result

@router.post("/study-groups/{group_id}/join")
async def join_study_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rejoindre un groupe d'étude"""
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent rejoindre des groupes"
        )
    
    group = db.query(StudyGroup).filter(StudyGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Groupe non trouvé"
        )
    
    # Vérifier si l'utilisateur est déjà membre
    existing_member = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous êtes déjà membre de ce groupe"
        )
    
    # Vérifier le nombre maximum de membres
    members_count = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.is_active == True
    ).count()
    
    if members_count >= group.max_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le groupe est complet"
        )
    
    member = StudyGroupMember(
        group_id=group_id,
        user_id=current_user.id,
        role="member"
    )
    
    db.add(member)
    db.commit()
    
    return {"message": "Vous avez rejoint le groupe avec succès"}

@router.post("/study-groups/{group_id}/messages", response_model=GroupMessageResponse)
async def create_group_message(
    group_id: int,
    message: GroupMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un message dans un groupe"""
    # Vérifier si l'utilisateur est membre du groupe
    member = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.user_id == current_user.id,
        StudyGroupMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du groupe pour envoyer des messages"
        )
    
    db_message = GroupMessage(
        group_id=group_id,
        user_id=current_user.id,
        content=message.content,
        message_type=message.message_type,
        attachments=message.attachments
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return GroupMessageResponse(
        **db_message.__dict__,
        user_name=current_user.username
    )

@router.get("/study-groups/{group_id}/messages", response_model=List[GroupMessageResponse])
async def get_group_messages(
    group_id: int,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les messages d'un groupe"""
    # Vérifier si l'utilisateur est membre du groupe
    member = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.user_id == current_user.id,
        StudyGroupMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du groupe pour voir les messages"
        )
    
    messages = db.query(GroupMessage).filter(
        GroupMessage.group_id == group_id
    ).order_by(GroupMessage.created_at.desc()).offset(offset).limit(limit).all()
    
    result = []
    for message in messages:
        user = db.query(User).filter(User.id == message.user_id).first()
        result.append(GroupMessageResponse(
            **message.__dict__,
            user_name=user.username if user else None
        ))
    
    return result

@router.post("/study-groups/{group_id}/resources", response_model=GroupResourceResponse)
async def create_group_resource(
    group_id: int,
    resource: GroupResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une ressource dans un groupe"""
    # Vérifier si l'utilisateur est membre du groupe
    member = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.user_id == current_user.id,
        StudyGroupMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du groupe pour partager des ressources"
        )
    
    db_resource = GroupResource(
        group_id=group_id,
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        file_url=resource.file_url,
        file_size=resource.file_size,
        uploaded_by=current_user.id
    )
    
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    
    return GroupResourceResponse(**db_resource.__dict__)

@router.get("/study-groups/{group_id}/resources", response_model=List[GroupResourceResponse])
async def get_group_resources(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les ressources d'un groupe"""
    # Vérifier si l'utilisateur est membre du groupe
    member = db.query(StudyGroupMember).filter(
        StudyGroupMember.group_id == group_id,
        StudyGroupMember.user_id == current_user.id,
        StudyGroupMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du groupe pour voir les ressources"
        )
    
    resources = db.query(GroupResource).filter(
        GroupResource.group_id == group_id
    ).all()
    
    return [GroupResourceResponse(**resource.__dict__) for resource in resources]

# Collaboration Projects
@router.post("/projects", response_model=CollaborationProjectResponse)
async def create_collaboration_project(
    project: CollaborationProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un projet collaboratif"""
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les étudiants peuvent créer des projets collaboratifs"
        )
    
    db_project = CollaborationProject(
        title=project.title,
        description=project.description,
        subject=project.subject,
        due_date=project.due_date,
        created_by=current_user.id
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Ajouter le créateur comme membre
    member = ProjectMember(
        project_id=db_project.id,
        user_id=current_user.id,
        role="leader"
    )
    db.add(member)
    db.commit()
    
    return CollaborationProjectResponse(
        **db_project.__dict__,
        members_count=1
    )

@router.get("/projects", response_model=List[CollaborationProjectResponse])
async def get_collaboration_projects(
    status: Optional[str] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les projets collaboratifs"""
    query = db.query(CollaborationProject)
    
    if current_user.role == UserRole.student:
        # Étudiants : voir leurs projets
        user_projects = db.query(ProjectMember.project_id).filter(
            ProjectMember.user_id == current_user.id
        ).subquery()
        
        query = query.filter(
            (CollaborationProject.id.in_(user_projects)) |
            (CollaborationProject.created_by == current_user.id)
        )
    
    if status:
        query = query.filter(CollaborationProject.status == status)
    if subject:
        query = query.filter(CollaborationProject.subject == subject)
    
    projects = query.all()
    
    # Ajouter le nombre de membres
    result = []
    for project in projects:
        members_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == project.id,
            ProjectMember.is_active == True
        ).count()
        
        result.append(CollaborationProjectResponse(
            **project.__dict__,
            members_count=members_count
        ))
    
    return result

@router.post("/projects/{project_id}/tasks", response_model=ProjectTaskResponse)
async def create_project_task(
    project_id: int,
    task: ProjectTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une tâche dans un projet"""
    # Vérifier si l'utilisateur est membre du projet
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du projet pour créer des tâches"
        )
    
    db_task = ProjectTask(
        project_id=project_id,
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        priority=task.priority,
        due_date=task.due_date,
        created_by=current_user.id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return ProjectTaskResponse(**db_task.__dict__)

@router.get("/projects/{project_id}/tasks", response_model=List[ProjectTaskResponse])
async def get_project_tasks(
    project_id: int,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les tâches d'un projet"""
    # Vérifier si l'utilisateur est membre du projet
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.is_active == True
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous devez être membre du projet pour voir les tâches"
        )
    
    query = db.query(ProjectTask).filter(ProjectTask.project_id == project_id)
    
    if status:
        query = query.filter(ProjectTask.status == status)
    if assigned_to:
        query = query.filter(ProjectTask.assigned_to == assigned_to)
    
    tasks = query.all()
    return [ProjectTaskResponse(**task.__dict__) for task in tasks]
