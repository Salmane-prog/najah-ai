import sys
sys.path.append('.')

from database import get_db
from models.user import User

def check_students():
    db = next(get_db())
    students = db.query(User).filter(User.role == 'student').all()
    
    print('Étudiants disponibles:')
    for student in students:
        print(f'ID: {student.id}, Nom: {student.first_name} {student.last_name}')
    
    if not students:
        print('Aucun étudiant trouvé!')

if __name__ == "__main__":
    check_students() 