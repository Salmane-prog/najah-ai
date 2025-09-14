from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.quiz import Quiz, Question, QuizResult, QuizAnswer, QuizAssignment
from models.user import User, UserRole
from models.class_group import ClassGroup
from schemas.quiz import (
    QuizCreate, QuizRead, QuizUpdate, QuizWithQuestions,
    QuestionCreate, QuestionRead, QuestionUpdate,
    QuizResultCreate, QuizResultRead, QuizResultWithAnswers,
    QuizSubmission, QuizAssignmentCreate, QuizAssignmentRead, QuizAssignmentEnriched
)
from core.security import get_current_user
from api.v1.auth import require_role
from typing import List, Optional
from datetime import datetime
from fastapi.responses import StreamingResponse
import csv
from fpdf import FPDF
from api.v1.notifications_ws import send_notification
from models.class_group import ClassStudent
from schemas.quiz import QuizAnswerRead, QuizResultWithAnswers

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_question_text(question_text: str) -> str:
    """Nettoie le texte de la question pour n'afficher que la question pure."""
    if not question_text:
        return ""
    
    # Chercher la fin de la question (premier point d'interrogation)
    question_end = question_text.find('?')
    if question_end != -1:
        # Retourner seulement la partie jusqu'au point d'interrogation inclus
        return question_text[:question_end + 1]
    
    # Si pas de point d'interrogation, chercher la fin logique
    # Chercher les patterns de réponses (A), B), C), D))
    patterns = ['A)', 'B)', 'C)', 'D)']
    for pattern in patterns:
        pos = question_text.find(pattern)
        if pos != -1:
            return question_text[:pos].strip()
    
    # Si rien trouvé, retourner le texte complet
    return question_text

def extract_options_from_text(question_text: str) -> list:
    """Extrait les options depuis le texte de la question."""
    if not question_text:
        return []
    
    options = []
    # Chercher les patterns A), B), C), D)
    patterns = ['A)', 'B)', 'C)', 'D)']
    
    for i, pattern in enumerate(patterns):
        start = question_text.find(pattern)
        if start != -1:
            # Chercher la fin de cette option (début de la suivante)
            end = len(question_text)
            for next_pattern in patterns[i+1:]:
                next_pos = question_text.find(next_pattern)
                if next_pos != -1 and next_pos > start:
                    end = next_pos
                    break
            
            # Extraire l'option
            option_text = question_text[start:end].strip()
            # Nettoyer l'option (enlever le pattern et les espaces)
            clean_option = option_text.replace(pattern, '').strip()
            options.append(clean_option)
    
    return options

def extract_correct_answer_from_text(question_text: str) -> str:
    """Extrait la réponse correcte depuis le texte de la question."""
    if not question_text:
        return ""
    
    # Chercher "Réponse correcte:"
    correct_start = question_text.find("Réponse correcte:")
    if correct_start != -1:
        # Chercher la fin (explication ou fin du texte)
        explanation_start = question_text.find("Explication:", correct_start)
        if explanation_start != -1:
            correct_answer = question_text[correct_start:explanation_start].strip()
        else:
            correct_answer = question_text[correct_start:].strip()
        
        # Nettoyer
        return correct_answer.replace("Réponse correcte:", "").strip()
    
    return ""

# Quiz CRUD
@router.get("/", response_model=List[QuizRead])
def list_quizzes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    print(f"[DEBUG] list_quizzes: current_user.id={getattr(current_user, 'id', None)}, role={getattr(current_user, 'role', None)}")
    """Lister tous les quiz (professeurs voient les leurs, admins voient tout)."""
    try:
        if current_user.role == UserRole.admin:
            quizzes = db.query(Quiz).all()
        else:
            quizzes = db.query(Quiz).filter(Quiz.created_by == current_user.id).all()
        
        # Au lieu de filtrer les quiz sans created_at, on leur assigne une date par défaut
        for quiz in quizzes:
            if quiz.created_at is None:
                quiz.created_at = datetime.utcnow()
        
        print(f"[DEBUG] Quizzes trouvés pour user {current_user.id}: {[q.id for q in quizzes]}")
        return quizzes
    except Exception as e:
        print(f"[ERROR] Erreur dans list_quizzes: {str(e)}")
        # Retourner une liste vide en cas d'erreur
        return []

@router.get("/teacher/{teacher_id}/completed", response_model=List[QuizResultRead])
def get_teacher_completed_quizzes(teacher_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupère tous les quiz complétés par les étudiants d'un professeur spécifique."""
    # Vérifier que l'utilisateur connecté est le professeur demandé ou un admin
    if current_user.id != teacher_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer tous les quiz créés par ce professeur
    teacher_quizzes = db.query(Quiz.id).filter(Quiz.created_by == teacher_id).all()
    quiz_ids = [q.id for q in teacher_quizzes]
    
    if not quiz_ids:
        return []
    
    # Récupérer tous les résultats de ces quiz
    completed_results = db.query(QuizResult).filter(
        QuizResult.quiz_id.in_(quiz_ids),
        QuizResult.is_completed == True
    ).order_by(QuizResult.completed_at.desc()).all()
    
    print(f"[DEBUG] Quiz complétés trouvés pour teacher {teacher_id}: {[r.id for r in completed_results]}")
    return completed_results

@router.get("/teacher/{teacher_id}", response_model=List[QuizRead])
def get_teacher_quizzes(teacher_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupère tous les quiz créés par un professeur spécifique."""
    # Vérifier que l'utilisateur connecté est le professeur demandé ou un admin
    if current_user.id != teacher_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    quizzes = db.query(Quiz).filter(Quiz.created_by == teacher_id).order_by(Quiz.created_at.desc()).all()
    
    # Au lieu de filtrer les quiz sans created_at, on leur assigne une date par défaut
    for quiz in quizzes:
        if quiz.created_at is None:
            quiz.created_at = datetime.utcnow()
    
    print(f"[DEBUG] Quizzes trouvés pour teacher {teacher_id}: {[q.id for q in quizzes]}")
    return quizzes

@router.post("/", response_model=QuizRead, status_code=201)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Créer un nouveau quiz."""
    db_quiz = Quiz(**quiz.dict(), created_by=current_user.id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.get("/{quiz_id}", response_model=QuizWithQuestions)
def get_quiz(quiz_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Obtenir un quiz avec ses questions."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Vérifier les permissions
    # Les admins peuvent voir tous les quiz
    if current_user.role == UserRole.admin:
        # Nettoyer et formater les questions
        for question in quiz.questions:
            question.question_text = clean_question_text(question.question_text)
            # Si pas d'options définies, les extraire du texte
            if not question.options:
                question.options = extract_options_from_text(question.question_text)
        return quiz
    
    # Les profs peuvent voir tous les quiz (pour les consulter)
    if current_user.role == UserRole.teacher:
        # Nettoyer et formater les questions
        for question in quiz.questions:
            question.question_text = clean_question_text(question.question_text)
            # Si pas d'options définies, les extraire du texte
            if not question.options:
                question.options = extract_options_from_text(question.question_text)
        return quiz
    
    # Les étudiants peuvent voir les quiz qui leur sont assignés
    if current_user.role == UserRole.student:
        # Vérifier si le quiz est assigné à l'étudiant
        assignment = db.query(QuizAssignment).filter(
            QuizAssignment.quiz_id == quiz_id,
            QuizAssignment.student_id == current_user.id
        ).first()
        
        if assignment:
            # Nettoyer et formater les questions
            for question in quiz.questions:
                question.question_text = clean_question_text(question.question_text)
                # Si pas d'options définies, les extraire du texte
                if not question.options:
                    question.options = extract_options_from_text(question.question_text)
            return quiz
        else:
            raise HTTPException(status_code=403, detail="Quiz not assigned to you")
    
    raise HTTPException(status_code=403, detail="Not authorized")

@router.put("/{quiz_id}", response_model=QuizRead)
def update_quiz(quiz_id: int, quiz_update: QuizUpdate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Mettre à jour un quiz."""
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Vérifier les permissions
    if current_user.role != UserRole.admin and db_quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in quiz_update.dict(exclude_unset=True).items():
        setattr(db_quiz, field, value)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.delete("/{quiz_id}", status_code=204)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Supprimer un quiz."""
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Vérifier les permissions
    if current_user.role not in ["admin"] and db_quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_quiz)
    db.commit()
    return None

# Questions CRUD
@router.post("/{quiz_id}/questions", response_model=QuestionRead, status_code=201)
def add_question(quiz_id: int, question: QuestionCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Ajouter une question à un quiz."""
    # Vérifier que le quiz existe et appartient au professeur
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if current_user.role not in ["admin"] and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_question = Question(**question.dict(), quiz_id=quiz_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # Mettre à jour le total des points du quiz
    total_points = sum(q.points for q in quiz.questions)
    quiz.total_points = total_points
    db.commit()
    
    return db_question

@router.put("/questions/{question_id}", response_model=QuestionRead)
def update_question(question_id: int, question_update: QuestionUpdate, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Mettre à jour une question."""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Vérifier les permissions
    quiz = db.query(Quiz).filter(Quiz.id == db_question.quiz_id).first()
    if current_user.role not in ["admin"] and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in question_update.dict(exclude_unset=True).items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    
    # Mettre à jour le total des points du quiz
    total_points = sum(q.points for q in quiz.questions)
    quiz.total_points = total_points
    db.commit()
    
    return db_question

@router.delete("/questions/{question_id}", status_code=204)
def delete_question(question_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Supprimer une question."""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Vérifier les permissions
    quiz = db.query(Quiz).filter(Quiz.id == db_question.quiz_id).first()
    if current_user.role not in ["admin"] and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_question)
    db.commit()
    
    # Mettre à jour le total des points du quiz
    total_points = sum(q.points for q in quiz.questions)
    quiz.total_points = total_points
    db.commit()
    
    return None

# Quiz Results
@router.get("/{quiz_id}/results", response_model=List[QuizResultRead])
def get_quiz_results(quiz_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['teacher', 'admin']))):
    """Obtenir les résultats d'un quiz."""
    # Vérifier que le quiz existe et appartient au professeur
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if current_user.role not in ["admin"] and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return db.query(QuizResult).filter(QuizResult.quiz_id == quiz_id).all()

@router.get("/results/{result_id}", response_model=QuizResultWithAnswers)
def get_quiz_result_detail(result_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Obtenir les détails d'un résultat de quiz avec les réponses."""
    print(f"[DEBUG] get_quiz_result_detail appelé pour result_id={result_id}, user_id={current_user.id}, role={current_user.role}")
    
    result = db.query(QuizResult).filter(QuizResult.id == result_id).first()
    if not result:
        print(f"[DEBUG] Résultat non trouvé pour result_id={result_id}")
        raise HTTPException(status_code=404, detail="Quiz result not found")
    
    print(f"[DEBUG] Résultat trouvé: quiz_id={result.quiz_id}, student_id={result.student_id}, score={result.score}")
    
    quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
    if not quiz:
        print(f"[DEBUG] Quiz non trouvé pour quiz_id={result.quiz_id}")
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    print(f"[DEBUG] Quiz trouvé: title={quiz.title}, created_by={quiz.created_by}")
    
    # Les étudiants peuvent voir leurs propres résultats
    if current_user.role == "student" and result.student_id == current_user.id:
        print(f"[DEBUG] Accès autorisé pour étudiant")
        # Récupérer les réponses avec les détails
        answers = []
        for answer in result.quiz_answers:
            # Créer un objet QuizAnswerRead avec les données
            answer_data = {
                "id": answer.id,
                "result_id": answer.result_id,
                "question_id": answer.question_id,
                "student_answer": answer.answer_text or "Aucune réponse",
                "is_correct": answer.is_correct,
                "points_earned": answer.points_earned or 0,
                "correct_answer": getattr(answer, 'correct_answer', None) or "Réponse correcte non disponible"
            }
            
            # Si correct_answer n'est pas défini, essayer de le récupérer depuis la question
            correct_answer_value = getattr(answer, 'correct_answer', None)
            if not correct_answer_value or correct_answer_value == "Réponse correcte non disponible":
                question = db.query(Question).filter(Question.id == answer.question_id).first()
                if question:
                    print(f"[DEBUG] Traitement réponse {len(answers)+1}: question_id={answer.question_id}")
                    print(f"[DEBUG] Question trouvée: type={question.question_type}, correct_answer={question.correct_answer}")
                    
                    if question.question_type == "mcq":
                        # Pour les QCM, récupérer la bonne option
                        options = question.options or extract_options_from_text(question.question_text)
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] QCM: options={options}, correct_answer={correct_answer}")
                        
                        # Gérer les différents types de correct_answer
                        if isinstance(correct_answer, int):
                            # Si c'est un index numérique
                            if 0 <= correct_answer < len(options):
                                answer_data["correct_answer"] = options[correct_answer]
                                print(f"[DEBUG] Réponse correcte (index): {answer_data['correct_answer']}")
                            else:
                                answer_data["correct_answer"] = "Réponse correcte non disponible"
                                print(f"[DEBUG] Index invalide: {correct_answer} >= {len(options)}")
                        elif isinstance(correct_answer, str):
                            # Si c'est déjà une chaîne (réponse directe)
                            answer_data["correct_answer"] = correct_answer
                            print(f"[DEBUG] Réponse correcte (directe): {answer_data['correct_answer']}")
                        else:
                            # Essayer d'extraire depuis le texte de la question
                            extracted_answer = extract_correct_answer_from_text(question.question_text)
                            if extracted_answer:
                                answer_data["correct_answer"] = extracted_answer
                                print(f"[DEBUG] Réponse correcte (extraite): {answer_data['correct_answer']}")
                            else:
                                answer_data["correct_answer"] = "Réponse correcte non disponible"
                                print(f"[DEBUG] Type non géré: {type(correct_answer)}")
                            
                            # Sauvegarder dans la base de données
                            answer.correct_answer = answer_data["correct_answer"]
                            db.commit()
                                
                    elif question.question_type == "true_false":
                        # Pour Vrai/Faux
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] Vrai/Faux: correct_answer={correct_answer}")
                        if isinstance(correct_answer, bool):
                            answer_data["correct_answer"] = "Vrai" if correct_answer else "Faux"
                        elif isinstance(correct_answer, str):
                            answer_data["correct_answer"] = correct_answer
                        else:
                            answer_data["correct_answer"] = "Réponse correcte non disponible"
                        
                        # Sauvegarder dans la base de données
                        answer.correct_answer = answer_data["correct_answer"]
                        db.commit()
                    else:
                        # Pour les questions texte
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] Texte: correct_answer={correct_answer}")
                        if isinstance(correct_answer, str):
                            answer_data["correct_answer"] = correct_answer
                        else:
                            answer_data["correct_answer"] = "Réponse correcte non disponible"
                        
                        # Sauvegarder dans la base de données
                        answer.correct_answer = answer_data["correct_answer"]
                        db.commit()
                else:
                    print(f"[DEBUG] Question non trouvée pour question_id={answer.question_id}")
            
            answers.append(QuizAnswerRead(**answer_data))
        
        # Créer un objet de réponse avec les données
        result_data = {
            "id": result.id,
            "student_id": result.student_id,
            "quiz_id": result.quiz_id,
            "sujet": result.sujet,
            "score": result.score,
            "completed": result.is_completed,  # Utiliser is_completed au lieu de completed
            "created_at": result.created_at,
            "max_score": result.max_score,
            "percentage": result.percentage,
            "started_at": getattr(result, 'started_at', None),  # Utiliser getattr pour éviter l'erreur
            "completed_at": result.completed_at,
            "is_completed": result.is_completed,
            "answers": answers
        }
        
        return QuizResultWithAnswers(**result_data)
    
    # Les professeurs peuvent voir les résultats de leurs quiz
    if current_user.role == "teacher" and quiz.created_by == current_user.id:
        print(f"[DEBUG] Accès autorisé pour professeur")
        # Récupérer les réponses avec les détails
        answers = []
        for answer in result.quiz_answers:
            # Créer un objet QuizAnswerRead avec les données
            answer_data = {
                "id": answer.id,
                "result_id": answer.result_id,
                "question_id": answer.question_id,
                "student_answer": answer.answer_text or "Aucune réponse",
                "is_correct": answer.is_correct,
                "points_earned": answer.points_earned or 0,
                "correct_answer": getattr(answer, 'correct_answer', None) or "Réponse correcte non disponible"
            }
            
            # Si correct_answer n'est pas défini, essayer de le récupérer depuis la question
            correct_answer_value = getattr(answer, 'correct_answer', None)
            if not correct_answer_value or correct_answer_value == "Réponse correcte non disponible":
                question = db.query(Question).filter(Question.id == answer.question_id).first()
                if question:
                    print(f"[DEBUG] Traitement réponse {len(answers)+1}: question_id={answer.question_id}")
                    print(f"[DEBUG] Question trouvée: type={question.question_type}, correct_answer={question.correct_answer}")
                    
                    if question.question_type == "mcq":
                        # Pour les QCM, récupérer la bonne option
                        options = question.options or extract_options_from_text(question.question_text)
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] QCM: options={options}, correct_answer={correct_answer}")
                        
                        # Gérer les différents types de correct_answer
                        if isinstance(correct_answer, int):
                            # Si c'est un index numérique
                            if 0 <= correct_answer < len(options):
                                answer_data["correct_answer"] = options[correct_answer]
                                print(f"[DEBUG] Réponse correcte (index): {answer_data['correct_answer']}")
                            else:
                                answer_data["correct_answer"] = "Réponse correcte non disponible"
                                print(f"[DEBUG] Index invalide: {correct_answer} >= {len(options)}")
                        elif isinstance(correct_answer, str):
                            # Si c'est déjà une chaîne (réponse directe)
                            answer_data["correct_answer"] = correct_answer
                            print(f"[DEBUG] Réponse correcte (directe): {answer_data['correct_answer']}")
                        else:
                            # Essayer d'extraire depuis le texte de la question
                            extracted_answer = extract_correct_answer_from_text(question.question_text)
                            if extracted_answer:
                                answer_data["correct_answer"] = extracted_answer
                                print(f"[DEBUG] Réponse correcte (extraite): {answer_data['correct_answer']}")
                            else:
                                answer_data["correct_answer"] = "Réponse correcte non disponible"
                                print(f"[DEBUG] Type non géré: {type(correct_answer)}")
                            
                            # Sauvegarder dans la base de données
                            answer.correct_answer = answer_data["correct_answer"]
                            db.commit()
                                
                    elif question.question_type == "true_false":
                        # Pour Vrai/Faux
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] Vrai/Faux: correct_answer={correct_answer}")
                        if isinstance(correct_answer, bool):
                            answer_data["correct_answer"] = "Vrai" if correct_answer else "Faux"
                        elif isinstance(correct_answer, str):
                            answer_data["correct_answer"] = correct_answer
                        else:
                            answer_data["correct_answer"] = "Réponse correcte non disponible"
                        
                        # Sauvegarder dans la base de données
                        answer.correct_answer = answer_data["correct_answer"]
                        db.commit()
                    else:
                        # Pour les questions texte
                        correct_answer = question.correct_answer
                        print(f"[DEBUG] Texte: correct_answer={correct_answer}")
                        if isinstance(correct_answer, str):
                            answer_data["correct_answer"] = correct_answer
                        else:
                            answer_data["correct_answer"] = "Réponse correcte non disponible"
                        
                        # Sauvegarder dans la base de données
                        answer.correct_answer = answer_data["correct_answer"]
                        db.commit()
                else:
                    print(f"[DEBUG] Question non trouvée pour question_id={answer.question_id}")
            
            answers.append(QuizAnswerRead(**answer_data))
        
        # Créer un objet de réponse avec les données
        result_data = {
            "id": result.id,
            "student_id": result.student_id,
            "quiz_id": result.quiz_id,
            "sujet": result.sujet,
            "score": result.score,
            "completed": result.is_completed,  # Utiliser is_completed au lieu de completed
            "created_at": result.created_at,
            "max_score": result.max_score,
            "percentage": result.percentage,
            "started_at": getattr(result, 'started_at', None),  # Utiliser getattr pour éviter l'erreur
            "completed_at": result.completed_at,
            "is_completed": result.is_completed,
            "answers": answers
        }
        
        return QuizResultWithAnswers(**result_data)
    
    # Les admins peuvent voir tous les résultats
    if current_user.role == "admin":
        # Récupérer les réponses avec les bonnes réponses
        answers = db.query(QuizAnswer).filter(QuizAnswer.result_id == result_id).all()
        
        # Pour chaque réponse, ajouter la bonne réponse
        for answer in answers:
            question = db.query(Question).filter(Question.id == answer.question_id).first()
            if question:
                if question.question_type == "mcq":
                    # Pour les QCM, récupérer la bonne option
                    options = question.options or []
                    correct_answer = question.correct_answer
                    
                    # Gérer les différents types de correct_answer
                    if isinstance(correct_answer, int):
                        # Si c'est un index numérique
                        if 0 <= correct_answer < len(options):
                            answer.correct_answer = options[correct_answer]
                        else:
                            answer.correct_answer = "Réponse correcte non disponible"
                    elif isinstance(correct_answer, str):
                        # Si c'est déjà une chaîne (réponse directe)
                        answer.correct_answer = correct_answer
                    else:
                        # Si c'est None ou autre type
                        answer.correct_answer = "Réponse correcte non disponible"
                        
                elif question.question_type == "true_false":
                    # Pour Vrai/Faux
                    correct_answer = question.correct_answer
                    if isinstance(correct_answer, bool):
                        answer.correct_answer = "Vrai" if correct_answer else "Faux"
                    elif isinstance(correct_answer, str):
                        answer.correct_answer = correct_answer
                    else:
                        answer.correct_answer = "Réponse correcte non disponible"
                else:
                    # Pour les questions texte
                    correct_answer = question.correct_answer
                    if isinstance(correct_answer, str):
                        answer.correct_answer = correct_answer
                    else:
                        answer.correct_answer = "Réponse correcte non disponible"
        
        result.answers = answers
        return result
    
    raise HTTPException(status_code=403, detail="Not authorized")

# Submit Quiz (pour les élèves)
@router.post("/{quiz_id}/submit", response_model=QuizResultRead)
def submit_quiz(quiz_id: int, submission: QuizSubmission, db: Session = Depends(get_db), current_user=Depends(require_role(['student']))):
    """Soumettre un quiz (pour les élèves)."""
    print(f"[DEBUG] submit_quiz appelée pour quiz_id={quiz_id}, user_id={current_user.id}")
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found or inactive")
    
    # Vérifier si l'élève a déjà commencé ce quiz
    existing_result = db.query(QuizResult).filter(
        QuizResult.quiz_id == quiz_id,
        QuizResult.student_id == current_user.id
    ).first()
    
    print(f"[DEBUG] Existing result found: {existing_result is not None}")
    if existing_result and existing_result.is_completed:
        print(f"[DEBUG] Quiz already completed, raising 400 error")
        raise HTTPException(status_code=400, detail="Quiz already completed")
    
    print(f"[DEBUG] Proceeding with quiz submission")
    
    # Créer ou récupérer le résultat
    if not existing_result:
        result = QuizResult(
            user_id=current_user.id,  # Ajouter le user_id manquant
            quiz_id=quiz_id,
            student_id=current_user.id,
            max_score=quiz.max_score,
            score=0,
            percentage=0,
            is_completed=False,
            sujet=quiz.subject,
            created_at=datetime.utcnow()
        )
        db.add(result)
        db.commit()
        db.refresh(result)
    else:
        result = existing_result
    
    # Traiter les réponses
    score = 0
    for answer_data in submission.answers:
        question = db.query(Question).filter(Question.id == answer_data["question_id"]).first()
        if not question:
            continue
        
        # Créer la réponse
        quiz_answer = QuizAnswer(
            result_id=result.id,
            question_id=question.id,
            answer_text=str(answer_data["answer"])
        )
        
        # Évaluer la réponse
        is_correct = False
        points_earned = 0
        
        if question.question_type == "mcq":
            # Récupérer les options et la réponse correcte
            options = question.options or []
            correct_answer = question.correct_answer
            
            # Déterminer la réponse correcte textuelle
            correct_text = ""
            if isinstance(correct_answer, int) and 0 <= correct_answer < len(options):
                correct_text = options[correct_answer]
            elif isinstance(correct_answer, str):
                correct_text = correct_answer
            else:
                # Essayer d'extraire depuis le texte de la question
                correct_text = extract_correct_answer_from_text(question.question_text) or ""
            
            # Comparer avec la réponse de l'étudiant
            student_answer = str(answer_data["answer"])
            is_correct = student_answer.strip().lower() == correct_text.strip().lower()
            
            print(f"[DEBUG] QCM Scoring - Question {question.id}:")
            print(f"  Student answer: '{student_answer}'")
            print(f"  Correct text: '{correct_text}'")
            print(f"  Is correct: {is_correct}")
            
        elif question.question_type == "true_false":
            is_correct = str(answer_data["answer"]).lower() == str(question.correct_answer).lower()
        elif question.question_type == "text":
            # Pour les questions texte, on peut faire une comparaison simple
            is_correct = str(answer_data["answer"]).strip().lower() == str(question.correct_answer).strip().lower()
        
        if is_correct:
            points_earned = question.points
            score += question.points
        
        quiz_answer.is_correct = is_correct
        quiz_answer.points_earned = points_earned
        
        # Ajouter la réponse correcte pour l'affichage
        if question.question_type == "mcq":
            options = question.options or []
            correct_answer = question.correct_answer
            if isinstance(correct_answer, int) and 0 <= correct_answer < len(options):
                quiz_answer.correct_answer = options[correct_answer]
            elif isinstance(correct_answer, str):
                quiz_answer.correct_answer = correct_answer
            else:
                quiz_answer.correct_answer = extract_correct_answer_from_text(question.question_text) or "Réponse correcte non disponible"
        elif question.question_type == "true_false":
            if isinstance(question.correct_answer, bool):
                quiz_answer.correct_answer = "Vrai" if question.correct_answer else "Faux"
            else:
                quiz_answer.correct_answer = str(question.correct_answer)
        else:
            quiz_answer.correct_answer = str(question.correct_answer)
        
        db.add(quiz_answer)
    
    # Mettre à jour le résultat
    result.score = score
    result.percentage = (score / quiz.max_score * 100) if quiz.max_score > 0 else 0
    result.is_completed = True
    result.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(result)
    
    print(f"[DEBUG] Quiz submitted successfully, score: {score}")
    return result

@router.post("/assign/", response_model=QuizAssignmentRead)
def assign_quiz(assignment: QuizAssignmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Assigner un quiz à une classe ou un étudiant."""
    print(f"🔧 Tentative d'assignation: quiz_id={assignment.quiz_id}, class_id={assignment.class_id}, student_id={assignment.student_id}")
    
    # Vérifier que le quiz existe
    quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
    if not quiz:
        print(f"❌ Quiz {assignment.quiz_id} non trouvé")
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    print(f"✅ Quiz trouvé: {quiz.title}")
    
    # Vérifier que la classe existe si spécifiée
    if assignment.class_id:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == assignment.class_id).first()
        if not class_group:
            print(f"❌ Classe {assignment.class_id} non trouvée")
            raise HTTPException(status_code=404, detail="Class not found")
        print(f"✅ Classe trouvée: {class_group.name}")
    
    # Vérifier que l'étudiant existe si spécifié
    if assignment.student_id:
        student = db.query(User).filter(User.id == assignment.student_id).first()
        if not student:
            print(f"❌ Étudiant {assignment.student_id} non trouvé")
            raise HTTPException(status_code=404, detail="Student not found")
        print(f"✅ Étudiant trouvé: {student.email}")
    
    # Créer l'assignation
    assignment_data = assignment.dict()
    assignment_data['assigned_by'] = current_user.id  # Ajouter l'ID de l'utilisateur actuel
    
    qa = QuizAssignment(**assignment_data)
    db.add(qa)
    db.commit()
    db.refresh(qa)
    
    print(f"✅ Assignation créée avec succès: ID={qa.id}")
    
    # Envoyer des notifications temps réel
    try:
        if assignment.student_id:
            send_notification(assignment.student_id, f"Nouveau quiz '{quiz.title}' à faire !")
            print(f"📢 Notification envoyée à l'étudiant {assignment.student_id}")
        elif assignment.class_id:
            students = db.query(User).join(ClassStudent, User.id == ClassStudent.student_id).filter(ClassStudent.class_id == assignment.class_id).all()
            for s in students:
                send_notification(s.id, f"Nouveau quiz '{quiz.title}' à faire !")
            print(f"📢 Notifications envoyées à {len(students)} étudiants de la classe {assignment.class_id}")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'envoi des notifications: {e}")
    
    return qa

@router.get("/assigned/")
def get_assigned_quizzes(class_id: Optional[int] = None, student_id: Optional[int] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupérer les quiz assignés avec les détails du quiz."""
    query = db.query(QuizAssignment)
    if class_id:
        query = query.filter(QuizAssignment.class_id == class_id)
    if student_id:
        query = query.filter(QuizAssignment.student_id == student_id)
    
    assignments = query.all()
    
    # Enrichir avec les détails du quiz
    enriched_assignments = []
    for assignment in assignments:
        quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
        if quiz:
            # Créer un objet enrichi avec les détails du quiz
            enriched_assignment = {
                "id": assignment.id,
                "quiz_id": assignment.quiz_id,
                "class_id": assignment.class_id,
                "student_id": assignment.student_id,
                "assigned_at": assignment.created_at,  # Utiliser created_at au lieu de assigned_at
                "due_date": assignment.due_date,
                "quiz": {
                    "id": quiz.id,
                    "title": quiz.title,
                    "description": quiz.description,
                    "subject": quiz.subject,
                    "level": quiz.level,
                    "time_limit": quiz.time_limit,
                    "max_score": quiz.max_score,  # Utiliser max_score au lieu de total_points
                    "questions": [
                        {
                            "id": q.id,
                            "question_text": q.question_text,
                            "question_type": q.question_type,
                            "points": q.points,
                            "options": q.options
                        } for q in quiz.questions
                    ]
                }
            }
            enriched_assignments.append(enriched_assignment)
    
    return enriched_assignments

@router.get("/assigned/{student_id}")
def get_assigned_quizzes(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupérer les quiz assignés à un étudiant spécifique."""
    
    # Vérifier l'accès
    if current_user.id != student_id and current_user.role not in ['teacher', 'admin']:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    query = db.query(QuizAssignment).filter(QuizAssignment.student_id == student_id)
    assignments = query.all()
    
    # Enrichir avec les détails du quiz
    enriched_assignments = []
    for assignment in assignments:
        quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
        if quiz:
            # Créer un objet enrichi avec les détails du quiz
            enriched_assignment = {
                "id": assignment.id,
                "quiz_id": assignment.quiz_id,
                "class_id": assignment.class_id,
                "student_id": assignment.student_id,
                "assigned_at": assignment.created_at,  # Utiliser created_at au lieu de assigned_at
                "due_date": assignment.due_date,
                "quiz": {
                    "id": quiz.id,
                    "title": quiz.title,
                    "description": quiz.description,
                    "subject": quiz.subject,
                    "level": quiz.level,
                    "time_limit": quiz.time_limit,
                    "max_score": quiz.max_score,  # Utiliser max_score au lieu de total_points
                    "questions": [
                        {
                            "id": q.id,
                            "question_text": q.question_text,
                            "question_type": q.question_type,
                            "points": q.points,
                            "options": q.options
                        } for q in quiz.questions
                    ]
                }
            }
            enriched_assignments.append(enriched_assignment)
    
    return enriched_assignments

@router.get("/{quiz_id}/export")
def export_quiz(quiz_id: int, format: str = 'pdf', db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = quiz.questions
    if format == 'csv':
        def csv_generator():
            output = []
            writer = csv.writer(output)
            writer.writerow(["Question", "Options", "Réponse"])
            for q in questions:
                opts = ", ".join(q.options or [])
                writer.writerow([q.question_text, opts, q.correct_answer])
            for row in output:
                yield ','.join(map(str, row)) + '\n'
        headers = {"Content-Disposition": f"attachment; filename=quiz_{quiz_id}.csv"}
        return StreamingResponse(csv_generator(), media_type="text/csv", headers=headers)
    if format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Quiz : {quiz.title}', ln=1, align='C')
        pdf.set_font('Arial', '', 12)
        for idx, q in enumerate(questions, 1):
            pdf.multi_cell(0, 8, f"{idx}. {q.question_text}")
            if q.options:
                for opt in q.options:
                    pdf.cell(0, 8, f"- {opt}", ln=1)
            pdf.cell(0, 8, f"Réponse : {q.correct_answer}", ln=1)
            pdf.ln(2)
        pdf_output = pdf.output(dest='S').encode('latin1')
        headers = {"Content-Disposition": f"attachment; filename=quiz_{quiz_id}.pdf"}
        return StreamingResponse(iter([pdf_output]), media_type="application/pdf", headers=headers)
    raise HTTPException(status_code=400, detail="Format non supporté") 

@router.get("/{quiz_id}/start")
def start_quiz(quiz_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = quiz.questions
    return {
        "quiz_id": quiz.id,
        "title": quiz.title,
        "questions": [
            {
                "id": q.id,
                "question": q.question_text,
                "choices": q.options or [],
                "type": q.question_type
            } for q in questions
        ]
    }

@router.post("/{quiz_id}/submit-simple")
def submit_quiz_simple(quiz_id: int, answers: List[dict], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = {q.id: q for q in quiz.questions}
    score = 0
    max_score = 0
    corrections = []
    for ans in answers:
        qid = ans.get("question_id")
        student_answer = ans.get("answer")
        q = questions.get(qid)
        if not q:
            continue
        correct = False
        if q.question_type == 'mcq':
            correct = (student_answer == q.correct_answer)
        elif q.question_type == 'text':
            correct = (student_answer.strip().lower() == str(q.correct_answer).strip().lower())
        pts = q.points if correct else 0
        score += pts
        max_score += q.points
        corrections.append({
            "question": q.question_text,
            "student_answer": student_answer,
            "correct_answer": q.correct_answer,
            "is_correct": correct,
            "points": pts
        })
    percent = (score / max_score * 100) if max_score else 0
    # Enregistrer le résultat (optionnel)
    result = QuizResult(student_id=current_user.id, quiz_id=quiz.id, score=score, max_score=max_score, percentage=percent, is_completed=True, sujet=quiz.subject)
    db.add(result)
    db.commit()
    db.refresh(result)
    return {
        "score": score,
        "max_score": max_score,
        "percentage": percent,
        "corrections": corrections
    }

@router.get("/{quiz_id}/results")
def quiz_results(quiz_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    results = db.query(QuizResult).filter(QuizResult.quiz_id == quiz_id).all()
    return [
        {
            "student_id": r.user_id,
            "score": r.score,
            "percentage": r.percentage,
            "completed_at": r.completed_at
        } for r in results
    ]

# Endpoint de test pour lister tous les quiz disponibles
@router.get("/list/all")
def list_all_quizzes(db: Session = Depends(get_db)):
    """Liste tous les quiz disponibles (pour debug)"""
    quizzes = db.query(Quiz).all()
    return [
        {
            "id": q.id,
            "title": q.title,
            "subject": q.subject,
            "description": q.description,
            "total_questions": len(q.questions) if q.questions else 0
        } for q in quizzes
    ]

# Endpoint de test pour créer un quiz simple
@router.post("/create-test")
def create_test_quiz(db: Session = Depends(get_db)):
    """Créer un quiz de test simple (pour debug)"""
    try:
        # Créer un quiz de test
        test_quiz = Quiz(
            title="Quiz de Test - Français",
            subject="Français",
            description="Quiz de test pour vérifier le fonctionnement du système",
            time_limit=15,
            difficulty="medium",
            created_by=1
        )
        db.add(test_quiz)
        db.flush()  # Pour obtenir l'ID
        
        # Créer des questions de test
        questions_data = [
            {
                "question_text": "Quelle est la capitale de la France?",
                "options": ["Londres", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris",
                "question_type": "mcq",
                "points": 10
            },
            {
                "question_text": "Combien de voyelles y a-t-il dans l'alphabet français?",
                "options": ["4", "5", "6", "7"],
                "correct_answer": "6",
                "question_type": "mcq",
                "points": 10
            }
        ]
        
        for q_data in questions_data:
            question = Question(
                question_text=q_data["question_text"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                question_type=q_data["question_type"],
                points=q_data["points"],
                quiz_id=test_quiz.id
            )
            db.add(question)
        
        db.commit()
        
        # Assigner le quiz à l'étudiant avec l'ID 33 (utilisateur de test)
        from models.quiz import QuizAssignment
        assignment = QuizAssignment(
            quiz_id=test_quiz.id,
            student_id=33,  # ID de l'étudiant de test
            assigned_by=1,  # ID du professeur de test
            due_date=datetime.now(),
            status='assigned'
        )
        db.add(assignment)
        db.commit()
        
        return {
            "message": "Quiz de test créé et assigné avec succès",
            "quiz_id": test_quiz.id,
            "title": test_quiz.title,
            "questions_count": len(questions_data),
            "assigned_to_student": 33
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du quiz de test: {str(e)}") 