#!/usr/bin/env python3
"""
API OPTIMISÉE pour l'évaluation initiale française
Garantit exactement 20 questions avec répartition équilibrée et anti-répétition
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from core.database import get_db
from core.security import get_current_user, require_role
from models.user import User, UserRole
from models.french_learning import FrenchLearningProfile
from models.question_history import QuestionHistory
from sqlalchemy import text

# Import de nos nouveaux services
try:
    from services.french_question_selector import FrenchQuestionSelector
    from services.french_test_session_manager import FrenchTestSessionManager
    SERVICES_AVAILABLE = True
    print("✅ Services français optimisés chargés avec succès")
except ImportError as e:
    SERVICES_AVAILABLE = False
    print(f"⚠️ Services français non disponibles: {e}")

router = APIRouter(tags=["french_initial_assessment_optimized"])

# ============================================================================
# ENDPOINTS OPTIMISÉS POUR 20 QUESTIONS EXACTES
# ============================================================================

@router.post("/student/start")
async def start_french_assessment(
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Démarrer une évaluation française avec exactement 20 questions
    Répartition: 7 facile + 6 moyen + 7 difficile
    """
    
    if not SERVICES_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services d'évaluation française temporairement indisponibles"
        )
    
    try:
        student_id = request.get("student_id") or current_user.id
        
        if not student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID étudiant requis"
            )
        
        print(f"🚀 Démarrage évaluation française pour étudiant {student_id}")
        
        # Utiliser notre service optimisé
        session_manager = FrenchTestSessionManager(db)
        test_result = session_manager.start_test_session(student_id)
        
        print(f"✅ Test démarré avec succès: {test_result['status']}")
        
        return {
            "success": True,
            "message": "Test français démarré avec succès",
            **test_result
        }
        
    except Exception as e:
        print(f"❌ Erreur démarrage test: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage du test: {str(e)}"
        )

@router.post("/{test_id}/submit")
async def submit_french_answer(
    test_id: int,
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Soumettre une réponse et passer à la question suivante
    Arrêt automatique après 20 questions
    """
    
    if not SERVICES_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services d'évaluation française temporairement indisponibles"
        )
    
    try:
        student_id = current_user.id
        answer = request.get("answer")
        
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Réponse requise"
            )
        
        print(f"📝 Soumission réponse pour test {test_id}, étudiant {student_id}")
        
        # Utiliser notre service optimisé
        session_manager = FrenchTestSessionManager(db)
        result = session_manager.submit_answer(test_id, student_id, answer)
        
        print(f"✅ Réponse soumise, statut: {result['status']}")
        
        return {
            "success": True,
            "message": "Réponse soumise avec succès",
            **result
        }
        
    except Exception as e:
        print(f"❌ Erreur soumission réponse: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la soumission: {str(e)}"
        )

@router.get("/student/{student_id}/profile")
async def get_french_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer le profil français de l'étudiant
    """
    
    try:
        print(f"👤 Récupération profil français pour étudiant {student_id}")
        
        # Récupérer le profil depuis la base
        result = db.execute(text("""
            SELECT 
                flp.learning_style,
                flp.french_level,
                flp.preferred_pace,
                flp.strengths,
                flp.weaknesses,
                flp.cognitive_profile,
                flp.created_at,
                flp.updated_at
            FROM french_learning_profiles flp
            WHERE flp.student_id = :student_id
            ORDER BY flp.updated_at DESC
            LIMIT 1
        """), {"student_id": student_id})
        
        profile_row = result.fetchone()
        
        if not profile_row:
            return {
                "success": True,
                "message": "Aucun profil français trouvé",
                "profile": None
            }
        
        # Formater le profil
        profile = {
            "learning_style": profile_row[0],
            "french_level": profile_row[1],
            "preferred_pace": profile_row[2],
            "strengths": json.loads(profile_row[3]) if profile_row[3] else [],
            "weaknesses": json.loads(profile_row[4]) if profile_row[4] else [],
            "cognitive_profile": json.loads(profile_row[5]) if profile_row[5] else {},
            "created_at": profile_row[6].isoformat() if hasattr(profile_row[6], 'isoformat') else str(profile_row[6]) if profile_row[6] else None,
            "updated_at": profile_row[7].isoformat() if hasattr(profile_row[7], 'isoformat') else str(profile_row[7]) if profile_row[7] else None
        }
        
        return {
            "success": True,
            "message": "Profil français récupéré avec succès",
            "profile": profile
        }
        
    except Exception as e:
        print(f"❌ Erreur récupération profil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du profil: {str(e)}"
        )

@router.get("/student/{student_id}/test-status")
async def get_test_status(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer le statut du test français de l'étudiant
    """
    
    try:
        print(f"📊 Vérification statut test pour étudiant {student_id}")
        
        # Récupérer le statut du test
        result = db.execute(text("""
            SELECT 
                id,
                status,
                current_question_index,
                total_questions,
                current_difficulty,
                started_at,
                completed_at,
                final_score
            FROM french_adaptive_tests
            WHERE student_id = :student_id
            ORDER BY started_at DESC
            LIMIT 1
        """), {"student_id": student_id})
        
        test_row = result.fetchone()
        
        if not test_row:
            return {
                "success": True,
                "message": "Aucun test français trouvé",
                "test_status": "not_started"
            }
        
        # Formater le statut
        test_status = {
            "id": test_row[0],
            "status": test_row[1],
            "current_question": test_row[2],
            "total_questions": test_row[3],
            "current_difficulty": test_row[4],
            "started_at": test_row[5].isoformat() if hasattr(test_row[5], 'isoformat') else str(test_row[5]) if test_row[5] else None,
            "completed_at": test_row[6].isoformat() if hasattr(test_row[6], 'isoformat') else str(test_row[6]) if test_row[6] else None,
            "final_score": test_row[7]
        }
        
        return {
            "success": True,
            "message": "Statut du test récupéré avec succès",
            "test_status": test_status
        }
        
    except Exception as e:
        print(f"❌ Erreur récupération statut: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du statut: {str(e)}"
        )

@router.get("/test/public")
async def public_test_endpoint():
    """
    Endpoint de test public pour vérifier le système
    """
    return {
        "status": "success",
        "message": "API française optimisée accessible",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "exact_20_questions": True,
            "anti_repetition": True,
            "balanced_difficulty": True,
            "intelligent_selection": True,
            "profile_generation": True
        }
    }

@router.get("/questions/count/public")
async def get_questions_count_public(
    db: Session = Depends(get_db)
):
    """
    Compter les questions disponibles sans authentification (pour diagnostic)
    """
    try:
        print("🔍 Diagnostic public des questions françaises disponibles")
        
        counts = {
            "facile": 0,
            "moyen": 0,
            "difficile": 0,
            "total": 0
        }
        
        # Compter depuis question_history (existe avec colonne 'difficulty')
        result = db.execute(text("""
            SELECT difficulty, COUNT(*) as count
            FROM question_history
            WHERE topic IN ('Articles', 'Genre des noms', 'Pluriels', 'Grammaire', 'Conjugaison', 'Vocabulaire', 'Compréhension')
            GROUP BY difficulty
        """))
        
        for row in result:
            difficulty = row[0]
            count = row[1]
            if difficulty in ['easy', 'facile']:
                counts['facile'] += count
            elif difficulty in ['medium', 'moyen']:
                counts['moyen'] += count
            elif difficulty in ['hard', 'difficile']:
                counts['difficile'] += count
            counts['total'] += count
        
        # Compter depuis adaptive_questions (existe avec colonne 'difficulty_level')
        result = db.execute(text("""
            SELECT difficulty_level, COUNT(*) as count
            FROM adaptive_questions
            WHERE topic LIKE '%french%' OR topic LIKE '%français%' OR topic LIKE '%grammar%' OR topic LIKE '%grammaire%'
            GROUP BY difficulty_level
        """))
        
        for row in result:
            difficulty = row[0]
            count = row[1]
            if difficulty in [1, 2]:
                counts['facile'] += count
            elif difficulty in [3, 4]:
                counts['moyen'] += count
            elif difficulty in [5, 6, 7]:
                counts['difficile'] += count
            counts['total'] += count
        
        # Compter depuis questions (existe avec questions de quiz)
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM questions
            WHERE question_text LIKE '%Français%' OR question_text LIKE '%français%'
        """))
        
        quiz_count = result.fetchone()[0]
        counts['total'] += quiz_count
        
        return {
            "status": "success",
            "message": "Comptage des questions françaises disponibles",
            "counts": counts,
            "can_generate_20_questions": counts['total'] >= 20,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Erreur comptage public: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors du comptage: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/questions/available")
async def get_available_questions_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer le nombre de questions françaises disponibles
    """
    
    if not SERVICES_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services d'évaluation française temporairement indisponibles"
        )
    
    try:
        print("🔍 Vérification des questions françaises disponibles")
        
        # Utiliser notre service pour compter les questions
        question_selector = FrenchQuestionSelector(db)
        
        # Compter les questions par difficulté
        counts = {
            "facile": 0,
            "moyen": 0,
            "difficile": 0
        }
        
        # Compter depuis question_history
        result = db.execute(text("""
            SELECT difficulty, COUNT(*) as count
            FROM question_history
            WHERE topic IN ('Articles', 'Grammaire', 'Conjugaison', 'Vocabulaire', 'Compréhension')
            GROUP BY difficulty
        """))
        
        for row in result:
            difficulty = row[0]
            if difficulty in ['easy', 'facile']:
                counts['facile'] += row[1]
            elif difficulty in ['medium', 'moyen']:
                counts['moyen'] += row[1]
            elif difficulty in ['hard', 'difficile']:
                counts['difficile'] += row[1]
        
        # Compter depuis adaptive_questions
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM adaptive_questions
            WHERE (topic LIKE '%français%' OR topic LIKE '%grammaire%' OR topic LIKE '%conjugaison%')
            AND is_active = TRUE
        """))
        
        adaptive_count = result.fetchone()[0]
        
        total_available = sum(counts.values()) + adaptive_count
        
        return {
            "success": True,
            "message": "Nombre de questions disponibles récupéré",
            "counts": {
                **counts,
                "adaptive": adaptive_count,
                "total": total_available,
                "required_for_test": 20,
                "sufficient": total_available >= 20
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur comptage questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du comptage: {str(e)}"
        )

@router.post("/reset-test/{student_id}")
async def reset_french_test(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Réinitialiser le test français d'un étudiant
    """
    
    try:
        print(f"🔄 Réinitialisation du test français pour étudiant {student_id}")
        
        # Mettre à jour le statut du test existant
        result = db.execute(text("""
            UPDATE french_adaptive_tests
            SET status = 'abandoned', completed_at = CURRENT_TIMESTAMP
            WHERE student_id = :student_id AND status IN ('in_progress', 'paused')
        """), {"student_id": student_id})
        
        db.commit()
        
        return {
            "success": True,
            "message": "Test français réinitialisé avec succès",
            "reset_count": result.rowcount
        }
        
    except Exception as e:
        print(f"❌ Erreur réinitialisation: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la réinitialisation: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE DIAGNOSTIC ET MAINTENANCE
# ============================================================================

@router.get("/health")
async def health_check():
    """Vérification de la santé de l'API"""
    return {
        "status": "healthy",
        "service": "french_initial_assessment_optimized",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "exact_20_questions": True,
            "anti_repetition": True,
            "balanced_difficulty": True,
            "intelligent_selection": True,
            "profile_generation": True
        }
    }

@router.get("/debug/questions-selection")
async def debug_questions_selection(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint de debug pour tester la sélection de questions
    """
    
    if not SERVICES_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services non disponibles"
        )
    
    try:
        print(f"🐛 Debug sélection questions pour étudiant {student_id}")
        
        question_selector = FrenchQuestionSelector(db)
        selected_questions = question_selector.select_20_questions(student_id)
        
        return {
            "success": True,
            "message": "Sélection de questions testée",
            "debug_info": {
                "total_selected": len(selected_questions),
                "expected": 20,
                "difficulty_distribution": {
                    "facile": len([q for q in selected_questions if q['difficulty'] == 'easy']),
                    "moyen": len([q for q in selected_questions if q['difficulty'] == 'medium']),
                    "difficile": len([q for q in selected_questions if q['difficulty'] == 'hard'])
                },
                "questions_sample": selected_questions[:3]  # Premières 3 questions
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur debug: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du debug: {str(e)}"
        )
