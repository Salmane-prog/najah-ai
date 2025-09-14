from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Optional
import os, json, random
from models.quiz import Quiz, Question, QuizResult  # Ajout de QuizResult
from models.learning_path import LearningPath
from models.content import Content
from sqlalchemy.orm import Session
from core.database import SessionLocal
from api.v1.users import get_current_user
import openai
from core.config import settings
import re
from api.v1.auth import get_db
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import csv
from fpdf import FPDF
from models.user import User
from models.learning_history import LearningHistory
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta

router = APIRouter()

class RecommendRequest(BaseModel):
    user_id: int

class AnalyticsRequest(BaseModel):
    user_id: int
    periode: Optional[str] = None
    type_analyse: Optional[str] = None

QCM_PATHS = {
    "antigone": "data/qcm/Antigone/antigone_training_data.json",
    "la_boite_a_merveilles": "data/qcm/La_Boite/training_data_V4.json",
    "dernier_jour_d_un_condamne": "data/qcm/Le_Dernier_Jour/training_data_V1.json"
}

import os
# BASE_DIR doit pointer vers le répertoire racine du projet, pas vers backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@router.get("/test/")
def test_endpoint():
    """Endpoint de test très simple"""
    return {"message": "API accessible", "status": "ok"}

@router.post("/generate-qcm-test/")
def generate_qcm_test(
    sujet: str = Body(...),
    niveau: Optional[str] = Body(None),
    nombre: int = Body(5),
    type_qcm: Optional[str] = Body(None),
    chapitre: Optional[str] = Body(None),
    scene: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """Endpoint de test sans authentification pour diagnostiquer"""
    print(f"[DEBUG] Test endpoint appelé avec: sujet={sujet}, niveau={niveau}, nombre={nombre}")
    
    sujet_key = sujet.lower().replace(" ", "_")
    if sujet_key not in QCM_PATHS:
        raise HTTPException(status_code=404, detail="Sujet non disponible")
    path = os.path.join(BASE_DIR, QCM_PATHS[sujet_key])
    print("Chemin QCM utilisé :", path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier QCM introuvable")
    
    # Retourner une réponse simple pour tester
    return {
        "quiz_id": 999,
        "title": f"Quiz test - {sujet}",
        "questions": [
            {
                "id": 1,
                "question_text": "Question de test",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A"
            }
        ]
    }

@router.post("/generate-qcm/")
def generate_qcm(
    sujet: str = Body(...),
    niveau: Optional[str] = Body(None),
    nombre: int = Body(5),
    type_qcm: Optional[str] = Body(None),
    chapitre: Optional[str] = Body(None),
    scene: Optional[str] = Body(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_role(['teacher', 'admin']))  # Ajouter l'authentification
):
    """Endpoint principal pour générer des QCM - avec authentification"""
    print(f"[DEBUG] Endpoint principal appelé avec: sujet={sujet}, niveau={niveau}, nombre={nombre}")
    print(f"[DEBUG] Utilisateur connecté: {current_user.id} ({current_user.email})")
    
    sujet_key = sujet.lower().replace(" ", "_")
    if sujet_key not in QCM_PATHS:
        raise HTTPException(status_code=404, detail="Sujet non disponible")
    path = os.path.join(BASE_DIR, QCM_PATHS[sujet_key])
    print("Chemin QCM utilisé :", path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier QCM introuvable")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    # Adapter selon le format du fichier
    if "dataset_entrainement_enrichi" in data:
        questions = data["dataset_entrainement_enrichi"]
    elif "dataset_entrainement_complet" in data:
        questions = data["dataset_entrainement_complet"]
    else:
        raise HTTPException(status_code=404, detail="Format de fichier non reconnu")
    print(f"[DEBUG] Nombre de questions après chargement JSON : {len(questions)}")
    if niveau and niveau.lower() != 'toutes':
        questions = [q for q in questions if q.get("difficulte") and q.get("difficulte").lower() == niveau.lower()]
    print(f"[DEBUG] Après filtre difficulté : {len(questions)}")
    if type_qcm:
        questions = [q for q in questions if q.get("type") == type_qcm]
    if chapitre:
        questions = [q for q in questions if str(q.get("chapitre")) == str(chapitre)]
    
    # Garde une copie avant de filtrer par scène
    questions_before_scene_filter = questions[:]

    if scene:
        questions = [q for q in questions if str(q.get("section")) == str(scene)]
    print(f"[DEBUG] Après filtre scène : {len(questions)}")
    if not questions:
        questions = questions_before_scene_filter
        print(f"[DEBUG] Aucun résultat pour la scène, retour à la liste avant filtre scène : {len(questions)}")

    # Filtrer pour ne garder que les QCM avec des choix non vides
    # Ancien code : questions = [q for q in questions if q.get("type") in ["mcq", "qcm"] and q.get("choices") and len(q.get("choices")) > 0]
    # Nouveau : accepte tout type si choix et bonne réponse
    questions = [q for q in questions if q.get("choices") and len(q.get("choices")) > 0 or True]  # ce filtre sera remplacé par le parsing plus bas
    
    def extract_choices_and_answer(texte_cible):
        import re
        # Extraire les lignes de choix (A), B), ...)
        choices = re.findall(r'^[A-D]\)\s.*', texte_cible, re.MULTILINE)
        choices_clean = [re.sub(r'^[A-D]\)\s', '', c).strip() for c in choices]
        # Essayer plusieurs formats pour la réponse correcte
        m = re.search(r'Réponse correcte\s*:\s*([A-D])\)', texte_cible)
        if not m:
            m = re.search(r'Réponse correcte\s*:\s*([A-D])', texte_cible)
        correct_answer = None
        if m:
            idx = ord(m.group(1)) - ord('A')
            if 0 <= idx < len(choices_clean):
                correct_answer = choices_clean[idx]
        return choices_clean, correct_answer

    # Debug : afficher le parsing pour les 3 premières questions
    for i, q in enumerate(questions[:3]):
        texte_cible = q.get("texte_cible", "")
        choices, correct_answer = extract_choices_and_answer(texte_cible)
        print(f"[DEBUG] Q{i+1} - choices: {choices}, correct_answer: {correct_answer}")

    # Adapter la sélection des questions QCM
    qcm_questions = []
    for q in questions:
        texte_cible = q.get("texte_cible", "")
        choices, correct_answer = extract_choices_and_answer(texte_cible)
        if len(choices) >= 2 and correct_answer:
            qcm_questions.append({
                **q,
                "choices": choices,
                "correct_answer": correct_answer
            })
    print(f"[DEBUG] Nombre de QCM détectés : {len(qcm_questions)}")
    if not qcm_questions:
        raise HTTPException(status_code=404, detail="Aucune question QCM détectée dans le fichier JSON")
    selected = random.sample(qcm_questions, min(nombre, len(qcm_questions)))

    # 1. Créer le quiz en base
    quiz = Quiz(
        title=f"Quiz généré - {sujet}",
        description=f"Quiz généré automatiquement sur {sujet}",
        subject=sujet,
        level=niveau or "medium",
        created_by=current_user.id,  # Utiliser l'ID de l'utilisateur connecté
        time_limit=15,
        max_score=len(selected) * 1
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    # 2. Créer chaque question en base
    question_objs = []
    for idx, q in enumerate(selected):
        question = Question(
            quiz_id=quiz.id,
            question_text=q.get("texte_cible", ""),
            question_type="mcq",
            points=1,
            order=idx + 1,
            options=q.get("choices", []),
            correct_answer=q.get("correct_answer", "")
        )
        db.add(question)
        question_objs.append(question)
    db.commit()

    # 3. Retourner l'id du quiz et les questions
    return {
        "quiz_id": quiz.id,
        "title": quiz.title,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer
            }
            for q in question_objs
        ]
    }

@router.post("/recommend/")
def recommend(
    request: RecommendRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    authorization: str = Depends(lambda: None)
):
    import fastapi
    from fastapi import Request
    # Ajout du log du header Authorization
    import inspect
    frame = inspect.currentframe()
    try:
        request_obj = None
        for f in inspect.stack():
            if 'request' in f.frame.f_locals:
                request_obj = f.frame.f_locals['request']
                break
        if request_obj:
            print(f"[DEBUG] Authorization header: {request_obj.headers.get('authorization')}")
    except Exception as e:
        print(f"[DEBUG] Impossible d'afficher le header Authorization: {e}")
    print(f"[API] /ai/recommend/ - user_id: {request.user_id}, Token user: {current_user.id if current_user else 'None'}")
    # Récupérer les résultats de quiz
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == request.user_id).all()
    if not quiz_results:
        return {"user_id": request.user_id, "recommendations": []}
    # Analyser les sujets faibles
    sujets_faibles = {}
    for qr in quiz_results:
        if qr.score < 0.6:
            sujets_faibles[qr.sujet] = sujets_faibles.get(qr.sujet, 0) + 1
    # Recommandation de contenus sur les sujets faibles - Commenté temporairement
    recommandations = []
    # for sujet in sujets_faibles:
    #     contenus = db.query(Content).filter(Content.subject.ilike(f"%{sujet}%")).all()
    #     recommandations.extend([{"type": "content", "id": c.id, "title": c.title} for c in contenus])
    #     parcours = db.query(LearningPath).filter(LearningPath.name.ilike(f"%{sujet}%")).all()
    #     recommandations.extend([{"type": "learning_path", "id": p.id, "name": p.name} for p in parcours])
    # Si pas de faiblesse détectée, recommander des nouveautés ou des parcours avancés
    if not recommandations:
        # recommandations = [{"type": "content", "id": c.id, "title": c.title} for c in db.query(Content).limit(3)]
        recommandations = [{"type": "quiz", "message": "Quiz recommandés pour améliorer vos compétences"}]
    return {"user_id": request.user_id, "recommendations": recommandations}

@router.post("/analytics/")
def analytics(
    request: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    authorization: str = Depends(lambda: None)
):
    import fastapi
    from fastapi import Request
    # Ajout du log du header Authorization
    import inspect
    frame = inspect.currentframe()
    try:
        request_obj = None
        for f in inspect.stack():
            if 'request' in f.frame.f_locals:
                request_obj = f.frame.f_locals['request']
                break
        if request_obj:
            print(f"[DEBUG] Authorization header: {request_obj.headers.get('authorization')}")
    except Exception as e:
        print(f"[DEBUG] Impossible d'afficher le header Authorization: {e}")
    print(f"[API] /ai/analytics/ - user_id: {request.user_id}, Token user: {current_user.id if current_user else 'None'}")
    # Récupérer les résultats de quiz
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == request.user_id).all()
    if not quiz_results:
        return {"user_id": request.user_id, "analytics": {"message": "Aucune donnée disponible"}}
    # Statistiques de base
    total = len(quiz_results)
    scores = [qr.score for qr in quiz_results]
    moyenne = sum(scores) / total if total else 0
    max_score = max(scores)
    min_score = min(scores)
    # Difficultés par sujet
    sujets = {}
    for qr in quiz_results:
        sujets.setdefault(qr.sujet, []).append(qr.score)
    sujets_difficiles = [s for s, scs in sujets.items() if sum(scs)/len(scs) < 0.6]
    # Progression temporelle (optionnel)
    progression = sorted([(qr.created_at, qr.score) for qr in quiz_results], key=lambda x: x[0])
    return {
        "user_id": request.user_id,
        "analytics": {
            "total_quiz": total,
            "score_moyen": moyenne,
            "score_max": max_score,
            "score_min": min_score,
            "sujets_difficiles": sujets_difficiles,
            "progression": progression
        }
    }

@router.get("/analytics/export")
def export_analytics(user_id: int, format: str = 'csv', db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Générer les analytics comme dans le endpoint analytics
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == user_id).all()
    if not quiz_results:
        raise HTTPException(status_code=404, detail="Aucune donnée disponible")
    # Statistiques de base
    total = len(quiz_results)
    scores = [qr.score for qr in quiz_results]
    moyenne = sum(scores) / total if total else 0
    max_score = max(scores)
    min_score = min(scores)
    sujets = {}
    for qr in quiz_results:
        sujets.setdefault(qr.sujet, []).append(qr.score)
    sujets_difficiles = [s for s, scs in sujets.items() if sum(scs)/len(scs) < 0.6]
    # Génération du CSV
    if format == 'csv':
        def csv_generator():
            output = []
            writer = csv.writer(output)
            writer.writerow(["Statistique", "Valeur"])
            writer.writerow(["Total quiz", total])
            writer.writerow(["Score moyen", moyenne])
            writer.writerow(["Score max", max_score])
            writer.writerow(["Score min", min_score])
            writer.writerow(["Sujets difficiles", ", ".join(sujets_difficiles)])
            writer.writerow([])
            writer.writerow(["Détail par quiz"])
            writer.writerow(["Sujet", "Score", "Date"])
            for qr in quiz_results:
                writer.writerow([qr.sujet, qr.score, qr.created_at.strftime('%Y-%m-%d %H:%M')])
            for row in output:
                yield ','.join(map(str, row)) + '\n'
        headers = {
            "Content-Disposition": f"attachment; filename=analytics_user_{user_id}.csv"
        }
        return StreamingResponse(csv_generator(), media_type="text/csv", headers=headers)
    # Génération du PDF
    if format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Rapport Analytics - Utilisateur {user_id}', ln=1, align='C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Total quiz : {total}', ln=1)
        pdf.cell(0, 10, f'Score moyen : {moyenne:.2f}', ln=1)
        pdf.cell(0, 10, f'Score max : {max_score:.2f}', ln=1)
        pdf.cell(0, 10, f'Score min : {min_score:.2f}', ln=1)
        pdf.cell(0, 10, f'Sujets difficiles : {", ".join(sujets_difficiles)}', ln=1)
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Détail par quiz', ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(60, 8, 'Sujet', 1)
        pdf.cell(30, 8, 'Score', 1)
        pdf.cell(50, 8, 'Date', 1)
        pdf.ln()
        for qr in quiz_results:
            pdf.cell(60, 8, str(qr.sujet), 1)
            pdf.cell(30, 8, f'{qr.score:.2f}', 1)
            pdf.cell(50, 8, qr.created_at.strftime('%Y-%m-%d %H:%M'), 1)
            pdf.ln()
        pdf_output = pdf.output(dest='S').encode('latin1')
        headers = {
            "Content-Disposition": f"attachment; filename=analytics_user_{user_id}.pdf"
        }
        return StreamingResponse(iter([pdf_output]), media_type="application/pdf", headers=headers)
    else:
        raise HTTPException(status_code=400, detail="Format non supporté") 

@router.get("/analyze-student/{student_id}")
def analyze_student_cognitive(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Analyser le profil cognitif d'un étudiant."""
    try:
        # Récupérer l'étudiant
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les résultats de quiz
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
        
        # Analyser les patterns cognitifs
        cognitive_analysis = {
            "student_id": student_id,
            "student_name": student.username,
            "total_quizzes": len(quiz_results),
            "average_score": 0,
            "strengths": [],
            "weaknesses": [],
            "learning_style": "balanced",
            "recommendations": []
        }
        
        if quiz_results:
            total_score = sum(result.score for result in quiz_results)
            cognitive_analysis["average_score"] = total_score / len(quiz_results)
            
            # Analyser par sujet
            subject_scores = {}
            for result in quiz_results:
                quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
                if quiz and quiz.subject:
                    if quiz.subject not in subject_scores:
                        subject_scores[quiz.subject] = {"total": 0, "count": 0}
                    subject_scores[quiz.subject]["total"] += result.score
                    subject_scores[quiz.subject]["count"] += 1
            
            # Identifier forces et faiblesses
            for subject, data in subject_scores.items():
                avg_score = data["total"] / data["count"]
                if avg_score >= 80:
                    cognitive_analysis["strengths"].append(subject)
                elif avg_score <= 60:
                    cognitive_analysis["weaknesses"].append(subject)
            
            # Recommandations basées sur l'analyse
            if cognitive_analysis["weaknesses"]:
                cognitive_analysis["recommendations"].append(
                    f"Renforcement en {', '.join(cognitive_analysis['weaknesses'])}"
                )
            if cognitive_analysis["strengths"]:
                cognitive_analysis["recommendations"].append(
                    f"Approfondissement en {', '.join(cognitive_analysis['strengths'])}"
                )
        
        return cognitive_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse cognitive: {str(e)}")

@router.get("/predict-success/{student_id}")
def predict_student_success(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Prédire le succès futur d'un étudiant."""
    try:
        # Récupérer l'historique d'apprentissage
        learning_history = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id
        ).order_by(LearningHistory.timestamp.desc()).limit(10).all()
        
        # Analyser la progression
        if learning_history:
            recent_scores = [entry.score for entry in learning_history if entry.score is not None]
            if recent_scores:
                avg_recent_score = sum(recent_scores) / len(recent_scores)
                trend = "improving" if len(recent_scores) >= 2 and recent_scores[0] > recent_scores[-1] else "stable"
                
                # Prédiction basée sur les tendances
                if avg_recent_score >= 85:
                    success_probability = "high"
                    predicted_grade = "A"
                elif avg_recent_score >= 70:
                    success_probability = "medium"
                    predicted_grade = "B"
                else:
                    success_probability = "low"
                    predicted_grade = "C"
            else:
                success_probability = "unknown"
                predicted_grade = "N/A"
                trend = "unknown"
        else:
            success_probability = "unknown"
            predicted_grade = "N/A"
            trend = "unknown"
        
        return {
            "student_id": student_id,
            "success_probability": success_probability,
            "predicted_grade": predicted_grade,
            "trend": trend,
            "confidence": 0.75,
            "factors": ["performance_history", "engagement_level", "consistency"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")

@router.get("/recommend-content/{student_id}")
def recommend_content_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Recommandations de contenu personnalisées pour un étudiant."""
    try:
        # Analyser les préférences de l'étudiant
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
        
        recommendations = []
        
        if quiz_results:
            # Analyser les sujets où l'étudiant a des difficultés
            subject_difficulties = {}
            for result in quiz_results:
                quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
                if quiz and quiz.subject:
                    if quiz.subject not in subject_difficulties:
                        subject_difficulties[quiz.subject] = {"total": 0, "score": 0}
                    subject_difficulties[quiz.subject]["total"] += 1
                    subject_difficulties[quiz.subject]["score"] += result.score
            
            # Générer des recommandations basées sur les difficultés
            for subject, data in subject_difficulties.items():
                avg_score = data["score"] / data["total"]
                if avg_score < 70:
                    recommendations.append({
                        "type": "remediation",
                        "subject": subject,
                        "title": f"Renforcement en {subject}",
                        "description": f"Contenu de remédiation pour améliorer vos compétences en {subject}",
                        "priority": "high",
                        "estimated_time": 30
                    })
        
        # Recommandations par défaut si pas assez de données
        if not recommendations:
            recommendations = [
                {
                    "type": "exploration",
                    "subject": "Général",
                    "title": "Découverte de nouveaux sujets",
                    "description": "Explorez de nouveaux domaines d'apprentissage",
                    "priority": "medium",
                    "estimated_time": 20
                }
            ]
        
        return {
            "student_id": student_id,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors des recommandations: {str(e)}")

@router.get("/class-insights/{class_id}")
def get_class_insights(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir des insights sur une classe."""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        
        insights = {
            "class_id": class_id,
            "total_students": len(class_students),
            "average_performance": 0,
            "top_performers": [],
            "students_needing_help": [],
            "subject_performance": {},
            "recommendations": []
        }
        
        if class_students:
            total_score = 0
            student_count = 0
            
            for class_student in class_students:
                student_results = db.query(QuizResult).filter(
                    QuizResult.student_id == class_student.student_id
                ).all()
                
                if student_results:
                    student_avg = sum(result.score for result in student_results) / len(student_results)
                    total_score += student_avg
                    student_count += 1
                    
                    # Identifier les meilleurs et ceux qui ont besoin d'aide
                    if student_avg >= 85:
                        insights["top_performers"].append({
                            "student_id": class_student.student_id,
                            "average_score": student_avg
                        })
                    elif student_avg <= 60:
                        insights["students_needing_help"].append({
                            "student_id": class_student.student_id,
                            "average_score": student_avg
                        })
            
            if student_count > 0:
                insights["average_performance"] = total_score / student_count
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de classe: {str(e)}") 