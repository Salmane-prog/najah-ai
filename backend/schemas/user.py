from pydantic import BaseModel, EmailStr, ConfigDict
from models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str 