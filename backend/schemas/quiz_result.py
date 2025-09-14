from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class QuizResultBase(BaseModel):
    student_id: int
    quiz_id: int
    score: float
    max_score: Optional[float] = None
    percentage: Optional[float] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    sujet: Optional[str] = None
    answers: Optional[str] = None
    time_spent: Optional[int] = None
    created_at: Optional[datetime] = None

class QuizResultCreate(QuizResultBase):
    pass

class QuizResultRead(QuizResultBase):
    id: int
    
    class Config:
        from_attributes = True

class QuizResultDetail(QuizResultRead):
    quiz_title: str
    subject: str
    max_score: float
    
    class Config:
        from_attributes = True

class QuizResultSummary(BaseModel):
    total_quizzes: int
    average_score: float
    best_score: float
    
    class Config:
        from_attributes = True 