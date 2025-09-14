from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class QuizAssignmentBase(BaseModel):
    quiz_id: int
    student_id: int
    due_date: Optional[datetime] = None
    feedback: Optional[str] = None

class QuizAssignmentCreate(QuizAssignmentBase):
    pass

class QuizAssignmentUpdate(BaseModel):
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None

class QuizAssignmentRead(QuizAssignmentBase):
    id: int
    assigned_by: int
    assigned_at: datetime
    status: str
    score: Optional[int] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuizAssignmentResponse(BaseModel):
    id: int
    quiz_id: int
    student_id: int
    student_name: str
    student_email: str
    assigned_by: int
    assigned_at: datetime
    due_date: Optional[datetime] = None
    status: str
    score: Optional[int] = None
    completed_at: Optional[datetime] = None
    feedback: Optional[str] = None
    quiz_title: str
    quiz_subject: str
    
    class Config:
        from_attributes = True
