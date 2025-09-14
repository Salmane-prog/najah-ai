#!/usr/bin/env python3
"""
API pour l'évaluation initiale française adaptative avec IA
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import random

from core.database import get_db
from core.security import get_current_user, require_role
from models.user import User, UserRole
from models.french_learning import (
    FrenchLearningProfile, FrenchCompetency, FrenchCompetencyProgress,
    FrenchAdaptiveTest
)
from models.question_history import QuestionHistory

# Import des services IA
try:
    from services.openai_service import OpenAIService
    from services.huggingface_service import HuggingFaceService
    from services.question_rotation_service import QuestionRotationService
    from services.adaptive_progression_service import AdaptiveProgressionService
    from services.intelligent_profile_service import IntelligentProfileService
    from services.test_cleanup_service import TestCleanupService
    AI_SERVICES_AVAILABLE = True
    print("✅ Services IA et profil intelligent chargés avec succès")
except ImportError:
    AI_SERVICES_AVAILABLE = False
    print("⚠️ Services IA non disponibles - utilisation du mode fallback")

# Import de la banque de questions étendue
try:
    from data.extended_french_questions import get_question_pool, get_random_question, select_questions_for_level_assessment
    ENHANCED_QUESTIONS_AVAILABLE = True
    print("✅ Banque de questions étendue (100+ questions) chargée avec succès")
except ImportError:
    ENHANCED_QUESTIONS_AVAILABLE = False
    print("⚠️ Banque de questions étendue non disponible - utilisation du fallback")

router = APIRouter(tags=["french_initial_assessment"])

# Initialisation des services IA
ai_service = None
hf_service = None
question_rotation_service = None
if AI_SERVICES_AVAILABLE:
    try:
        ai_service = OpenAIService()
        hf_service = HuggingFaceService()
        question_rotation_service = QuestionRotationService
        print("✅ Services IA initialisés avec succès")
    except Exception as e:
        print(f"❌ Erreur initialisation IA: {e}")
        AI_SERVICES_AVAILABLE = False

# Banque de questions françaises de fallback (si IA indisponible)
FRENCH_QUESTIONS_FALLBACK = {
    "easy": [
        {
            "id": 1,
            "question": "Quel est l'article correct ? '___ chat'",
            "options": ["Le", "La", "Les", "L'"],
            "correct": "Le",
            "explanation": "Le mot 'chat' est masculin singulier, donc on utilise 'Le'",
            "difficulty": "easy",
            "topic": "Articles"
        },
        {
            "id": 2,
            "question": "Conjuguez le verbe 'être' à la 1ère personne du singulier au présent",
            "options": ["Je suis", "Je es", "Je être", "Je suis être"],
            "correct": "Je suis",
            "explanation": "Le verbe 'être' se conjugue 'je suis' à la 1ère personne du singulier au présent",
            "difficulty": "easy",
            "topic": "Conjugaison"
        },
        {
            "id": 3,
            "question": "Quel est le genre du mot 'maison' ?",
            "options": ["Masculin", "Féminin", "Neutre", "Variable"],
            "correct": "Féminin",
            "explanation": "Le mot 'maison' est un nom féminin",
            "difficulty": "easy",
            "topic": "Genre des noms"
        },
        {
            "id": 4,
            "question": "Quel est le pluriel de 'cheval' ?",
            "options": ["Chevals", "Chevaux", "Chevales", "Cheval"],
            "correct": "Chevaux",
            "explanation": "Le pluriel de 'cheval' est 'chevaux' (pluriel irrégulier)",
            "difficulty": "easy",
            "topic": "Pluriels"
        },
        {
            "id": 5,
            "question": "Quel est l'antonyme de 'grand' ?",
            "options": ["Petit", "Gros", "Long", "Large"],
            "correct": "Petit",
            "explanation": "L'antonyme de 'grand' est 'petit'",
            "difficulty": "easy",
            "topic": "Vocabulaire"
        }
    ],
    "medium": [
        {
            "id": 6,
            "question": "Complétez : 'Les enfants ___ dans le jardin.'",
            "options": ["joue", "jouent", "joues", "jouer"],
            "correct": "jouent",
            "explanation": "Avec le sujet 'Les enfants' (pluriel), le verbe 'jouer' prend la terminaison '-ent'",
            "difficulty": "medium",
            "topic": "Accords"
        },
        {
            "id": 7,
            "question": "Quel temps verbal dans 'J'ai mangé une pomme' ?",
            "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
            "correct": "Passé composé",
            "explanation": "'J'ai mangé' est au passé composé (avoir + participe passé)",
            "difficulty": "medium",
            "topic": "Temps verbaux"
        },
        {
            "id": 8,
            "question": "Quel est le féminin de 'acteur' ?",
            "options": ["Acteur", "Actrice", "Acteuse", "Acteure"],
            "correct": "Actrice",
            "explanation": "Le féminin de 'acteur' est 'actrice'",
            "difficulty": "medium",
            "topic": "Formation du féminin"
        },
        {
            "id": 9,
            "question": "Combien de syllabes dans 'ordinateur' ?",
            "options": ["3", "4", "5", "6"],
            "correct": "4",
            "explanation": "'ordinateur' se divise en 4 syllabes : or-di-na-teur",
            "difficulty": "medium",
            "topic": "Phonétique"
        },
        {
            "id": 10,
            "question": "Quel est le sens de 'rapidement' ?",
            "options": ["Lentement", "Vite", "Doucement", "Fortement"],
            "correct": "Vite",
            "explanation": "'Rapidement' signifie 'vite' ou 'avec rapidité'",
            "difficulty": "medium",
            "topic": "Adverbes"
        }
    ],
    "hard": [
        {
            "id": 11,
            "question": "Quel est le mode du verbe dans 'Veuillez patienter' ?",
            "options": ["Indicatif", "Subjonctif", "Impératif", "Conditionnel"],
            "correct": "Impératif",
            "explanation": "'Veuillez' est à l'impératif, forme de politesse",
            "difficulty": "hard",
            "topic": "Modes verbaux"
        },
        {
            "id": 12,
            "question": "Quel est le type de phrase 'Quelle belle journée !' ?",
            "options": ["Déclarative", "Interrogative", "Exclamative", "Impérative"],
            "correct": "Exclamative",
            "explanation": "Cette phrase exprime une exclamation, c'est une phrase exclamative",
            "difficulty": "hard",
            "topic": "Types de phrases"
        },
        {
            "id": 13,
            "question": "Quel est le registre de langue de 'bagnole' ?",
            "options": ["Soutenu", "Courant", "Familier", "Argotique"],
            "correct": "Familier",
            "explanation": "'Bagnole' est un terme familier pour désigner une voiture",
            "difficulty": "hard",
            "topic": "Registres de langue"
        },
        {
            "id": 14,
            "question": "Quel est le sens figuré de 'avoir le cafard' ?",
            "options": ["Être malade", "Être triste", "Être fatigué", "Être en colère"],
            "correct": "Être triste",
            "explanation": "'Avoir le cafard' signifie être triste ou déprimé (expression figurée)",
            "difficulty": "hard",
            "topic": "Expressions idiomatiques"
        },
        {
            "id": 15,
            "question": "Quel est le type de complément dans 'Il mange une pomme' ?",
            "options": ["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"],
            "correct": "Complément d'objet direct",
            "explanation": "'Une pomme' est le complément d'objet direct du verbe 'mange'",
            "difficulty": "hard",
            "topic": "Analyse grammaticale"
        }
    ]
}

@router.post("/initial-assessment/start")
async def start_french_initial_assessment(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Lance une évaluation initiale française pour un étudiant (professeurs et admins uniquement)"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Vérifier s'il y a déjà une évaluation en cours
        existing_test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.student_id == student_id,
            FrenchAdaptiveTest.test_type == "initial",
            FrenchAdaptiveTest.status == "in_progress"
        ).first()
        
        if existing_test:
            raise HTTPException(
                status_code=400, 
                detail="Une évaluation initiale est déjà en cours pour cet étudiant"
            )
        
        # Créer un nouveau test adaptatif (système de 40+ questions)
        adaptive_test = FrenchAdaptiveTest(
            student_id=student_id,
            test_type="initial",
            total_questions=None,  # Pas de limite fixe - système adaptatif
            current_difficulty="easy",
            status="in_progress",
            started_at=datetime.utcnow()
        )
        
        db.add(adaptive_test)
        db.commit()
        db.refresh(adaptive_test)
        
        # Générer la première question
        first_question = generate_adaptive_question(student_id, "easy", db, adaptive_test.id)
        
        return {
            "test_id": adaptive_test.id,
            "message": "Évaluation initiale française lancée avec succès",
            "current_question": first_question,
            "progress": {
                "current": 1,
                "total": None,  # Pas de limite fixe - système adaptatif
                "difficulty": "easy"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du lancement de l'évaluation : {str(e)}"
        )

@router.post("/initial-assessment/student/start")
async def start_french_initial_assessment_student(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lance ou reprend une évaluation initiale française pour l'étudiant connecté"""
    try:
        # Debug: Afficher les informations de l'utilisateur
        print(f"🔍 DEBUG: Utilisateur connecté - ID: {current_user.id}, Rôle: {current_user.role}, Email: {current_user.email}")
        
        student_id = current_user.id
        
        # Vérifier s'il y a déjà une évaluation en cours
        existing_test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.student_id == student_id,
            FrenchAdaptiveTest.test_type == "initial",
            FrenchAdaptiveTest.status == "in_progress"
        ).first()
        
        if existing_test:
            # Vérifier si le test est récent (moins de 2 heures)
            time_threshold = datetime.utcnow() - timedelta(hours=2)
            
            if existing_test.started_at > time_threshold:
                print(f"🔄 Test existant trouvé (ID: {existing_test.id}), reprise...")
                
                # Générer la question actuelle
                current_question = generate_adaptive_question(
                    student_id, 
                    existing_test.current_difficulty, 
                    db, 
                    existing_test.id
                )
                
                return {
                    "id": existing_test.id,
                    "status": "in_progress",
                    "message": "Reprise de l'évaluation en cours",
                    "current_question": current_question,
                    "progress": {
                        "current": existing_test.current_question_index or 0,
                        "total": None,
                        "difficulty": existing_test.current_difficulty,
                        "level_progression": existing_test.level_progression,
                        "current_level": existing_test.current_level
                    }
                }
            else:
                # Test trop ancien, le supprimer et en créer un nouveau
                print(f"🗑️ Test ancien trouvé (ID: {existing_test.id}), suppression...")
                
                # Supprimer l'historique des questions
                db.query(QuestionHistory).filter(
                    QuestionHistory.test_id == existing_test.id
                ).delete()
                
                # Supprimer l'ancien test
                db.delete(existing_test)
                db.commit()
                
                print("✅ Ancien test supprimé")
        
        # Créer un nouveau test adaptatif
        print(f"🆕 Création d'un nouveau test pour l'étudiant {student_id}")
        
        adaptive_test = FrenchAdaptiveTest(
            student_id=student_id,
            test_type="initial",
            total_questions=None,  # Pas de limite fixe - système adaptatif
            current_difficulty="easy",
            status="in_progress",
            started_at=datetime.utcnow(),
            current_question_index=0,
            level_progression="A1",
            current_level="A1"
        )
        
        db.add(adaptive_test)
        db.commit()
        db.refresh(adaptive_test)
        
        # Générer la première question
        first_question = generate_adaptive_question(student_id, "easy", db, adaptive_test.id)
        
        return {
            "id": adaptive_test.id,
            "status": "in_progress",
            "message": "Évaluation initiale française lancée avec succès",
            "current_question": first_question,
            "progress": {
                "current": 0,
                "total": None,  # Pas de limite fixe - système adaptatif
                "difficulty": "easy",
                "level_progression": "A1",
                "current_level": "A1"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors du lancement de l'évaluation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du lancement de l'évaluation : {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/questions")
async def get_next_question(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère la prochaine question adaptative"""
    try:
        # Récupérer le test
        test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.id == test_id
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier que l'utilisateur est l'étudiant ou un professeur
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != test.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        if test.status != "in_progress":
            raise HTTPException(status_code=400, detail="Ce test n'est plus en cours")
        
        # Générer la prochaine question adaptative
        next_question = generate_adaptive_question(
            test.student_id, 
            test.current_difficulty, 
            db,
            test_id
        )
        
        return {
            "test_id": test_id,
            "question": next_question,
            "progress": {
                "current": test.current_question_index + 1,
                "total": None,  # Pas de limite fixe - système adaptatif
                "difficulty": test.current_difficulty
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de la question : {str(e)}"
        )

@router.post("/initial-assessment/{test_id}/submit")
async def submit_french_answer(
    test_id: int,
    answer_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soumet une réponse et adapte la difficulté"""
    try:
        # Récupérer le test
        test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.id == test_id
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier l'autorisation
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != test.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        if test.status != "in_progress":
            raise HTTPException(status_code=400, detail="Ce test n'est plus en cours")
        
        # Récupérer la question actuelle depuis les données de réponse
        student_answer = answer_data.get("answer", "")
        question_difficulty = answer_data.get("question_difficulty", "easy")
        correct_answer = answer_data.get("correct_answer", "")
        
        # Vérifier si la réponse est correcte
        is_correct = student_answer == correct_answer
        
        # Calculer le score
        if is_correct:
            test.final_score = (test.final_score or 0) + 10
        
        # Récupérer l'index actuel AVANT l'incrémentation
        current_question_index = test.current_question_index or 0
        new_question_index = current_question_index + 1
        
        print(f"📝 Question {current_question_index + 1} → {new_question_index} (Score actuel: {test.final_score or 0})")
        
        # Adapter la difficulté selon la réponse de manière plus intelligente
        current_score = test.final_score or 0
        
        # Logique de progression adaptative plus sophistiquée
        if is_correct:
            if question_difficulty == "easy":
                # Progression rapide si bon score sur easy
                if current_score >= (new_question_index * 8):  # 80% de bonnes réponses
                    new_difficulty = "medium"
                else:
                    new_difficulty = "easy"  # Rester sur easy pour consolider
            elif question_difficulty == "medium":
                # Progression vers hard si excellent sur medium
                if current_score >= (new_question_index * 9):  # 90% de bonnes réponses
                    new_difficulty = "hard"
                else:
                    new_difficulty = "medium"  # Consolider medium
            elif question_difficulty == "hard":
                new_difficulty = "hard"  # Maintenir le niveau hard
        else:
            # Réduction de difficulté si erreur
            if question_difficulty == "hard":
                new_difficulty = "medium"
            elif question_difficulty == "medium":
                new_difficulty = "easy"
            else:
                new_difficulty = "easy"  # Rester sur easy
        
        print(f"🧠 Adaptation difficulté: {question_difficulty} → {new_difficulty} (Score: {current_score}/{new_question_index * 10})")
        
        # Mettre à jour le test
        test.current_difficulty = new_difficulty
        test.current_question_index = new_question_index
        
        # Enregistrer la progression de difficulté pour l'analyse
        try:
            import json
            difficulty_progression = json.loads(test.difficulty_progression) if test.difficulty_progression else []
            difficulty_progression.append({
                "question_index": new_question_index,
                "difficulty": new_difficulty,
                "score": current_score,
                "was_correct": is_correct
            })
            test.difficulty_progression = json.dumps(difficulty_progression)
            print(f"📊 Progression enregistrée: {len(difficulty_progression)} étapes")
        except Exception as e:
            print(f"⚠️ Erreur enregistrement progression: {e}")
        
        # VÉRIFIER SI LE TEST EST TERMINÉ (SYSTÈME À 20 QUESTIONS FIXES)
        should_complete = False
        completion_reason = ""
        
        print(f"🔍 Vérification fin de test: question {new_question_index}/20")
        
        # CRITÈRE PRINCIPAL : Exactement 20 questions
        if new_question_index >= 20:
            should_complete = True
            completion_reason = f"Test de 20 questions terminé - Profil en cours de génération (Question {new_question_index})"
            print(f"🎯 TEST TERMINÉ après exactement {new_question_index} questions!")
        
        # CRITÈRE DE SÉCURITÉ : Limite absolue (au cas où)
        elif new_question_index >= 25:
            should_complete = True
            completion_reason = f"Limite de sécurité atteinte: {new_question_index} questions"
            print(f"⚠️ Limite de sécurité atteinte: {new_question_index} questions")
        
        if should_complete:
            print(f"🏁 FINALISATION DU TEST: {completion_reason}")
            test.status = "completed"
            test.completed_at = datetime.utcnow()
            test.final_score = (test.final_score or 0)
            
            # Générer le profil d'apprentissage immédiatement
            try:
                print("🧠 Génération du profil d'apprentissage...")
                
                # Calculer le niveau basé sur le score
                score_percentage = (test.final_score / (new_question_index * 10)) * 100
                print(f"📊 Score final: {test.final_score}/{new_question_index * 10} = {score_percentage:.1f}%")
                
                if score_percentage >= 90:
                    french_level = "B2"
                elif score_percentage >= 80:
                    french_level = "B1"
                elif score_percentage >= 70:
                    french_level = "A2"
                elif score_percentage >= 60:
                    french_level = "A1"
                else:
                    french_level = "A0"
                
                print(f"🎯 Niveau déterminé: {french_level}")
                
                # Analyser les forces et faiblesses basées sur la progression
                try:
                    difficulty_progression = json.loads(test.difficulty_progression) if test.difficulty_progression else []
                    
                    # Compter les bonnes réponses par difficulté
                    easy_correct = sum(1 for step in difficulty_progression if step["difficulty"] == "easy" and step["was_correct"])
                    medium_correct = sum(1 for step in difficulty_progression if step["difficulty"] == "medium" and step["was_correct"])
                    hard_correct = sum(1 for step in difficulty_progression if step["difficulty"] == "hard" and step["was_correct"])
                    
                    print(f"📈 Analyse des performances: Easy={easy_correct}, Medium={medium_correct}, Hard={hard_correct}")
                    
                    # Déterminer les forces et faiblesses
                    strengths = []
                    weaknesses = []
                    
                    if easy_correct >= 3:
                        strengths.append("maîtrise des bases")
                    if medium_correct >= 2:
                        strengths.append("niveau intermédiaire")
                    if hard_correct >= 1:
                        strengths.append("aptitude pour les défis")
                    
                    if easy_correct < 3:
                        weaknesses.append("consolidation des bases")
                    if medium_correct < 2:
                        weaknesses.append("grammaire intermédiaire")
                    if hard_correct < 1:
                        weaknesses.append("vocabulaire avancé")
                    
                    print(f"💪 Forces: {strengths}")
                    print(f"🔧 Faiblesses: {weaknesses}")
                    
                    # Créer ou mettre à jour le profil
                    existing_profile = db.query(FrenchLearningProfile).filter(
                        FrenchLearningProfile.student_id == test.student_id
                    ).first()
                    
                    if existing_profile:
                        existing_profile.french_level = french_level
                        existing_profile.strengths = json.dumps(strengths)
                        existing_profile.weaknesses = json.dumps(weaknesses)
                        existing_profile.updated_at = datetime.utcnow()
                        print(f"✅ Profil mis à jour pour l'étudiant {test.student_id}")
                    else:
                        new_profile = FrenchLearningProfile(
                            student_id=test.student_id,
                            french_level=french_level,
                            learning_style="adaptive",
                            preferred_pace="moyen",
                            strengths=json.dumps(strengths),
                            weaknesses=json.dumps(weaknesses),
                            cognitive_profile=json.dumps({
                                "memory_type": "mixed",
                                "attention_span": "medium",
                                "problem_solving": "analytical"
                            })
                        )
                        db.add(new_profile)
                        print(f"✅ Nouveau profil créé pour l'étudiant {test.student_id}")
                    
                except Exception as e:
                    print(f"⚠️ Erreur lors de la génération du profil: {e}")
                    # Créer un profil basique en cas d'erreur
                    basic_profile = FrenchLearningProfile(
                        student_id=test.student_id,
                        french_level=french_level,
                        learning_style="adaptive",
                        preferred_pace="moyen",
                        strengths=json.dumps(["persévérance"]),
                        weaknesses=json.dumps(["consolidation nécessaire"]),
                        cognitive_profile=json.dumps({
                            "memory_type": "mixed",
                            "attention_span": "medium",
                            "problem_solving": "analytical"
                        })
                    )
                    db.add(basic_profile)
                
            except Exception as e:
                print(f"❌ Erreur critique lors de la génération du profil: {e}")
            
            db.commit()
            
            print(f"🎯 Test terminé: {completion_reason}")
            print(f"📊 Score final: {test.final_score}/{new_question_index * 10}")
            
            return {
                "test_id": test_id,
                "status": "completed",
                "message": f"Évaluation terminée: {completion_reason}",
                "final_score": test.final_score,
                "total_questions": new_question_index,
                "correct_answers": test.final_score // 10,
                "completion_reason": completion_reason,
                "profile_generated": True
            }
        
        db.commit()
        
        # Générer la prochaine question
        next_question = generate_adaptive_question(
            test.student_id, 
            test.current_difficulty, 
            db,
            test_id
        )
        
        return {
            "test_id": test_id,
            "status": "in_progress",
            "next_question": next_question,
            "progress": {
                "current": new_question_index,
                "total": 20,  # Test à 20 questions fixes
                "progress_percentage": (new_question_index / 20) * 100
            },
            "previous_answer_correct": is_correct
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la soumission de la réponse : {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/results")
async def get_french_assessment_results(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère les résultats de l'évaluation française"""
    try:
        # Récupérer le test
        test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.id == test_id
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier l'autorisation
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != test.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer le profil d'apprentissage
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == test.student_id
        ).first()
        
        return {
            "test_id": test_id,
            "student_id": test.student_id,
            "status": test.status,
            "final_score": test.final_score,
            "difficulty_progression": json.loads(test.difficulty_progression) if test.difficulty_progression else [],
            "learning_profile": {
                "french_level": profile.french_level if profile else "A1",
                "learning_style": profile.learning_style if profile else "visual",
                "strengths": json.loads(profile.strengths) if profile and profile.strengths else [],
                "weaknesses": json.loads(profile.weaknesses) if profile and profile.weaknesses else []
            } if profile else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des résultats : {str(e)}"
        )

@router.get("/initial-assessment/student/{student_id}/profile")
async def get_student_french_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère le profil d'apprentissage français d'un étudiant"""
    try:
        # Vérifier que l'utilisateur est l'étudiant lui-même ou un professeur/admin
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer le profil d'apprentissage français
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == student_id
        ).first()
        
        if not profile:
            # Créer un profil par défaut si aucun n'existe
            profile = FrenchLearningProfile(
                student_id=student_id,
                learning_style="visual",
                french_level="A1",
                preferred_pace="moyen",
                strengths=json.dumps(["motivation", "persévérance"]),
                weaknesses=json.dumps(["grammaire", "vocabulaire"]),
                cognitive_profile=json.dumps({
                    "memory_type": "visual",
                    "attention_span": "medium",
                    "problem_solving": "analytical"
                })
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        
        # Récupérer les compétences et progrès
        competencies = db.query(FrenchCompetencyProgress).filter(
            FrenchCompetencyProgress.student_id == student_id
        ).all()
        
        # Récupérer les tests passés
        tests = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.student_id == student_id
        ).order_by(FrenchAdaptiveTest.started_at.desc()).all()
        
        return {
            "student_id": student_id,
            "profile": {
                "id": profile.id,
                "learning_style": profile.learning_style,
                "french_level": profile.french_level,
                "preferred_pace": profile.preferred_pace,
                "strengths": json.loads(profile.strengths) if profile.strengths else [],
                "weaknesses": json.loads(profile.weaknesses) if profile.weaknesses else [],
                "cognitive_profile": json.loads(profile.cognitive_profile) if profile.cognitive_profile else {},
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            },
            "competencies": [
                {
                    "id": comp.id,
                    "competency_name": comp.competency.name if comp.competency else "Compétence inconnue",
                    "current_level": comp.current_level,
                    "progress_percentage": comp.progress_percentage
                }
                for comp in competencies
            ],
            "tests": [
                {
                    "id": test.id,
                    "test_type": test.test_type,
                    "status": test.status,
                    "final_score": test.final_score,
                    "started_at": test.started_at,
                    "completed_at": test.completed_at
                }
                for test in tests
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du profil : {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/question-stats")
async def get_question_statistics(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère les statistiques des questions posées dans un test"""
    try:
        # Récupérer le test
        test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.id == test_id
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier que l'utilisateur est l'étudiant ou un professeur
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != test.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les statistiques via le service de rotation
        try:
            question_rotation_service = QuestionRotationService(db)
            stats = question_rotation_service.get_question_statistics(test_id)
            
            # Ajouter des informations sur la banque de questions
            if ENHANCED_QUESTIONS_AVAILABLE:
                from data.enhanced_french_questions import get_total_questions_count
                question_counts = get_total_questions_count()
                stats["question_bank_info"] = {
                    "total_available": question_counts["total"],
                    "by_difficulty": question_counts,
                    "enhanced_questions": True
                }
            else:
                stats["question_bank_info"] = {
                    "total_available": 15,  # Questions de fallback originales
                    "enhanced_questions": False
                }
            
            return {
                "test_id": test_id,
                "statistics": stats,
                "rotation_quality": "excellent" if stats.get("repetition_rate", 1.0) == 0.0 else "good"
            }
            
        except Exception as e:
            print(f"❌ Erreur récupération statistiques: {e}")
            return {
                "test_id": test_id,
                "statistics": {"error": "Impossible de récupérer les statistiques"},
                "rotation_quality": "unknown"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des statistiques : {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/personalized-profile")
async def get_personalized_profile(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère le profil personnalisé complet avec analyses détaillées"""
    try:
        # Récupérer le test
        test = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.id == test_id
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Vérifier que l'utilisateur est l'étudiant ou un professeur
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != test.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        if test.status != "completed":
            raise HTTPException(status_code=400, detail="Ce test n'est pas encore terminé")
        
        # Utiliser le service de progression adaptative
        try:
            progression_service = AdaptiveProgressionService(db)
            profile_analysis = progression_service.analyze_student_performance(
                test.student_id, test_id
            )
            
            return {
                "test_id": test_id,
                "student_id": test.student_id,
                "test_completion_date": test.completed_at,
                "profile_analysis": profile_analysis,
                "system_info": {
                    "enhanced_questions": ENHANCED_QUESTIONS_AVAILABLE,
                    "question_count": "40+ questions diversifiées" if ENHANCED_QUESTIONS_AVAILABLE else "15 questions limitées",
                    "personalization_engine": "AdaptiveProgressionService",
                    "ai_available": AI_SERVICES_AVAILABLE
                }
            }
            
        except Exception as e:
            print(f"❌ Erreur service de progression: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'analyse du profil : {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du profil : {str(e)}"
        )

# Fonctions utilitaires
def generate_adaptive_question(student_id: int, difficulty: str, db: Session, test_id: int = None) -> Dict[str, Any]:
    """Génère une question adaptative pour l'évaluation française avec rotation intelligente"""
    
    print(f"🎯 Génération question pour étudiant {student_id}, difficulté: {difficulty}, test: {test_id}")
    
    # Essayer d'abord avec l'IA
    if AI_SERVICES_AVAILABLE and ai_service:
        try:
            print(f"🤖 Génération de question IA pour difficulté: {difficulty}")
            
            # Déterminer le niveau de l'étudiant
            student_profile = db.query(FrenchLearningProfile).filter(
                FrenchLearningProfile.student_level == student_id
            ).first()
            
            student_level = student_profile.french_level if student_profile else "A1"
            
            # Générer une question avec GPT-3.5
            ai_question = ai_service.generate_quiz_question(
                topic="français",
                difficulty=difficulty,
                student_level=student_level
            )
            
            if ai_question and ai_question.get("question"):
                print(f"✅ Question IA générée: {ai_question['question'][:50]}...")
                
                # Enregistrer la question dans l'historique si on a un test_id
                if test_id and question_rotation_service:
                    try:
                        rotation_service = question_rotation_service(db)
                        rotation_service._record_question_asked(test_id, ai_question)
                    except Exception as e:
                        print(f"⚠️ Erreur enregistrement historique IA: {e}")
                
                return ai_question
            else:
                print("⚠️ Question IA invalide, utilisation du fallback")
                
        except Exception as e:
            print(f"❌ Erreur génération IA: {e}, utilisation du fallback")
    
    # Utiliser la banque de questions étendue avec rotation intelligente
    if ENHANCED_QUESTIONS_AVAILABLE and test_id and question_rotation_service:
        try:
            print(f"📚 Utilisation de la banque étendue avec rotation intelligente pour difficulté: {difficulty}")
            
            # Récupérer le pool de questions
            question_pool = get_question_pool(difficulty, include_dynamic=True)
            
            # Utiliser le service de rotation intelligente
            rotation_service = question_rotation_service(db)
            
            # Récupérer la performance de l'étudiant pour sélection optimale
            student_performance = None
            try:
                profile = db.query(FrenchLearningProfile).filter(
                    FrenchLearningProfile.student_id == student_id
                ).first()
                if profile and profile.weaknesses:
                    import json
                    weaknesses = json.loads(profile.weaknesses)
                    student_performance = {"weak_topics": weaknesses}
            except Exception as e:
                print(f"⚠️ Erreur récupération performance: {e}")
            
            # Sélectionner la question optimale
            selected_question = rotation_service.select_optimal_question(
                difficulty=difficulty,
                test_id=test_id,
                question_pool=question_pool,
                student_performance=student_performance
            )
            
            print(f"✅ Question sélectionnée intelligemment: {selected_question['question'][:50]}...")
            return selected_question
            
        except Exception as e:
            print(f"❌ Erreur rotation intelligente: {e}, utilisation du fallback simple")
    
    # Fallback vers les questions statiques avec rotation intelligente
    print(f"📚 Utilisation des questions de fallback avec rotation intelligente pour difficulté: {difficulty}")
    
    if test_id and question_rotation_service:
        try:
            # Utiliser le service de rotation même pour les questions de fallback
            rotation_service = question_rotation_service(db)
            
            # Récupérer le pool de questions de fallback
            question_pool = FRENCH_QUESTIONS_FALLBACK[difficulty] if difficulty in FRENCH_QUESTIONS_FALLBACK else FRENCH_QUESTIONS_FALLBACK["easy"]
            
            # Sélectionner une question sans répétition
            selected_question = rotation_service.select_optimal_question(
                difficulty=difficulty,
                test_id=test_id,
                question_pool=question_pool,
                student_performance=None
            )
            
            print(f"✅ Question de fallback sélectionnée intelligemment: {selected_question['question'][:50]}...")
            return selected_question
            
        except Exception as e:
            print(f"⚠️ Erreur rotation intelligente fallback: {e}, utilisation du fallback simple")
    
    # Fallback simple sans rotation (en cas d'erreur)
    print(f"⚠️ Utilisation du fallback simple pour difficulté: {difficulty}")
    
    # Sélectionner une question aléatoire de la difficulté demandée
    if difficulty in FRENCH_QUESTIONS_FALLBACK:
        import random
        question_pool = FRENCH_QUESTIONS_FALLBACK[difficulty]
        
        # Si on a un test_id, essayer d'éviter la répétition
        if test_id:
            try:
                # Récupérer les questions déjà posées
                existing_test = db.query(FrenchAdaptiveTest).filter(FrenchAdaptiveTest.id == test_id).first()
                if existing_test and existing_test.question_history:
                    import json
                    asked_questions = json.loads(existing_test.question_history)
                    
                    # Filtrer les questions non posées
                    available_questions = [q for q in question_pool if q.get('id') not in asked_questions]
                    
                    if available_questions:
                        selected_question = random.choice(available_questions)
                        print(f"✅ Question de fallback sélectionnée (évite répétition): {selected_question['question'][:50]}...")
                        return selected_question
                    else:
                        print("⚠️ Toutes les questions ont été posées, réutilisation")
            except Exception as e:
                print(f"⚠️ Erreur vérification historique: {e}")
        
        # Sélection aléatoire simple
        selected_question = random.choice(question_pool)
        print(f"✅ Question de fallback sélectionnée aléatoirement: {selected_question['question'][:50]}...")
        return selected_question
    else:
        # Fallback vers easy si la difficulté n'existe pas
        fallback_question = random.choice(FRENCH_QUESTIONS_FALLBACK["easy"])
        print(f"⚠️ Difficulté {difficulty} non trouvée, fallback vers easy: {fallback_question['question'][:50]}...")
        return fallback_question

def generate_fallback_question(difficulty: str) -> Dict[str, Any]:
    """Génère une question de fallback si l'IA n'est pas disponible"""
    # Sélectionner la difficulté appropriée
    if difficulty not in FRENCH_QUESTIONS_FALLBACK:
        difficulty = "easy"  # Fallback vers easy si la difficulté n'existe pas
    
    available_questions = FRENCH_QUESTIONS_FALLBACK[difficulty]
    
    if not available_questions:
        # Si pas de questions pour cette difficulté, utiliser easy
        available_questions = FRENCH_QUESTIONS_FALLBACK["easy"]
    
    # Sélectionner une question aléatoire
    selected_question = random.choice(available_questions)
    
    # Retourner la question au format attendu par le frontend
    return {
        "id": selected_question["id"],
        "question": selected_question["question"],
        "options": selected_question["options"],
        "correct": selected_question["correct"],
        "explanation": selected_question["explanation"],
        "difficulty": selected_question["difficulty"],
        "topic": selected_question["topic"],
        "question_type": "multiple_choice"
    }

def adapt_difficulty_ai(current_difficulty: str, response_analysis: Dict, question_context: Dict) -> str:
    """Adapte la difficulté de manière intelligente selon l'analyse IA"""
    
    precision = response_analysis.get("precision", 50)
    confidence = response_analysis.get("cognitive_insights", {}).get("confidence_level", "medium")
    thinking_pattern = response_analysis.get("cognitive_insights", {}).get("thinking_pattern", "linear")
    
    print(f"🧠 Adaptation IA - Précision: {precision}%, Confiance: {confidence}, Pattern: {thinking_pattern}")
    
    # Logique d'adaptation intelligente
    if current_difficulty == "easy":
        if precision > 85 and confidence == "high":
            return "medium"  # Progression rapide si excellente performance
        elif precision > 70:
            return "medium" if random.random() > 0.4 else "easy"
        else:
            return "easy"  # Reste en difficulté facile
    
    elif current_difficulty == "medium":
        if precision > 90 and thinking_pattern == "analytical":
            return "hard"  # Progression vers difficile si analyse excellente
        elif precision > 75:
            return "hard" if random.random() > 0.5 else "medium"
        elif precision < 60:
            return "easy"  # Retour en arrière si difficulté
        else:
            return "medium"
    
    else:  # hard
        if precision > 80:
            return "hard"  # Maintient le niveau difficile
        elif precision < 70:
            return "medium"  # Retour au niveau moyen
        else:
            return "hard" if random.random() > 0.3 else "medium"

def adapt_difficulty(current_difficulty: str, is_correct: bool, question_difficulty: str) -> str:
    """Adapte la difficulté selon la réponse de l'étudiant (fallback)"""
    if current_difficulty == "easy":
        if is_correct:
            return "medium" if random.random() > 0.3 else "easy"
        else:
            return "easy"
    elif current_difficulty == "medium":
        if is_correct:
            return "hard" if random.random() > 0.4 else "medium"
        else:
            return "easy"
    else:  # hard
        if is_correct:
            return "hard"
        else:
            return "medium" if random.random() > 0.5 else "easy"

async def generate_learning_profile(student_id: int, db: Session) -> Dict[str, Any]:
    """Génère un profil d'apprentissage intelligent basé sur l'analyse IA"""
    try:
        print(f"🧠 Génération du profil d'apprentissage intelligent pour étudiant {student_id}")
        
        # Récupérer les résultats du test pour analyse
        test_results = db.query(FrenchAdaptiveTest).filter(
            FrenchAdaptiveTest.student_id == student_id,
            FrenchAdaptiveTest.status == "completed"
        ).order_by(FrenchAdaptiveTest.completed_at.desc()).first()
        
        if test_results and AI_SERVICES_AVAILABLE:
            try:
                # Utiliser le nouveau service de profil intelligent
                intelligent_profile_service = IntelligentProfileService(db)
                profile_data = intelligent_profile_service.generate_intelligent_profile(
                    test_results.id, student_id
                )
                
                print(f"🧠 Profil intelligent généré - Niveau réel: {profile_data.get('real_french_level', 'N/A')}")
                print(f"📊 Score de confiance: {profile_data.get('confidence_score', 0):.2f}")
                
                # Mettre à jour le profil dans la base de données
                existing_profile = db.query(FrenchLearningProfile).filter(
                    FrenchLearningProfile.student_id == student_id
                ).first()
                
                if existing_profile:
                    # Mettre à jour le profil existant
                    existing_profile.learning_style = profile_data.get('learning_style', 'visual')
                    existing_profile.french_level = profile_data.get('real_french_level', 'A1')
                    existing_profile.preferred_pace = profile_data.get('preferred_pace', 'moyen')
                    existing_profile.strengths = profile_data.get('strengths', '[]')
                    existing_profile.weaknesses = profile_data.get('weaknesses', '[]')
                    existing_profile.cognitive_profile = profile_data.get('cognitive_profile', '{}')
                    existing_profile.updated_at = datetime.utcnow()
                else:
                    # Créer un nouveau profil
                    new_profile = FrenchLearningProfile(
                        student_id=student_id,
                        learning_style=profile_data.get('learning_style', 'visual'),
                        french_level=profile_data.get('real_french_level', 'A1'),
                        preferred_pace=profile_data.get('preferred_pace', 'moyen'),
                        strengths=profile_data.get('strengths', '[]'),
                        weaknesses=profile_data.get('weaknesses', '[]'),
                        cognitive_profile=profile_data.get('cognitive_profile', '{}')
                    )
                    db.add(new_profile)
                
                db.commit()
                print("✅ Profil intelligent mis à jour dans la base de données")
                
                return profile_data
                
            except Exception as e:
                print(f"❌ Erreur service de profil intelligent: {e}, utilisation du fallback")
                return generate_fallback_profile()
        
        # Fallback vers l'ancien système
        if AI_SERVICES_AVAILABLE and ai_service:
            try:
                # Utiliser l'IA pour analyser le profil
                profile_data = await generate_ai_learning_profile(student_id, test_results, db)
                print("✅ Profil IA généré avec succès")
                return profile_data
            except Exception as e:
                print(f"❌ Erreur génération IA: {e}, utilisation du fallback")
        
        return generate_fallback_profile()
        
    except Exception as e:
        print(f"❌ Erreur génération profil: {e}")
        return generate_fallback_profile()

async def generate_ai_learning_profile(student_id: int, test_results: FrenchAdaptiveTest, db: Session) -> Dict[str, Any]:
    """Génère un profil d'apprentissage intelligent avec l'IA"""
    
    try:
        # Analyser les performances du test
        final_score = test_results.final_score or 0
        difficulty_progression = json.loads(test_results.difficulty_progression) if test_results.difficulty_progression else []
        
        # Déterminer le niveau français basé sur le score
        if final_score >= 90:
            french_level = "B1"
        elif final_score >= 80:
            french_level = "A2"
        elif final_score >= 70:
            french_level = "A1+"
        else:
            french_level = "A1"
        
        # Analyser la progression de difficulté pour déterminer le style d'apprentissage
        if len(difficulty_progression) >= 3:
            # Analyser la stabilité de la progression
            stable_progression = all(difficulty_progression[i] <= difficulty_progression[i+1] 
                                   for i in range(len(difficulty_progression)-1))
            
            if stable_progression:
                learning_style = "auditory"  # Progression stable = style auditif
                preferred_pace = "rapide"
            else:
                learning_style = "kinesthetic"  # Progression variable = style kinesthésique
                preferred_pace = "moyen"
        else:
            learning_style = "visual"  # Par défaut
            preferred_pace = "moyen"
        
        # Déterminer les forces et faiblesses basées sur le score
        if final_score >= 80:
            strengths = ["excellente compréhension", "bonne mémoire", "logique développée"]
            weaknesses = ["perfectionnement", "pratique avancée"]
        elif final_score >= 60:
            strengths = ["motivation", "persévérance", "progression régulière"]
            weaknesses = ["grammaire", "vocabulaire", "pratique"]
        else:
            strengths = ["motivation", "détermination"]
            weaknesses = ["bases fondamentales", "grammaire", "vocabulaire", "pratique"]
        
        # Profil cognitif basé sur l'analyse
        cognitive_profile = {
            "memory_type": "visual" if learning_style == "visual" else "auditory",
            "attention_span": "long" if final_score >= 80 else "moyen",
            "problem_solving": "analytical" if final_score >= 70 else "intuitive",
            "learning_speed": "rapide" if preferred_pace == "rapide" else "moyen",
            "confidence_level": "high" if final_score >= 85 else "medium"
        }
        
        return {
            "learning_style": learning_style,
            "french_level": french_level,
            "preferred_pace": preferred_pace,
            "strengths": json.dumps(strengths),
            "weaknesses": json.dumps(weaknesses),
            "cognitive_profile": json.dumps(cognitive_profile),
            "ai_generated": True,
            "confidence_score": min(final_score / 100, 0.95)  # Score de confiance de l'IA
        }
        
    except Exception as e:
        print(f"❌ Erreur génération profil IA: {e}")
        return generate_fallback_profile()

def generate_fallback_profile() -> Dict[str, Any]:
    """Génère un profil de fallback sans IA"""
    return {
        "learning_style": random.choice(["visual", "auditory", "kinesthetic"]),
        "french_level": "A1",
        "preferred_pace": random.choice(["lent", "moyen", "rapide"]),
        "strengths": json.dumps(["motivation", "persévérance"]),
        "weaknesses": json.dumps(["grammaire", "vocabulaire"]),
        "cognitive_profile": json.dumps({
            "memory_type": "visual",
            "attention_span": "medium",
            "problem_solving": "analytical"
        }),
        "ai_generated": False,
        "confidence_score": 0.5
    }

def analyze_student_response_ai(student_answer: str, correct_answer: str, question_context: Dict) -> Dict[str, Any]:
    """Analyse intelligente de la réponse de l'étudiant avec IA"""
    
    if AI_SERVICES_AVAILABLE and hf_service:
        try:
            print(f"🧠 Analyse IA de la réponse: {student_answer[:30]}...")
            
            # Analyse avec HuggingFace
            analysis = hf_service.analyze_student_response(student_answer, correct_answer)
            
            # Analyse cognitive avancée
            cognitive_insights = analyze_cognitive_patterns(student_answer, question_context)
            
            return {
                **analysis,
                "cognitive_insights": cognitive_insights,
                "ai_analysis": True
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse IA: {e}")
    
    # Analyse simple de fallback
    return analyze_response_fallback(student_answer, correct_answer)

def analyze_cognitive_patterns(student_answer: str, question_context: Dict) -> Dict[str, Any]:
    """Analyse des patterns cognitifs dans la réponse"""
    
    insights = {
        "confidence_level": "medium",
        "thinking_pattern": "linear",
        "attention_span": "normal",
        "learning_style_hint": "visual"
    }
    
    # Analyse de la longueur de la réponse
    if len(student_answer) > 50:
        insights["confidence_level"] = "high"
        insights["thinking_pattern"] = "detailed"
    elif len(student_answer) < 10:
        insights["confidence_level"] = "low"
        insights["attention_span"] = "short"
    
    # Analyse du style de réponse
    if any(word in student_answer.lower() for word in ["parce que", "car", "donc"]):
        insights["thinking_pattern"] = "analytical"
    elif any(word in student_answer.lower() for word in ["je pense", "je crois", "peut-être"]):
        insights["confidence_level"] = "medium"
    
    return insights

def analyze_response_fallback(student_answer: str, correct_answer: str) -> Dict[str, Any]:
    """Analyse simple de fallback sans IA"""
    
    # Calcul de similarité simple
    student_words = set(student_answer.lower().split())
    correct_words = set(correct_answer.lower().split())
    
    if student_words and correct_words:
        similarity = len(student_words.intersection(correct_words)) / len(student_words.union(correct_words))
    else:
        similarity = 0.0
    
    # Déterminer la précision
    if similarity > 0.8:
        precision = 90
        feedback = "Excellente réponse!"
    elif similarity > 0.6:
        precision = 70
        feedback = "Bonne réponse, mais peut être améliorée."
    elif similarity > 0.4:
        precision = 50
        feedback = "Réponse partiellement correcte."
    else:
        precision = 20
        feedback = "Réponse incorrecte, revoyez le cours."
    
    return {
        "precision": precision,
        "feedback": feedback,
        "similarity": similarity,
        "ai_analysis": False
    }

# Endpoints de nettoyage et maintenance
@router.post("/cleanup/abandoned-tests")
async def cleanup_abandoned_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['admin', 'teacher']))
):
    """Nettoie les tests abandonnés (admin et professeurs uniquement)"""
    try:
        cleanup_service = TestCleanupService(db)
        result = cleanup_service.cleanup_abandoned_tests()
        
        return {
            "message": "Nettoyage des tests abandonnés terminé",
            "tests_cleaned": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du nettoyage: {str(e)}"
        )

@router.post("/cleanup/full")
async def full_cleanup(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    """Effectue un nettoyage complet (admin uniquement)"""
    try:
        cleanup_service = TestCleanupService(db)
        result = cleanup_service.full_cleanup()
        
        return {
            "message": "Nettoyage complet terminé",
            "results": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du nettoyage complet: {str(e)}"
        )

@router.get("/cleanup/stats")
async def get_cleanup_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['admin', 'teacher']))
):
    """Retourne les statistiques de nettoyage (admin et professeurs uniquement)"""
    try:
        cleanup_service = TestCleanupService(db)
        stats = cleanup_service.get_cleanup_stats()
        
        return {
            "cleanup_stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des stats: {str(e)}"
        )
