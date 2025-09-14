from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class ClassGroup(Base):
    __tablename__ = "class_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(String, nullable=True)  # 'primary', 'middle', 'high', 'university'
    subject = Column(String, nullable=True)  # Matière principale
    max_students = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    teacher = relationship("User", foreign_keys=[teacher_id], viewonly=True)
    students = relationship("ClassStudent", foreign_keys="ClassStudent.class_id", viewonly=True)

class ClassStudent(Base):
    __tablename__ = "class_students"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_group = relationship("ClassGroup", foreign_keys=[class_id], viewonly=True)
    student = relationship("User", foreign_keys=[student_id], viewonly=True) 