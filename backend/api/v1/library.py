from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User
from models.library import UserFavorite, Collection, CollectionItem, ContentHistory, ContentRecommendation, Playlist, PlaylistItem
from models.content import Content
from models.class_group import ClassGroup

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/library", tags=["Library"])

# =====================================================
# ENDPOINTS POUR LES RESSOURCES
# =====================================================

@router.get("/resources", response_model=List[dict])
def get_resources(
    subject: Optional[str] = None,
    level: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les ressources de la bibliothèque avec filtres"""
    query = db.query(Content)
    
    if subject:
        query = query.filter(Content.subject == subject)
    if level:
        query = query.filter(Content.level == level)
    if type:
        query = query.filter(Content.type == type)
    if search:
        query = query.filter(
            (Content.title.contains(search)) | 
            (Content.description.contains(search))
        )
    
    resources = query.offset(offset).limit(limit).all()
    
    # Convertir en format compatible avec le frontend
    result = []
    for resource in resources:
        # Vérifier si l'utilisateur a mis en favori
        is_favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.content_id == resource.id
        ).first() is not None
        
        resource_data = {
            "id": resource.id,
            "title": resource.title,
            "description": resource.description,
            "type": resource.type,
            "subject": resource.subject,
            "level": resource.level,
            "tags": json.loads(resource.tags) if resource.tags else [],
            "author": resource.author,
            "created_at": resource.created_at.isoformat() if resource.created_at else "",
            "duration": getattr(resource, 'duration', None),
            "file_size": getattr(resource, 'file_size', None),
            "views": getattr(resource, 'views', 0),
            "rating": getattr(resource, 'rating', 0.0),
            "is_favorite": is_favorite,
            "is_in_collection": False,  # À implémenter
            "collections": [],
            "url": getattr(resource, 'url', ''),
            "thumbnail": getattr(resource, 'thumbnail', '')
        }
        result.append(resource_data)
    
    return result

@router.get("/resources/{resource_id}", response_model=dict)
def get_resource_by_id(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une ressource spécifique"""
    resource = db.query(Content).filter(Content.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    
    # Vérifier si l'utilisateur a mis en favori
    is_favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.content_id == resource.id
    ).first() is not None
    
    return {
        "id": resource.id,
        "title": resource.title,
        "description": resource.description,
        "type": resource.type,
        "subject": resource.subject,
        "level": resource.level,
        "tags": json.loads(resource.tags) if resource.tags else [],
        "author": resource.author,
        "created_at": resource.created_at.isoformat() if resource.created_at else "",
        "duration": getattr(resource, 'duration', None),
        "file_size": getattr(resource, 'file_size', None),
        "views": getattr(resource, 'views', 0),
        "rating": getattr(resource, 'rating', 0.0),
        "is_favorite": is_favorite,
        "url": getattr(resource, 'url', ''),
        "thumbnail": getattr(resource, 'thumbnail', '')
    }

# =====================================================
# ENDPOINTS POUR LES FAVORIS
# =====================================================

@router.post("/resources/{resource_id}/favorite")
def toggle_favorite(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ajouter/retirer une ressource des favoris"""
    # Vérifier que la ressource existe
    resource = db.query(Content).filter(Content.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    
    # Vérifier si déjà en favori
    existing_favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.content_id == resource_id
    ).first()
    
    if existing_favorite:
        # Retirer des favoris
        db.delete(existing_favorite)
        db.commit()
        return {"message": "Ressource retirée des favoris"}
    else:
        # Ajouter aux favoris
        new_favorite = UserFavorite(
            user_id=current_user.id,
            content_id=resource_id
        )
        db.add(new_favorite)
        db.commit()
        return {"message": "Ressource ajoutée aux favoris"}

@router.post("/resources/{resource_id}/collection")
def toggle_collection(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ajouter/retirer une ressource d'une collection par défaut"""
    # Vérifier que la ressource existe
    resource = db.query(Content).filter(Content.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    
    # Récupérer ou créer une collection par défaut pour l'utilisateur
    default_collection = db.query(Collection).filter(
        Collection.user_id == current_user.id,
        Collection.name == "Mes Favoris"
    ).first()
    
    if not default_collection:
        # Créer une collection par défaut
        default_collection = Collection(
            name="Mes Favoris",
            description="Ressources que j'aime",
            user_id=current_user.id,
            is_public=False,
            color="bg-yellow-100"
        )
        db.add(default_collection)
        db.commit()
        db.refresh(default_collection)
    
    # Vérifier si la ressource est déjà dans la collection
    existing_item = db.query(CollectionItem).filter(
        CollectionItem.collection_id == default_collection.id,
        CollectionItem.content_id == resource_id
    ).first()
    
    if existing_item:
        # Retirer de la collection
        db.delete(existing_item)
        db.commit()
        return {"message": "Ressource retirée de la collection"}
    else:
        # Ajouter à la collection
        new_item = CollectionItem(
            collection_id=default_collection.id,
            content_id=resource_id
        )
        db.add(new_item)
        db.commit()
        return {"message": "Ressource ajoutée à la collection"}

# =====================================================
# ENDPOINTS POUR LES COLLECTIONS
# =====================================================

@router.get("/collections", response_model=List[dict])
def get_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les collections de l'utilisateur"""
    collections = db.query(Collection).filter(Collection.user_id == current_user.id).all()
    
    result = []
    for collection in collections:
        # Compter le nombre de ressources dans la collection
        resource_count = db.query(CollectionItem).filter(
            CollectionItem.collection_id == collection.id
        ).count()
        
        collection_data = {
            "id": collection.id,
            "name": collection.name,
            "description": collection.description,
            "resource_count": resource_count,
            "is_public": collection.is_public,
            "created_at": collection.created_at.isoformat() if collection.created_at else "",
            "color": collection.color
        }
        result.append(collection_data)
    
    return result

@router.post("/collections", response_model=dict)
def create_collection(
    collection_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle collection"""
    db_collection = Collection(
        name=collection_data.get("name", ""),
        description=collection_data.get("description", ""),
        user_id=current_user.id,
        is_public=collection_data.get("is_public", False),
        color=collection_data.get("color", "bg-blue-100")
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return {
        "id": db_collection.id,
        "name": db_collection.name,
        "description": db_collection.description,
        "resource_count": 0,
        "is_public": db_collection.is_public,
        "created_at": db_collection.created_at.isoformat() if db_collection.created_at else "",
        "color": db_collection.color
    }

# =====================================================
# ENDPOINTS POUR LES MATIÈRES ET NIVEAUX
# =====================================================

@router.get("/subjects", response_model=List[dict])
def get_subjects(db: Session = Depends(get_db)):
    """Récupérer toutes les matières disponibles"""
    # Récupérer les matières uniques depuis les contenus
    subjects = db.query(Content.subject).distinct().all()
    
    result = []
    for subject in subjects:
        if subject[0]:  # Vérifier que le sujet n'est pas None
            # Compter le nombre de ressources pour cette matière
            resource_count = db.query(Content).filter(Content.subject == subject[0]).count()
            
            subject_data = {
                "id": len(result) + 1,  # ID temporaire
                "name": subject[0],
                "color": f"bg-blue-{500 - (len(result) * 100)}",
                "resource_count": resource_count
            }
            result.append(subject_data)
    
    return result

@router.get("/levels", response_model=List[dict])
def get_levels(db: Session = Depends(get_db)):
    """Récupérer tous les niveaux disponibles"""
    # Récupérer les niveaux uniques depuis les contenus
    levels = db.query(Content.level).distinct().all()
    
    result = []
    for level in levels:
        if level[0]:  # Vérifier que le niveau n'est pas None
            # Compter le nombre de ressources pour ce niveau
            resource_count = db.query(Content).filter(Content.level == level[0]).count()
            
            level_data = {
                "id": len(result) + 1,  # ID temporaire
                "name": level[0],
                "color": f"bg-green-{500 - (len(result) * 100)}",
                "resource_count": resource_count
            }
            result.append(level_data)
    
    return result

# =====================================================
# ENDPOINTS POUR LES RECOMMANDATIONS
# =====================================================

@router.get("/recommendations", response_model=List[dict])
def get_recommendations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les recommandations de ressources pour l'utilisateur"""
    # Logique simple de recommandation basée sur l'historique
    # À améliorer avec un algorithme plus sophistiqué
    
    # Récupérer les ressources les plus populaires
    popular_resources = db.query(Content).order_by(Content.views.desc()).limit(limit).all()
    
    result = []
    for resource in popular_resources:
        resource_data = {
            "id": resource.id,
            "title": resource.title,
            "description": resource.description,
            "type": resource.type,
            "subject": resource.subject,
            "level": resource.level,
            "rating": getattr(resource, 'rating', 0.0),
            "views": getattr(resource, 'views', 0)
        }
        result.append(resource_data)
    
    return result 