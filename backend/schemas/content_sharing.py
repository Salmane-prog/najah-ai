from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

# Schémas pour les requêtes de partage
class ContentSharingCreate(BaseModel):
    content_id: int
    target_type: str = Field(..., description="Type de cible: 'class', 'student', 'all_students'")
    target_ids: Optional[List[int]] = Field(None, description="IDs des classes ou étudiants cibles")
    
    # Paramètres de partage
    allow_download: bool = True
    allow_view: bool = True
    expiration_date: Optional[datetime] = None
    
    # Notifications
    notify_students: bool = True
    custom_message: Optional[str] = None

class ContentSharingUpdate(BaseModel):
    is_active: Optional[bool] = None
    allow_download: Optional[bool] = None
    allow_view: Optional[bool] = None
    expiration_date: Optional[datetime] = None
    custom_message: Optional[str] = None

# Schémas pour les réponses
class ContentSharingRead(BaseModel):
    id: int
    content_id: int
    shared_by: int
    shared_at: datetime
    is_active: bool
    
    target_type: str
    target_ids: Optional[List[int]]
    
    allow_download: bool
    allow_view: bool
    expiration_date: Optional[datetime]
    
    notify_students: bool
    custom_message: Optional[str]
    
    view_count: int
    download_count: int
    student_count: int
    
    # Informations du contenu
    content_title: str
    content_subject: str
    content_type: str
    
    # Informations de l'enseignant
    teacher_name: str
    
    class Config:
        from_attributes = True

class ContentAccessRead(BaseModel):
    id: int
    content_id: int
    student_id: int
    sharing_id: int
    
    first_accessed: Optional[datetime]
    last_accessed: Optional[datetime]
    access_count: int
    
    can_view: bool
    can_download: bool
    
    # Informations de l'étudiant
    student_name: str
    student_email: str
    
    # Informations du contenu
    content_title: str
    
    class Config:
        from_attributes = True

# Schémas pour les statistiques
class ContentSharingStats(BaseModel):
    total_sharings: int
    active_sharings: int
    total_views: int
    total_downloads: int
    total_students_reached: int
    
    # Statistiques par période
    sharings_this_week: int
    sharings_this_month: int
    views_this_week: int
    downloads_this_week: int

# Schémas pour la sélection des cibles
class SharingTarget(BaseModel):
    id: int
    name: str
    type: str  # 'class' ou 'student'
    student_count: Optional[int] = None  # Pour les classes

class SharingTargetsResponse(BaseModel):
    classes: List[SharingTarget]
    students: List[SharingTarget]
    all_students_count: int



