from core.database import Base, engine, SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash

Base.metadata.create_all(bind=engine)

def init_users():
    db = SessionLocal()
    users = [
        User(username="student1", email="student1@example.com", hashed_password=get_password_hash("studentpass"), role=UserRole.student),
        User(username="parent1", email="parent1@example.com", hashed_password=get_password_hash("parentpass"), role=UserRole.parent),
        User(username="teacher1", email="teacher1@example.com", hashed_password=get_password_hash("teacherpass"), role=UserRole.teacher),
        User(username="admin1", email="admin1@example.com", hashed_password=get_password_hash("adminpass"), role=UserRole.admin),
    ]
    for user in users:
        if not db.query(User).filter_by(username=user.username).first():
            db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_users() 