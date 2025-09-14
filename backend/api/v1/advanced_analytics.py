from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# Import des services
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.advanced_cognitive_analysis import AdvancedCognitiveAnalyzer, ResponseAnalysis, CognitiveProfile
from services.irt_engine import IRTEngine, IRTParameters, StudentAbility
from database import get_db

router = APIRouter(prefix="/api/v1/advanced", tags=["Advanced Analytics"])

# Initialisation des services
cognitive_analyzer = AdvancedCognitiveAnalyzer()
irt_engine = IRTEngine()

# ============================================================================
# ENDPOINTS D'ANALYSE COGNITIVE AVANCÉE
# ============================================================================

@router.post("/cognitive/analyze-response")
async def analyze_single_response(
    response_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Analyser une réponse individuelle d'un étudiant"""
    try:
        # Extraire les données de la réponse
        question_id = response_data.get("question_id")
        student_id = response_data.get("student_id")
        response_time = response_data.get("response_time", 0)
        is_correct = response_data.get("is_correct", False)
        answer_text = response_data.get("answer_text", "")
        question_difficulty = response_data.get("question_difficulty", 5)
        
        # Analyser le temps de réponse
        time_analysis = cognitive_analyzer.analyze_response_time(
            response_time, question_difficulty
        )
        
        # Détecter le pattern de réponse
        response_pattern = cognitive_analyzer.detect_response_pattern(
            response_time, is_correct, answer_text, question_difficulty
        )
        
        # Créer l'analyse de réponse
        analysis = ResponseAnalysis(
            question_id=question_id,
            student_id=student_id,
            response_time=response_time,
            is_correct=is_correct,
            time_analysis=time_analysis,
            pattern=response_pattern,
            timestamp=datetime.now()
        )
        
        return {
            "status": "success",
            "analysis": {
                "question_id": analysis.question_id,
                "student_id": analysis.student_id,
                "response_time": analysis.response_time,
                "is_correct": analysis.is_correct,
                "time_analysis": analysis.time_analysis,
                "pattern": analysis.pattern,
                "timestamp": analysis.timestamp.isoformat()
            },
            "insights": {
                "time_category": time_analysis["category"],
                "pattern_type": response_pattern,
                "recommendations": cognitive_analyzer._get_time_recommendations(time_analysis["category"])
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de la réponse: {str(e)}"
        )

@router.post("/cognitive/generate-profile")
async def generate_cognitive_profile(
    student_responses: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Générer un profil cognitif complet basé sur les réponses d'un étudiant"""
    try:
        if not student_responses:
            raise HTTPException(
                status_code=400,
                detail="Aucune réponse fournie pour l'analyse"
            )
        
        # Générer le profil cognitif
        profile = cognitive_analyzer.generate_cognitive_profile(student_responses)
        
        return {
            "status": "success",
            "cognitive_profile": {
                "student_id": profile.student_id,
                "learning_style": profile.learning_style,
                "strengths": profile.strengths,
                "weaknesses": profile.weaknesses,
                "recommendations": profile.recommendations,
                "confidence_level": profile.confidence_level,
                "generated_at": profile.generated_at.isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du profil cognitif: {str(e)}"
        )

@router.get("/cognitive/error-patterns/{student_id}")
async def get_error_patterns(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Analyser les patterns d'erreurs récurrentes d'un étudiant"""
    try:
        # Simuler des données d'erreurs (à remplacer par de vraies données)
        mock_responses = [
            {"question_id": 1, "is_correct": False, "subject": "math", "difficulty": 7},
            {"question_id": 2, "is_correct": False, "subject": "math", "difficulty": 6},
            {"question_id": 3, "is_correct": True, "subject": "french", "difficulty": 5},
            {"question_id": 4, "is_correct": False, "subject": "math", "difficulty": 8},
        ]
        
        error_analysis = cognitive_analyzer.analyze_error_patterns(mock_responses)
        
        return {
            "status": "success",
            "student_id": student_id,
            "error_analysis": error_analysis
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse des patterns d'erreurs: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DU MOTEUR IRT
# ============================================================================

@router.post("/irt/estimate-ability")
async def estimate_student_ability(
    student_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Estimer la capacité d'un étudiant basée sur ses performances"""
    try:
        student_id = student_data.get("student_id")
        responses = student_data.get("responses", [])
        
        if not responses:
            raise HTTPException(
                status_code=400,
                detail="Aucune réponse fournie pour l'estimation"
            )
        
        # Estimer la capacité de l'étudiant
        ability = irt_engine.estimate_student_ability(student_id, responses)
        
        return {
            "status": "success",
            "student_id": student_id,
            "estimated_ability": ability.ability_level,
            "confidence_interval": ability.confidence_interval,
            "estimated_at": ability.estimated_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'estimation de la capacité: {str(e)}"
        )

@router.post("/irt/adapt-difficulty")
async def adapt_question_difficulty(
    adaptation_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Adapter la difficulté des questions basée sur IRT"""
    try:
        student_id = adaptation_data.get("student_id")
        current_performance = adaptation_data.get("current_performance", 0.5)
        current_difficulty = adaptation_data.get("current_difficulty", 5)
        
        # Adapter la difficulté
        adapted_difficulty = irt_engine.adapt_difficulty_irt(
            student_id, current_performance
        )
        
        return {
            "status": "success",
            "student_id": student_id,
            "current_difficulty": current_difficulty,
            "adapted_difficulty": adapted_difficulty,
            "adaptation_reason": "IRT-based adaptation",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'adaptation de la difficulté: {str(e)}"
        )

@router.post("/irt/predict-performance")
async def predict_student_performance(
    prediction_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Prédire la performance d'un étudiant sur une question donnée"""
    try:
        student_id = prediction_data.get("student_id")
        question_difficulty = prediction_data.get("question_difficulty", 5)
        question_type = prediction_data.get("question_type", "multiple_choice")
        
        # Prédire la performance
        prediction = irt_engine.predict_performance(
            student_id, question_difficulty, question_type
        )
        
        return {
            "status": "success",
            "student_id": student_id,
            "question_difficulty": question_difficulty,
            "predicted_performance": prediction,
            "confidence_level": "high" if prediction > 0.7 else "medium" if prediction > 0.4 else "low",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction de performance: {str(e)}"
        )

@router.post("/irt/cognitive-load")
async def calculate_cognitive_load(
    load_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Calculer la charge cognitive estimée d'une question"""
    try:
        question_difficulty = load_data.get("question_difficulty", 5)
        question_type = load_data.get("question_type", "multiple_choice")
        question_complexity = load_data.get("question_complexity", "medium")
        
        # Calculer la charge cognitive
        cognitive_load = irt_engine.calculate_cognitive_load(
            question_difficulty, question_type, question_complexity
        )
        
        return {
            "status": "success",
            "question_difficulty": question_difficulty,
            "question_type": question_type,
            "question_complexity": question_complexity,
            "estimated_cognitive_load": cognitive_load,
            "load_category": "high" if cognitive_load > 0.7 else "medium" if cognitive_load > 0.4 else "low",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul de la charge cognitive: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE LA BANQUE DE QUESTIONS ÉTENDUE
# ============================================================================

@router.get("/questions/extended")
async def get_extended_questions(
    subject: Optional[str] = None,
    difficulty: Optional[int] = None,
    question_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Récupérer des questions de la banque étendue avec filtres"""
    try:
        # Construire la requête de base
        query = """
        SELECT 
            eq.id,
            eq.question_text,
            eq.question_type,
            eq.subject,
            eq.difficulty,
            eq.competency,
            eq.learning_style,
            eq.options,
            eq.correct_answer,
            eq.explanation,
            eq.estimated_time,
            eq.cognitive_load,
            eq.tags,
            eq.curriculum_standards,
            eq.prerequisites,
            eq.learning_objectives
        FROM extended_questions eq
        WHERE 1=1
        """
        
        params = {}
        
        if subject:
            query += " AND eq.subject = :subject"
            params["subject"] = subject
            
        if difficulty:
            query += " AND eq.difficulty = :difficulty"
            params["difficulty"] = difficulty
            
        if question_type:
            query += " AND eq.question_type = :question_type"
            params["question_type"] = question_type
            
        query += " LIMIT :limit"
        params["limit"] = limit
        
        # Exécuter la requête
        result = db.execute(query, params)
        questions = result.fetchall()
        
        # Formater les résultats
        formatted_questions = []
        for q in questions:
            formatted_questions.append({
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "subject": q.subject,
                "difficulty": q.difficulty,
                "competency": q.competency,
                "learning_style": q.learning_style,
                "options": json.loads(q.options) if q.options else [],
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "estimated_time": q.estimated_time,
                "cognitive_load": q.cognitive_load,
                "tags": json.loads(q.tags) if q.tags else [],
                "curriculum_standards": q.curriculum_standards,
                "prerequisites": q.prerequisites,
                "learning_objectives": q.learning_objectives
            })
        
        return {
            "status": "success",
            "questions": formatted_questions,
            "total_count": len(formatted_questions),
            "filters_applied": {
                "subject": subject,
                "difficulty": difficulty,
                "question_type": question_type,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des questions: {str(e)}"
        )

@router.get("/questions/metadata")
async def get_question_metadata(
    db: Session = Depends(get_db)
):
    """Récupérer les métadonnées des questions (statistiques, tags, etc.)"""
    try:
        # Statistiques par sujet
        subject_stats = db.execute("""
            SELECT 
                subject,
                COUNT(*) as total_questions,
                AVG(difficulty) as avg_difficulty,
                AVG(cognitive_load) as avg_cognitive_load
            FROM extended_questions 
            GROUP BY subject
        """).fetchall()
        
        # Statistiques par type de question
        type_stats = db.execute("""
            SELECT 
                question_type,
                COUNT(*) as total_questions,
                AVG(difficulty) as avg_difficulty
            FROM extended_questions 
            GROUP BY question_type
        """).fetchall()
        
        # Tags les plus populaires
        popular_tags = db.execute("""
            SELECT 
                tag,
                COUNT(*) as usage_count
            FROM question_tag_relations qtr
            JOIN question_tags qt ON qtr.tag_id = qt.id
            GROUP BY tag
            ORDER BY usage_count DESC
            LIMIT 10
        """).fetchall()
        
        return {
            "status": "success",
            "metadata": {
                "subject_statistics": [
                    {
                        "subject": stat.subject,
                        "total_questions": stat.total_questions,
                        "avg_difficulty": round(stat.avg_difficulty, 2),
                        "avg_cognitive_load": round(stat.avg_cognitive_load, 2)
                    }
                    for stat in subject_stats
                ],
                "question_type_statistics": [
                    {
                        "question_type": stat.question_type,
                        "total_questions": stat.total_questions,
                        "avg_difficulty": round(stat.avg_difficulty, 2)
                    }
                    for stat in type_stats
                ],
                "popular_tags": [
                    {
                        "tag": tag.tag,
                        "usage_count": tag.usage_count
                    }
                    for tag in popular_tags
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des métadonnées: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE DASHBOARD AVANCÉ
# ============================================================================

@router.get("/dashboard/class-overview")
async def get_advanced_class_overview(
    class_id: int,
    db: Session = Depends(get_db)
):
    """Vue d'ensemble avancée d'une classe avec analyses cognitives"""
    try:
        # Simuler des données de classe (à remplacer par de vraies données)
        class_data = {
            "class_id": class_id,
            "class_name": "Classe 6ème A",
            "total_students": 25,
            "average_performance": 78.5,
            "cognitive_insights": {
                "learning_styles_distribution": {
                    "visual": 40,
                    "auditory": 25,
                    "kinesthetic": 20,
                    "reading_writing": 15
                },
                "common_strengths": ["logique mathématique", "compréhension écrite"],
                "common_weaknesses": ["résolution de problèmes", "mémoire à long terme"],
                "recommendations": [
                    "Intégrer plus d'exercices pratiques",
                    "Utiliser des supports visuels pour les concepts abstraits",
                    "Encourager la collaboration entre pairs"
                ]
            },
            "irt_insights": {
                "optimal_difficulty_range": "4-6",
                "cognitive_load_balance": "équilibré",
                "adaptation_recommendations": [
                    "Augmenter progressivement la difficulté",
                    "Alterner entre types de questions",
                    "Surveiller la charge cognitive"
                ]
            }
        }
        
        return {
            "status": "success",
            "class_overview": class_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de la vue d'ensemble: {str(e)}"
        )

@router.get("/dashboard/student-progress/{student_id}")
async def get_student_progress_analysis(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Analyse détaillée du progrès d'un étudiant avec insights cognitifs"""
    try:
        # Simuler des données de progrès (à remplacer par de vraies données)
        progress_data = {
            "student_id": student_id,
            "student_name": "Alice Martin",
            "overall_progress": 78.5,
            "cognitive_evolution": {
                "confidence_level": "increasing",
                "learning_efficiency": "improving",
                "error_patterns": "decreasing",
                "response_time": "stabilizing"
            },
            "subject_performance": {
                "math": {"score": 85, "trend": "up", "weaknesses": ["géométrie"]},
                "french": {"score": 72, "trend": "stable", "weaknesses": ["grammaire"]},
                "science": {"score": 88, "trend": "up", "weaknesses": []}
            },
            "irt_analysis": {
                "current_ability": 6.2,
                "optimal_difficulty": 6,
                "learning_curve": "positive",
                "next_milestone": "difficulty 7"
            },
            "recommendations": [
                "Continuer avec les exercices de géométrie",
                "Renforcer la grammaire française",
                "Maintenir le niveau en sciences"
            ]
        }
        
        return {
            "status": "success",
            "student_progress": progress_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse du progrès: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE TEST ET VALIDATION
# ============================================================================

@router.get("/health/advanced-services")
async def health_check_advanced_services():
    """Vérifier la santé des services avancés"""
    try:
        # Tester les services
        cognitive_status = "healthy"
        irt_status = "healthy"
        
        # Test simple du service cognitif
        try:
            test_response = {"response_time": 30, "is_correct": True, "answer_text": "test"}
            cognitive_analyzer.detect_response_pattern(30, True, "test", 5)
        except Exception as e:
            cognitive_status = f"error: {str(e)}"
        
        # Test simple du service IRT
        try:
            irt_engine.calculate_cognitive_load(5, "multiple_choice", "medium")
        except Exception as e:
            irt_status = f"error: {str(e)}"
        
        return {
            "status": "success",
            "services_health": {
                "cognitive_analysis": cognitive_status,
                "irt_engine": irt_status,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur lors de la vérification de santé: {str(e)}",
            "timestamp": datetime.now().isoformat()
        } 