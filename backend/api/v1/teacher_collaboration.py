from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.quiz import Quiz
from models.content import Content
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/shared-resources")
def get_shared_resources(
    resource_type: str = None,
    subject: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les ressources partagées par d'autres professeurs."""
    try:
        # Récupérer les quiz partagés
        quiz_query = db.query(Quiz).filter(
            Quiz.is_shared == True,
            Quiz.created_by != current_user.id
        )
        
        if subject:
            quiz_query = quiz_query.filter(Quiz.subject == subject)
        
        shared_quizzes = quiz_query.all()
        
        # Récupérer les contenus partagés
        content_query = db.query(Content).filter(
            Content.is_shared == True,
            Content.created_by != current_user.id
        )
        
        if resource_type:
            content_query = content_query.filter(Content.content_type == resource_type)
        
        if subject:
            content_query = content_query.filter(Content.subject == subject)
        
        shared_contents = content_query.all()
        
        # Récupérer les informations des créateurs
        creator_ids = set()
        for quiz in shared_quizzes:
            creator_ids.add(quiz.created_by)
        for content in shared_contents:
            creator_ids.add(content.created_by)
        
        creators = db.query(User).filter(User.id.in_(creator_ids)).all()
        creators_dict = {c.id: c for c in creators}
        
        return {
            "shared_quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "subject": quiz.subject,
                    "description": quiz.description,
                    "difficulty": quiz.difficulty,
                    "total_questions": quiz.total_questions,
                    "created_by": {
                        "id": creators_dict.get(quiz.created_by, {}).id,
                        "name": f"{creators_dict.get(quiz.created_by, {}).first_name} {creators_dict.get(quiz.created_by, {}).last_name}",
                        "email": creators_dict.get(quiz.created_by, {}).email
                    },
                    "created_at": quiz.created_at.isoformat(),
                    "downloads_count": quiz.downloads_count if hasattr(quiz, 'downloads_count') else 0,
                    "rating": quiz.rating if hasattr(quiz, 'rating') else 0
                }
                for quiz in shared_quizzes
            ],
            "shared_contents": [
                {
                    "id": content.id,
                    "title": content.title,
                    "subject": content.subject,
                    "description": content.description,
                    "content_type": content.content_type,
                    "difficulty": content.difficulty,
                    "estimated_time": content.estimated_time,
                    "created_by": {
                        "id": creators_dict.get(content.created_by, {}).id,
                        "name": f"{creators_dict.get(content.created_by, {}).first_name} {creators_dict.get(content.created_by, {}).last_name}",
                        "email": creators_dict.get(content.created_by, {}).email
                    },
                    "created_at": content.created_at.isoformat(),
                    "downloads_count": content.downloads_count if hasattr(content, 'downloads_count') else 0,
                    "rating": content.rating if hasattr(content, 'rating') else 0
                }
                for content in shared_contents
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des ressources partagées: {str(e)}")

@router.post("/share-resource")
def share_resource(
    resource_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Partager une ressource avec d'autres professeurs."""
    try:
        resource_type = resource_data.get("resource_type")
        resource_id = resource_data.get("resource_id")
        description = resource_data.get("description", "")
        
        if resource_type == "quiz":
            resource = db.query(Quiz).filter(
                Quiz.id == resource_id,
                Quiz.created_by == current_user.id
            ).first()
            
            if not resource:
                raise HTTPException(status_code=404, detail="Quiz non trouvé")
            
            resource.is_shared = True
            resource.shared_description = description
            resource.shared_at = datetime.utcnow()
            
        elif resource_type == "content":
            resource = db.query(Content).filter(
                Content.id == resource_id,
                Content.created_by == current_user.id
            ).first()
            
            if not resource:
                raise HTTPException(status_code=404, detail="Contenu non trouvé")
            
            resource.is_shared = True
            resource.shared_description = description
            resource.shared_at = datetime.utcnow()
        
        else:
            raise HTTPException(status_code=400, detail="Type de ressource non supporté")
        
        db.commit()
        db.refresh(resource)
        
        return {
            "message": "Ressource partagée avec succès",
            "resource_id": resource.id,
            "resource_type": resource_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du partage de la ressource: {str(e)}")

@router.post("/download-resource")
def download_resource(
    resource_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Télécharger une ressource partagée."""
    try:
        resource_type = resource_data.get("resource_type")
        resource_id = resource_data.get("resource_id")
        
        if resource_type == "quiz":
            original_quiz = db.query(Quiz).filter(
                Quiz.id == resource_id,
                Quiz.is_shared == True
            ).first()
            
            if not original_quiz:
                raise HTTPException(status_code=404, detail="Quiz non trouvé")
            
            # Créer une copie du quiz
            new_quiz = Quiz(
                title=f"Copie - {original_quiz.title}",
                subject=original_quiz.subject,
                description=original_quiz.description,
                difficulty=original_quiz.difficulty,
                total_points=original_quiz.total_points,
                time_limit=original_quiz.time_limit,
                created_by=current_user.id,
                created_at=datetime.utcnow(),
                is_shared=False
            )
            
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)
            
            # Copier les questions
            from models.quiz import Question
            original_questions = db.query(Question).filter(
                Question.quiz_id == original_quiz.id
            ).all()
            
            for question in original_questions:
                new_question = Question(
                    quiz_id=new_quiz.id,
                    question_text=question.question_text,
                    question_type=question.question_type,
                    correct_answer=question.correct_answer,
                    points=question.points,
                    explanation=question.explanation,
                    options=question.options
                )
                db.add(new_question)
            
            # Incrémenter le compteur de téléchargements
            original_quiz.downloads_count = (original_quiz.downloads_count or 0) + 1
            
        elif resource_type == "content":
            original_content = db.query(Content).filter(
                Content.id == resource_id,
                Content.is_shared == True
            ).first()
            
            if not original_content:
                raise HTTPException(status_code=404, detail="Contenu non trouvé")
            
            # Créer une copie du contenu
            new_content = Content(
                title=f"Copie - {original_content.title}",
                description=original_content.description,
                content_type=original_content.content_type,
                subject=original_content.subject,
                difficulty=original_content.difficulty,
                estimated_time=original_content.estimated_time,
                file_url=original_content.file_url,
                created_by=current_user.id,
                created_at=datetime.utcnow(),
                is_shared=False
            )
            
            db.add(new_content)
            db.commit()
            db.refresh(new_content)
            
            # Incrémenter le compteur de téléchargements
            original_content.downloads_count = (original_content.downloads_count or 0) + 1
        
        else:
            raise HTTPException(status_code=400, detail="Type de ressource non supporté")
        
        db.commit()
        
        return {
            "message": "Ressource téléchargée avec succès",
            "new_resource_id": new_quiz.id if resource_type == "quiz" else new_content.id,
            "resource_type": resource_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement: {str(e)}")

@router.post("/rate-resource")
def rate_resource(
    rating_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Évaluer une ressource partagée."""
    try:
        resource_type = rating_data.get("resource_type")
        resource_id = rating_data.get("resource_id")
        rating = rating_data.get("rating")
        comment = rating_data.get("comment", "")
        
        if not 1 <= rating <= 5:
            raise HTTPException(status_code=400, detail="La note doit être entre 1 et 5")
        
        if resource_type == "quiz":
            resource = db.query(Quiz).filter(
                Quiz.id == resource_id,
                Quiz.is_shared == True
            ).first()
            
        elif resource_type == "content":
            resource = db.query(Content).filter(
                Content.id == resource_id,
                Content.is_shared == True
            ).first()
        
        else:
            raise HTTPException(status_code=400, detail="Type de ressource non supporté")
        
        if not resource:
            raise HTTPException(status_code=404, detail="Ressource non trouvée")
        
        # Créer ou mettre à jour l'évaluation
        from models.ratings import ResourceRating
        
        existing_rating = db.query(ResourceRating).filter(
            ResourceRating.resource_id == resource_id,
            ResourceRating.resource_type == resource_type,
            ResourceRating.user_id == current_user.id
        ).first()
        
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.comment = comment
            existing_rating.updated_at = datetime.utcnow()
        else:
            new_rating = ResourceRating(
                resource_id=resource_id,
                resource_type=resource_type,
                user_id=current_user.id,
                rating=rating,
                comment=comment,
                created_at=datetime.utcnow()
            )
            db.add(new_rating)
        
        # Recalculer la note moyenne
        all_ratings = db.query(ResourceRating).filter(
            ResourceRating.resource_id == resource_id,
            ResourceRating.resource_type == resource_type
        ).all()
        
        if all_ratings:
            avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
            resource.rating = round(avg_rating, 2)
        
        db.commit()
        
        return {
            "message": "Évaluation soumise avec succès",
            "resource_id": resource_id,
            "rating": rating,
            "average_rating": resource.rating
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'évaluation: {str(e)}")

@router.get("/collaboration-stats")
def get_collaboration_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les statistiques de collaboration."""
    try:
        # Statistiques des ressources partagées par le professeur
        shared_quizzes = db.query(Quiz).filter(
            Quiz.created_by == current_user.id,
            Quiz.is_shared == True
        ).count()
        
        shared_contents = db.query(Content).filter(
            Content.created_by == current_user.id,
            Content.is_shared == True
        ).count()
        
        # Statistiques des téléchargements
        total_downloads = 0
        for quiz in db.query(Quiz).filter(
            Quiz.created_by == current_user.id,
            Quiz.is_shared == True
        ).all():
            total_downloads += quiz.downloads_count or 0
        
        for content in db.query(Content).filter(
            Content.created_by == current_user.id,
            Content.is_shared == True
        ).all():
            total_downloads += content.downloads_count or 0
        
        # Statistiques des évaluations reçues
        from models.ratings import ResourceRating
        
        quiz_ratings = db.query(ResourceRating).join(Quiz).filter(
            Quiz.created_by == current_user.id,
            ResourceRating.resource_type == "quiz"
        ).all()
        
        content_ratings = db.query(ResourceRating).join(Content).filter(
            Content.created_by == current_user.id,
            ResourceRating.resource_type == "content"
        ).all()
        
        all_ratings = quiz_ratings + content_ratings
        avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings) if all_ratings else 0
        
        return {
            "shared_resources": {
                "quizzes": shared_quizzes,
                "contents": shared_contents,
                "total": shared_quizzes + shared_contents
            },
            "downloads": {
                "total_downloads": total_downloads,
                "average_downloads_per_resource": total_downloads / (shared_quizzes + shared_contents) if (shared_quizzes + shared_contents) > 0 else 0
            },
            "ratings": {
                "total_ratings": len(all_ratings),
                "average_rating": round(avg_rating, 2),
                "rating_distribution": {
                    "5_stars": len([r for r in all_ratings if r.rating == 5]),
                    "4_stars": len([r for r in all_ratings if r.rating == 4]),
                    "3_stars": len([r for r in all_ratings if r.rating == 3]),
                    "2_stars": len([r for r in all_ratings if r.rating == 2]),
                    "1_star": len([r for r in all_ratings if r.rating == 1])
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des statistiques: {str(e)}") 