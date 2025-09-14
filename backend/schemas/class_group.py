from pydantic import BaseModel
from typing import Optional, List

class ClassGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    teacher_id: Optional[int] = None

class ClassGroupCreate(ClassGroupBase):
    pass

class ClassGroupRead(ClassGroupBase):
    id: int
    class Config:
        from_attributes = True

class ClassStudentBase(BaseModel):
    student_id: int
    class_group_id: int

class ClassStudentCreate(ClassStudentBase):
    pass

class ClassStudentRead(ClassStudentBase):
    id: int
    class Config:
        from_attributes = True

class ClassStudentWithUserRead(ClassStudentBase):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class ClassGroupWithStudents(ClassGroupRead):
    students: List[ClassStudentRead] = [] 