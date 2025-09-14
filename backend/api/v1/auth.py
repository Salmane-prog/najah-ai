from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from schemas.user import UserCreate, UserLogin
from core.security import get_password_hash, verify_password, create_access_token, get_current_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_role(allowed_roles: List[str]):
    """Décorateur pour vérifier le rôle de l'utilisateur"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissions insuffisantes"
            )
        return current_user
    return role_checker

@router.options("/login")
def login_options():
    """Gérer les requêtes OPTIONS pour le login (CORS preflight)"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Récupérer les informations de l'utilisateur connecté."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.username,
        "role": current_user.role.value,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("[DEBUG] Route /register appelée")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username déjà utilisé")
    hashed = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        role=user.role if hasattr(user, 'role') else UserRole.student
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"[REGISTER] Utilisateur créé: id={db_user.id}, email={db_user.email}")
    return {"message": "Inscription réussie"}

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    print(f"[DEBUG] /login appelée avec email={user_login.email}")
    print(f"[DEBUG] Début de la fonction login")
    
    try:
        user = db.query(User).filter(User.email == user_login.email).first()
        print(f"[DEBUG] Recherche utilisateur: {user is not None}")
        
        if not user:
            print("[DEBUG] Aucun utilisateur trouvé pour cet email")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
        
        print(f"[DEBUG] Utilisateur trouvé: id={user.id}, email={user.email}")
        
        print(f"[DEBUG] Hash en base: {user.hashed_password}")
        print(f"[DEBUG] Mot de passe fourni: {user_login.password}")
        
        is_valid = verify_password(user_login.password, user.hashed_password)
        print(f"[DEBUG] Résultat vérification: {is_valid}")
        
        if not is_valid:
            print("[DEBUG] Mot de passe incorrect pour cet utilisateur")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
        
        print(f"[DEBUG] Mot de passe vérifié avec succès")
        print(f"[DEBUG] Login réussi pour id={user.id}, email={user.email}, role={user.role}")
        
        access_token = create_access_token({"sub": user.email, "role": user.role.value})
        print(f"[DEBUG] Token créé: {access_token[:20]}...")
        
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role.value,
            "id": user.id,
            "name": user.username
        }
        print(f"[DEBUG] Réponse préparée: {response_data}")
        return response_data
        
    except HTTPException:
        # Relancer les HTTPException sans modification
        raise
    except Exception as e:
        print(f"[ERROR] Exception dans login: {str(e)}")
        print(f"[ERROR] Type d'exception: {type(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur interne: {str(e)}") 