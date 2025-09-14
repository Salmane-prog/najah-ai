from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Quiz Schemas
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None
    time_limit: Optional[int] = None

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    time_limit: Optional[int] = None
    is_active: Optional[bool] = None

class QuizRead(QuizBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    is_active: bool
    total_points: Optional[float] = None
    
    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    question_type: str  # 'mcq', 'true_false', 'text'
    points: float = 1.0
    order: int = 0
    options: Optional[List[str]] = None
    correct_answer: Optional[Any] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    points: Optional[float] = None
    order: Optional[int] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[Any] = None

class QuestionRead(QuestionBase):
    id: int
    quiz_id: int
    
    class Config:
        from_attributes = True

# Quiz with Questions
class QuizWithQuestions(QuizRead):
    questions: List[QuestionRead] = []

# Quiz Result Schemas
class QuizResultBase(BaseModel):
    quiz_id: int
    student_id: int
    score: float = 0
    max_score: float = 0
    percentage: float = 0
    is_completed: bool = False

class QuizResultCreate(QuizResultBase):
    pass

class QuizResultRead(QuizResultBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Quiz Answer Schemas
class QuizAnswerBase(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    is_correct: Optional[bool] = None
    points_earned: float = 0
    correct_answer: Optional[str] = None

class QuizAnswerCreate(QuizAnswerBase):
    pass

class QuizAnswerRead(QuizAnswerBase):
    id: int
    result_id: int
    
    class Config:
        from_attributes = True

# Complete Quiz Result with Answers
class QuizResultWithAnswers(QuizResultRead):
    answers: List[QuizAnswerRead] = []

# Quiz Submission
class QuizSubmission(BaseModel):
    quiz_id: int
    answers: List[Dict[str, Any]]  # [{"question_id": 1, "answer": "option1"}, ...] 

class QuizAssignmentBase(BaseModel):
    quiz_id: int
    class_id: Optional[int] = None
    student_id: Optional[int] = None
    due_date: Optional[str] = None
    assigned_by: Optional[int] = None  # Ajout du champ manquant

class QuizAssignmentCreate(QuizAssignmentBase):
    pass

class QuizAssignmentRead(QuizAssignmentBase):
    id: int
    created_at: datetime  # Utiliser created_at au lieu de assigned_at
    
    class Config:
        from_attributes = True

# Schéma enrichi pour les quiz assignés avec détails du quiz
class QuizAssignmentEnriched(BaseModel):
    id: int
    quiz_id: int
    class_id: Optional[int] = None
    student_id: Optional[int] = None
    assigned_at: datetime
    due_date: Optional[str] = None
    quiz: Optional[Dict[str, Any]] = None  # Détails du quiz
    
    class Config:
        from_attributes = True 