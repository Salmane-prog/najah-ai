from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.quiz import QuizResult
from schemas.quiz_result import QuizResultCreate, QuizResultRead
from typing import List
from api.v1.users import get_current_user
from api.v1.notifications_ws import send_notification
from api.v1.ai import recommend
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=QuizResultRead, status_code=201)
async def create_quiz_result(result: QuizResultCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_result = QuizResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    # Analyse de l'historique de quiz pour feedback avancé
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == db_result.student_id).all()
    sujets_scores = {}
    for qr in quiz_results:
        sujets_scores.setdefault(qr.sujet, []).append(qr.score)
    sujets_forts = [s for s, scs in sujets_scores.items() if sum(scs)/len(scs) >= 0.8]
    sujets_faibles = [s for s, scs in sujets_scores.items() if sum(scs)/len(scs) < 0.6]
    # Message global
    if db_result.score >= 0.8:
        message = "Excellent travail ! Continue comme ça."
    elif db_result.score >= 0.6:
        message = "Bon effort, mais tu peux encore progresser sur certains thèmes."
    else:
        message = "Il faut retravailler certains sujets. Consulte les recommandations ci-dessous."
    # Suggestions personnalisées (utilise la logique de recommend)
    recos = recommend(user_id=db_result.student_id, db=db, current_user=current_user)
    recommandations = []
    for reco in recos.get("recommendations", []):
        # Ajout d'un champ url si possible (exemple pour content)
        url = None
        if reco["type"] == "content":
            url = f"/dashboard/student/content/{reco['id']}"
        elif reco["type"] == "learning_path":
            url = f"/dashboard/student/learning-path/{reco['id']}"
        recommandations.append({**reco, "url": url})
    feedback = {
        "score": db_result.score,
        "message": message,
        "sujets_forts": sujets_forts,
        "sujets_faibles": sujets_faibles,
        "recommandations": recommandations
    }
    # Envoi via WebSocket
    await send_notification(db_result.student_id, json.dumps({"type": "quiz_feedback", "feedback": feedback}))
    # Retourne aussi le feedback dans la réponse API
    return {"result": db_result, "feedback": feedback}

@router.get("/", response_model=List[QuizResultRead])
def list_all_quiz_results(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupérer tous les résultats de quiz (pour les professeurs)"""
    print(f"[API] /quiz_results/ - Token user: {current_user.id if current_user else 'None'}")
    print(f"[API] User role: {current_user.role}")
    
    # Si c'est un professeur, ne montrer que les résultats des quiz qu'il a créés
    if current_user.role == "teacher":
        # Récupérer les IDs des quiz créés par ce professeur
        from models.quiz import Quiz
        teacher_quizzes = db.query(Quiz.id).filter(Quiz.created_by == current_user.id).all()
        quiz_ids = [q.id for q in teacher_quizzes]
        print(f"[API] Teacher quiz IDs: {quiz_ids}")
        
        if quiz_ids:
            results = db.query(QuizResult).filter(QuizResult.quiz_id.in_(quiz_ids)).order_by(QuizResult.created_at.desc()).all()
            print(f"[API] Found {len(results)} results for teacher")
            for result in results:
                print(f"[API] Result: quiz_id={result.quiz_id}, student_id={result.student_id}, is_completed={result.is_completed}")
            return results
        else:
            print(f"[API] No quizzes found for teacher")
            return []
    
    # Pour les admins, montrer tous les résultats
    results = db.query(QuizResult).order_by(QuizResult.created_at.desc()).all()
    print(f"[API] Admin - Found {len(results)} total results")
    return results

@router.get("/enriched/", response_model=List[dict])
def list_enriched_quiz_results(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupérer tous les résultats de quiz avec les informations des étudiants et des quiz"""
    from models.quiz import Quiz
    from models.user import User
    
    # Si c'est un professeur, ne montrer que les résultats des quiz qu'il a créés
    if current_user.role == "teacher":
        teacher_quizzes = db.query(Quiz.id).filter(Quiz.created_by == current_user.id).all()
        quiz_ids = [q.id for q in teacher_quizzes]
        
        if quiz_ids:
            results = db.query(QuizResult).filter(QuizResult.quiz_id.in_(quiz_ids)).order_by(QuizResult.created_at.desc()).all()
        else:
            return []
    else:
        # Pour les admins, montrer tous les résultats
        results = db.query(QuizResult).order_by(QuizResult.created_at.desc()).all()
    
    # Enrichir les résultats avec les informations des étudiants et des quiz
    enriched_results = []
    for result in results:
        # Récupérer les informations de l'étudiant
        student = db.query(User).filter(User.id == result.student_id).first()
        # Récupérer les informations du quiz
        quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
        
        enriched_result = {
            "id": result.id,
            "quiz_id": result.quiz_id,
            "student_id": result.student_id,
            "score": result.score,
            "max_score": result.max_score,
            "percentage": result.percentage,
            "is_completed": result.is_completed,
            "completed_at": result.completed_at,
            "created_at": result.created_at,
            "student": {
                "username": student.username if student else "Inconnu",
                "email": student.email if student else ""
            },
            "quiz": {
                "title": quiz.title if quiz else "Quiz inconnu",
                "subject": quiz.subject if quiz else ""
            }
        }
        enriched_results.append(enriched_result)
    
    return enriched_results

@router.get("/user/{user_id}", response_model=List[QuizResultRead])
def get_user_quiz_results(user_id: int, db: Session = Depends(get_db)):
    """Obtenir tous les résultats de quiz d'un utilisateur."""
    results = db.query(QuizResult).filter(QuizResult.student_id == user_id).order_by(QuizResult.created_at.desc()).all()
    return results

@router.get("/student/{student_id}", response_model=List[QuizResultRead])
def get_student_quiz_results(
    student_id: int, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """Obtenir tous les résultats de quiz d'un étudiant spécifique"""
    print(f"[API] /quiz-results/student/{student_id} - Token user: {current_user.id if current_user else 'None'}")
    print(f"[API] User role: {current_user.role}")
    
    # Vérifier que l'utilisateur a accès à ces données
    if current_user.role == "student" and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé aux données d'un autre étudiant"
        )
    
    # Récupérer les résultats de l'étudiant
    results = db.query(QuizResult).filter(QuizResult.student_id == student_id).order_by(QuizResult.created_at.desc()).all()
    print(f"[API] Found {len(results)} results for student {student_id}")
    
    return results

@router.get("/{result_id}", response_model=QuizResultRead)
def get_quiz_result(result_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = db.query(QuizResult).filter(QuizResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    return result 