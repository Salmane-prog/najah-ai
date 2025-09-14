from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Schémas pour les étapes de parcours
class LearningPathStepCreate(BaseModel):
    learning_path_id: int
    title: str
    description: Optional[str] = None
    step_type: str = Field(..., description="Type d'étape: content, quiz, assessment, activity")
    content_id: Optional[int] = None
    quiz_id: Optional[int] = None
    order: int
    estimated_duration: int = Field(default=15, description="Durée estimée en minutes")
    is_required: bool = True
    prerequisites: Optional[List[int]] = None

class LearningPathStepRead(BaseModel):
    id: int
    learning_path_id: int
    title: str
    description: Optional[str]
    step_type: str
    content_id: Optional[int]
    quiz_id: Optional[int]
    order: int
    estimated_duration: int
    is_required: bool
    prerequisites: Optional[List[int]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Schémas pour la progression des étudiants
class StudentProgressCreate(BaseModel):
    student_id: int
    learning_path_id: int
    current_step_id: Optional[int] = None

class StudentProgressRead(BaseModel):
    id: int
    student_id: int
    learning_path_id: int
    current_step_id: Optional[int]
    completed_steps: List[int]
    progress_percentage: float
    started_at: datetime
    last_activity: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

# Schémas pour les analytics de classe
class ClassAnalyticsCreate(BaseModel):
    class_id: int
    total_students: int = 0
    active_students: int = 0
    average_progress: float = 0.0
    completed_quizzes: int = 0
    average_score: float = 0.0
    weak_subjects: Optional[List[str]] = None
    strong_subjects: Optional[List[str]] = None

class ClassAnalyticsRead(BaseModel):
    id: int
    class_id: int
    date: datetime
    total_students: int
    active_students: int
    average_progress: float
    completed_quizzes: int
    average_score: float
    weak_subjects: Optional[List[str]]
    strong_subjects: Optional[List[str]]

    class Config:
        from_attributes = True

# Schémas pour les analytics d'étudiant
class StudentAnalyticsCreate(BaseModel):
    student_id: int
    class_id: Optional[int] = None
    total_quizzes: int = 0
    average_score: float = 0.0
    progress_percentage: float = 0.0
    time_spent: int = 0
    completed_contents: int = 0
    weak_subjects: Optional[List[str]] = None
    strong_subjects: Optional[List[str]] = None
    learning_style: Optional[str] = None

class StudentAnalyticsRead(BaseModel):
    id: int
    student_id: int
    class_id: Optional[int]
    date: datetime
    total_quizzes: int
    average_score: float
    progress_percentage: float
    time_spent: int
    completed_contents: int
    weak_subjects: Optional[List[str]]
    strong_subjects: Optional[List[str]]
    learning_style: Optional[str]

    class Config:
        from_attributes = True

# Schémas pour les activités en temps réel
class RealTimeActivityCreate(BaseModel):
    student_id: int
    activity_type: str = Field(..., description="Type d'activité: quiz_start, quiz_complete, content_view, step_complete")
    activity_data: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class RealTimeActivityRead(BaseModel):
    id: int
    student_id: int
    activity_type: str
    activity_data: Optional[Dict[str, Any]]
    timestamp: datetime
    session_id: Optional[str]

    class Config:
        from_attributes = True

# Schémas pour le dashboard enseignant
class TeacherDashboardData(BaseModel):
    total_classes: int
    total_students: int
    active_students: int
    average_class_progress: float
    recent_activities: List[RealTimeActivityRead]
    class_performances: List[ClassAnalyticsRead]
    pending_tasks: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]

# Schémas pour la création de parcours
class LearningPathCreateAdvanced(BaseModel):
    name: str
    description: Optional[str] = None
    objectives: Optional[str] = None
    level: str = Field(..., description="Niveau: beginner, intermediate, advanced")
    estimated_duration: int = Field(default=30, description="Durée estimée en jours")
    is_adaptive: bool = False
    steps: List[LearningPathStepCreate] = []

class LearningPathReadAdvanced(BaseModel):
    id: int
    name: str
    description: Optional[str]
    objectives: Optional[str]
    level: str
    estimated_duration: int
    is_adaptive: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    steps: List[LearningPathStepRead] = []

    class Config:
        from_attributes = True

# Schémas pour la gestion des classes avancée
class ClassGroupCreateAdvanced(BaseModel):
    name: str
    description: Optional[str] = None
    level: str = Field(..., description="Niveau: primary, middle, high, university")
    subject: Optional[str] = None
    max_students: int = 30

class ClassGroupReadAdvanced(BaseModel):
    id: int
    name: str
    description: Optional[str]
    teacher_id: int
    level: str
    subject: Optional[str]
    max_students: int
    is_active: bool
    created_at: datetime
    student_count: int = 0
    average_progress: float = 0.0

    class Config:
        from_attributes = True

# Schémas pour le suivi temps réel
class RealTimeDashboard(BaseModel):
    active_students: int
    current_activities: List[RealTimeActivityRead]
    class_performances: List[ClassAnalyticsRead]
    alerts: List[Dict[str, Any]]
    notifications: List[Dict[str, Any]]

# Schémas pour les rapports
class StudentReport(BaseModel):
    student_id: int
    student_name: str
    class_name: str
    progress_percentage: float
    average_score: float
    total_quizzes: int
    time_spent: int
    weak_subjects: List[str]
    strong_subjects: List[str]
    recommendations: List[str]

class ClassReport(BaseModel):
    class_id: int
    class_name: str
    teacher_name: str
    total_students: int
    average_progress: float
    average_score: float
    top_performers: List[StudentReport]
    students_needing_help: List[StudentReport]
    subject_performance: Dict[str, float] 