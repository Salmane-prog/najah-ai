from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from models.user import User
import hashlib
import jwt
from jwt.exceptions import InvalidTokenError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Hashage de mot de passe

def verify_password(plain_password, hashed_password):
    # Essayer d'abord bcrypt
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"[SECURITY] Erreur bcrypt: {e}")
        
        # Fallback: essayer SHA256
        try:
            sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
            return sha256_hash == hashed_password
        except Exception as e2:
            print(f"[SECURITY] Erreur SHA256: {e2}")
            return False

def get_password_hash(password):
    return pwd_context.hash(password)

# Création et validation de JWT

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except InvalidTokenError as e:
        print(f"JWT Error: {e}")
        return None

# Authentification et autorisation

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    print(f"[DEBUG] get_current_user appelée")
    print(f"[DEBUG] Token reçu: {credentials.credentials[:50]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(credentials.credentials)
        print(f"[DEBUG] Payload décodé: {payload}")
        if payload is None:
            print(f"[DEBUG] Payload est None")
            raise credentials_exception
        user_email: str = payload.get("sub")
        print(f"[DEBUG] Email extrait: {user_email}")
        if user_email is None:
            print(f"[DEBUG] Email est None")
            raise credentials_exception
    except InvalidTokenError as e:
        print(f"[DEBUG] JWT Error: {e}")
        raise credentials_exception
    
    print(f"[DEBUG] Recherche utilisateur avec email: {user_email}")
    user = db.query(User).filter(User.email == user_email).first()
    print(f"[DEBUG] Utilisateur trouvé: {user}")
    if user is None:
        print(f"[DEBUG] Utilisateur non trouvé")
        raise credentials_exception
    
    print(f"[DEBUG] Utilisateur retourné: id={user.id}, role={user.role}")
    return user

def require_role(allowed_roles):
    """
    Dépendance FastAPI pour vérifier les rôles d'utilisateur
    Usage: current_user = Depends(require_role(["student", "teacher"]))
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissions insuffisantes"
            )
        return current_user
    return role_checker 