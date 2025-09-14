from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from schemas.user import UserCreate, UserRead
from core.security import get_password_hash, decode_access_token, get_current_user
from typing import List, Optional, Dict, Any

def require_role(roles):
    def role_checker(current_user=Depends(get_current_user)):
        # Convertir les rôles en UserRole enum si ce sont des chaînes
        role_enums = []
        for role in roles:
            if isinstance(role, str):
                try:
                    role_enums.append(UserRole(role))
                except ValueError:
                    continue
            else:
                role_enums.append(role)
        
        if current_user.role not in role_enums:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissions insuffisantes"
            )
        return current_user
    return role_checker

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_users(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),  # Accepter tous les utilisateurs connectés
    role: Optional[str] = Query(None, description="Filtrer par rôle (student, teacher, admin)")
):
    """Lister tous les utilisateurs (utilisateurs connectés uniquement)."""
    try:
        query = db.query(User)
        if role:
            try:
                user_role = UserRole(role)
                query = query.filter(User.role == user_role)
            except ValueError:
                raise HTTPException(status_code=400, detail="Rôle invalide")
        
        users = query.all()
        result = []
        
        for user in users:
            # Déterminer le nom à afficher
            display_name = "Utilisateur sans nom"
            if user.first_name and user.last_name:
                display_name = f"{user.first_name} {user.last_name}"
            elif user.username:
                display_name = user.username
            elif user.email:
                email_name = user.email.split('@')[0]
                display_name = email_name.replace('.', ' ').title()
            
            # Récupérer les informations de classe pour les étudiants
            class_info = None
            if user.role == UserRole.student:
                from models.class_group import ClassStudent, ClassGroup
                class_student = db.query(ClassStudent).filter(
                    ClassStudent.student_id == user.id
                ).first()
                
                if class_student:
                    class_group = db.query(ClassGroup).filter(
                        ClassGroup.id == class_student.class_id
                    ).first()
                    if class_group:
                        class_info = class_group.name
            
            user_data = {
                "id": user.id,
                "name": display_name,
                "email": user.email,
                "role": user.role.value,
                "avatar_url": user.avatar,
                "bio": user.bio,
                "phone": user.phone,
                "class": class_info
            }
            result.append(user_data)
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans list_users: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des utilisateurs: {str(e)}"
        )

@router.get("/students", response_model=List[Dict[str, Any]])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    """Récupérer la liste des étudiants avec leurs données de progression."""
    try:
        print(f"[DEBUG] get_students appelé par user_id: {current_user.id}")
        
        # Récupérer seulement les étudiants de base
        students = db.query(User).filter(User.role == UserRole.student).all()
        result = []
        
        for student in students:
            # Déterminer le nom à afficher
            display_name = "Élève sans nom"
            if student.first_name and student.last_name:
                display_name = f"{student.first_name} {student.last_name}"
            elif student.username:
                display_name = student.username
            elif student.email:
                # Extraire le nom de l'email si pas de username
                email_name = student.email.split('@')[0]
                display_name = email_name.replace('.', ' ').title()
            
            # Récupérer les informations de classe
            class_info = None
            from models.class_group import ClassStudent, ClassGroup
            class_student = db.query(ClassStudent).filter(
                ClassStudent.student_id == student.id
            ).first()
            
            if class_student:
                class_group = db.query(ClassGroup).filter(
                    ClassGroup.id == class_student.class_id
                ).first()
                if class_group:
                    class_info = class_group.name
            
            # Données de base pour éviter les erreurs
            student_data = {
                "id": student.id,
                "name": display_name,
                "email": student.email,
                "role": student.role.value,
                "avatar_url": student.avatar,
                "bio": student.bio,
                "phone": student.phone,
                "class": class_info,
                "overall_progress": 0,  # Valeur par défaut
                "quizzes_completed": 0,  # Valeur par défaut
                "average_score": 0,  # Valeur par défaut
                "last_activity": "Aucune activité",
                "classes": [],  # Liste vide par défaut
                "badges": [],  # Liste vide par défaut
                "recent_activity": []  # Liste vide par défaut
            }
            result.append(student_data)
        
        print(f"[DEBUG] get_students: {len(result)} étudiants trouvés")
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_students: {e}")
        import traceback
        traceback.print_exc()
        return []

@router.get("/by-role/{role}")
def get_users_by_role(
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les utilisateurs par rôle (pour compatibilité avec le frontend)"""
    try:
        # Convertir le rôle en UserRole
        try:
            user_role = UserRole(role)
        except ValueError:
            raise HTTPException(status_code=400, detail="Rôle invalide")
        
        # Récupérer les utilisateurs par rôle
        users = db.query(User).filter(User.role == user_role).all()
        
        result = []
        for user in users:
            # Déterminer le nom à afficher
            display_name = "Utilisateur sans nom"
            if user.first_name and user.last_name:
                display_name = f"{user.first_name} {user.last_name}"
            elif user.username:
                display_name = user.username
            elif user.email:
                email_name = user.email.split('@')[0]
                display_name = email_name.replace('.', ' ').title()
            
            # Récupérer les informations de classe pour les étudiants
            class_info = None
            if user.role == UserRole.student:
                from models.class_group import ClassStudent, ClassGroup
                class_student = db.query(ClassStudent).filter(
                    ClassStudent.student_id == user.id
                ).first()
                
                if class_student:
                    class_group = db.query(ClassGroup).filter(
                        ClassGroup.id == class_student.class_id
                    ).first()
                    if class_group:
                        class_info = class_group.name
            
            user_data = {
                "id": user.id,
                "name": display_name,
                "email": user.email,
                "role": user.role.value,
                "avatar_url": user.avatar,
                "bio": user.bio,
                "phone": user.phone,
                "class": class_info
            }
            result.append(user_data)
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_users_by_role: {e}")
        import traceback
        traceback.print_exc()
        return []

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Récupérer les informations de l'utilisateur connecté (alias pour compatibilité)."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.username,
        "role": current_user.role.value,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }

@router.get("/profile")
def get_user_profile_alias(current_user: User = Depends(get_current_user)):
    """Alias pour /profile qui redirige vers /me (pour compatibilité frontend)"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.username,
        "role": current_user.role.value,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }

@router.get("/user/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(['admin', 'teacher']))):
    """Obtenir un utilisateur par ID (admin et teacher uniquement)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(['admin']))):
    """Créer un nouvel utilisateur (admin uniquement)."""
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(['admin']))):
    """Mettre à jour un utilisateur (admin uniquement)."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = get_password_hash(user.password)
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(['admin']))):
    """Supprimer un utilisateur (admin uniquement)."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None 

@router.get("/students-by-role")
def get_students_by_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les étudiants avec leurs informations de classe (pour compatibilité frontend)"""
    try:
        # Récupérer seulement les étudiants
        students = db.query(User).filter(User.role == UserRole.student).all()
        result = []
        
        for student in students:
            # Déterminer le nom à afficher
            display_name = "Élève sans nom"
            if student.first_name and student.last_name:
                display_name = f"{student.first_name} {student.last_name}"
            elif student.username:
                display_name = student.username
            elif student.email:
                email_name = student.email.split('@')[0]
                display_name = email_name.replace('.', ' ').title()
            
            # Récupérer les informations de classe
            class_info = None
            from models.class_group import ClassStudent, ClassGroup
            class_student = db.query(ClassStudent).filter(
                ClassStudent.student_id == student.id
            ).first()
            
            if class_student:
                class_group = db.query(ClassGroup).filter(
                    ClassGroup.id == class_student.class_id
                ).first()
                if class_group:
                    class_info = class_group.name
            
            student_data = {
                "id": student.id,
                "name": display_name,
                "email": student.email,
                "role": student.role.value,
                "avatar_url": student.avatar,
                "bio": student.bio,
                "phone": student.phone,
                "class": class_info
            }
            result.append(student_data)
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_students_by_role: {e}")
        import traceback
        traceback.print_exc()
        return [] 