#!/usr/bin/env python3
"""
Service intelligent pour la génération de profils personnalisés
Analyse avancée des performances et création de profils IA
"""

import json
import random
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models.french_learning import FrenchAdaptiveTest, FrenchLearningProfile
from datetime import datetime

class IntelligentProfileService:
    """Service pour générer des profils d'apprentissage intelligents et personnalisés"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_intelligent_profile(self, test_id: int, student_id: int) -> Dict[str, Any]:
        """Génère un profil intelligent basé sur l'analyse complète du test"""
        try:
            # Récupérer le test
            test = self.db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.id == test_id
            ).first()
            
            if not test:
                raise Exception("Test non trouvé")
            
            # Analyser les performances
            performance_analysis = self._analyze_performance(test)
            
            # Déterminer le niveau réel
            real_level = self._determine_real_level(performance_analysis)
            
            # Analyser les forces et faiblesses
            strengths_weaknesses = self._analyze_strengths_weaknesses(performance_analysis)
            
            # Créer le profil cognitif
            cognitive_profile = self._create_cognitive_profile(performance_analysis)
            
            # Générer les recommandations
            recommendations = self._generate_recommendations(performance_analysis, real_level)
            
            # Créer le profil final
            profile = {
                "student_id": student_id,
                "test_id": test_id,
                "real_french_level": real_level,
                "confidence_score": performance_analysis["confidence_score"],
                "learning_style": cognitive_profile["learning_style"],
                "preferred_pace": cognitive_profile["preferred_pace"],
                "strengths": json.dumps(strengths_weaknesses["strengths"]),
                "weaknesses": json.dumps(strengths_weaknesses["weaknesses"]),
                "cognitive_profile": json.dumps(cognitive_profile),
                "recommendations": json.dumps(recommendations),
                "ai_generated": True,
                "generated_at": datetime.utcnow().isoformat(),
                "performance_metrics": performance_analysis
            }
            
            return profile
            
        except Exception as e:
            print(f"❌ Erreur génération profil intelligent: {e}")
            return self._generate_fallback_profile(student_id)
    
    def _analyze_performance(self, test: FrenchAdaptiveTest) -> Dict[str, Any]:
        """Analyse détaillée des performances du test"""
        try:
            final_score = test.final_score or 0
            total_questions = test.current_question_index or 1
            score_percentage = (final_score / (total_questions * 10)) * 100
            
            # Analyser la progression de difficulté
            difficulty_progression = []
            if test.difficulty_progression:
                try:
                    difficulty_progression = json.loads(test.difficulty_progression)
                except:
                    difficulty_progression = []
            
            # Calculer la stabilité de la progression
            stability_score = self._calculate_stability_score(difficulty_progression)
            
            # Analyser la distribution des réponses
            response_patterns = self._analyze_response_patterns(difficulty_progression)
            
            # Calculer le score de confiance
            confidence_score = self._calculate_confidence_score(
                score_percentage, stability_score, total_questions
            )
            
            return {
                "final_score": final_score,
                "total_questions": total_questions,
                "score_percentage": score_percentage,
                "difficulty_progression": difficulty_progression,
                "stability_score": stability_score,
                "response_patterns": response_patterns,
                "confidence_score": confidence_score,
                "max_difficulty_reached": self._get_max_difficulty_reached(difficulty_progression),
                "consistency_score": self._calculate_consistency_score(difficulty_progression)
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse performance: {e}")
            return {"confidence_score": 0.5}
    
    def _determine_real_level(self, performance: Dict[str, Any]) -> str:
        """Détermine le vrai niveau français basé sur l'analyse"""
        try:
            score_percentage = performance.get("score_percentage", 0)
            max_difficulty = performance.get("max_difficulty_reached", "easy")
            stability = performance.get("stability_score", 0)
            total_questions = performance.get("total_questions", 1)
            
            # Logique de détermination du niveau
            if total_questions < 5:
                return "A0"  # Pas assez de données
            
            if score_percentage >= 95 and max_difficulty in ["hard", "C1", "C2"]:
                return "C2" if stability >= 0.8 else "C1"
            elif score_percentage >= 90 and max_difficulty in ["medium", "hard", "B1", "B2"]:
                return "B2" if stability >= 0.7 else "B1"
            elif score_percentage >= 80 and max_difficulty in ["medium", "B1"]:
                return "B1" if stability >= 0.6 else "A2"
            elif score_percentage >= 70 and max_difficulty in ["easy", "medium", "A2"]:
                return "A2" if stability >= 0.5 else "A1"
            elif score_percentage >= 60:
                return "A1"
            else:
                return "A0"
                
        except Exception as e:
            print(f"❌ Erreur détermination niveau: {e}")
            return "A1"
    
    def _analyze_strengths_weaknesses(self, performance: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyse les forces et faiblesses basées sur la performance"""
        try:
            score_percentage = performance.get("score_percentage", 0)
            response_patterns = performance.get("response_patterns", {})
            max_difficulty = performance.get("max_difficulty_reached", "easy")
            
            strengths = []
            weaknesses = []
            
            # Forces basées sur le score
            if score_percentage >= 90:
                strengths.extend(["Excellente maîtrise", "Très bonne compréhension", "Logique développée"])
            elif score_percentage >= 80:
                strengths.extend(["Bonne maîtrise", "Compréhension solide", "Progression régulière"])
            elif score_percentage >= 70:
                strengths.extend(["Maîtrise correcte", "Bases solides", "Motivation"])
            else:
                strengths.extend(["Motivation", "Détermination", "Persévérance"])
            
            # Forces basées sur la difficulté
            if max_difficulty in ["C1", "C2"]:
                strengths.append("Niveau avancé atteint")
            elif max_difficulty in ["B1", "B2"]:
                strengths.append("Niveau intermédiaire avancé")
            elif max_difficulty == "medium":
                strengths.append("Progression vers l'intermédiaire")
            
            # Faiblesses basées sur le score
            if score_percentage < 70:
                weaknesses.extend(["Bases à consolider", "Grammaire", "Vocabulaire"])
            if score_percentage < 80:
                weaknesses.extend(["Pratique", "Fluidité"])
            if score_percentage < 90:
                weaknesses.extend(["Perfectionnement", "Nuances"])
            
            # Faiblesses basées sur les patterns
            if response_patterns.get("easy_errors", 0) > 0:
                weaknesses.append("Concepts de base")
            if response_patterns.get("medium_errors", 0) > 0:
                weaknesses.append("Concepts intermédiaires")
            if response_patterns.get("hard_errors", 0) > 0:
                weaknesses.append("Concepts avancés")
            
            return {
                "strengths": strengths[:5],  # Limiter à 5 forces
                "weaknesses": weaknesses[:5]  # Limiter à 5 faiblesses
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse forces/faiblesses: {e}")
            return {
                "strengths": ["Motivation", "Persévérance"],
                "weaknesses": ["Bases", "Pratique"]
            }
    
    def _create_cognitive_profile(self, performance: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un profil cognitif personnalisé"""
        try:
            score_percentage = performance.get("score_percentage", 0)
            stability = performance.get("stability_score", 0)
            consistency = performance.get("consistency_score", 0)
            response_patterns = performance.get("response_patterns", {})
            
            # Déterminer le style d'apprentissage
            if stability >= 0.8 and consistency >= 0.8:
                learning_style = "auditory"  # Apprentissage stable et cohérent
            elif stability >= 0.6 and consistency >= 0.6:
                learning_style = "visual"    # Apprentissage modérément stable
            else:
                learning_style = "kinesthetic"  # Apprentissage variable
            
            # Déterminer le rythme préféré
            if score_percentage >= 90:
                preferred_pace = "rapide"
            elif score_percentage >= 75:
                preferred_pace = "moyen"
            else:
                preferred_pace = "lent"
            
            # Profil cognitif détaillé
            cognitive_profile = {
                "learning_style": learning_style,
                "preferred_pace": preferred_pace,
                "memory_type": "visual" if learning_style == "visual" else "auditory",
                "attention_span": "long" if score_percentage >= 80 else "moyen",
                "problem_solving": "analytical" if score_percentage >= 70 else "intuitive",
                "learning_speed": "rapide" if preferred_pace == "rapide" else "moyen",
                "confidence_level": "high" if score_percentage >= 85 else "medium",
                "adaptability": "high" if stability >= 0.7 else "medium",
                "consistency": "high" if consistency >= 0.8 else "medium"
            }
            
            return cognitive_profile
            
        except Exception as e:
            print(f"❌ Erreur création profil cognitif: {e}")
            return {
                "learning_style": "visual",
                "preferred_pace": "moyen",
                "memory_type": "visual",
                "attention_span": "moyen",
                "problem_solving": "analytical",
                "learning_speed": "moyen",
                "confidence_level": "medium",
                "adaptability": "medium",
                "consistency": "medium"
            }
    
    def _generate_recommendations(self, performance: Dict[str, Any], level: str) -> List[Dict[str, Any]]:
        """Génère des recommandations personnalisées"""
        try:
            recommendations = []
            score_percentage = performance.get("score_percentage", 0)
            weaknesses = performance.get("weaknesses", [])
            
            # Recommandations basées sur le niveau
            if level in ["C1", "C2"]:
                recommendations.append({
                    "type": "advanced_practice",
                    "title": "Pratique avancée",
                    "description": "Travailler sur les nuances et expressions soutenues",
                    "priority": "high"
                })
            elif level in ["B1", "B2"]:
                recommendations.append({
                    "type": "intermediate_consolidation",
                    "title": "Consolidation intermédiaire",
                    "description": "Renforcer les concepts B1-B2 avant progression",
                    "priority": "high"
                })
            elif level == "A2":
                recommendations.append({
                    "type": "intermediate_progression",
                    "title": "Progression vers B1",
                    "description": "Travailler sur les concepts intermédiaires",
                    "priority": "medium"
                })
            else:
                recommendations.append({
                    "type": "basic_foundation",
                    "title": "Fondations de base",
                    "description": "Consolider les concepts A1-A2",
                    "priority": "high"
                })
            
            # Recommandations basées sur le score
            if score_percentage < 70:
                recommendations.append({
                    "type": "practice_intensive",
                    "title": "Pratique intensive",
                    "description": "Exercices quotidiens pour améliorer la maîtrise",
                    "priority": "high"
                })
            
            if score_percentage < 80:
                recommendations.append({
                    "type": "grammar_focus",
                    "title": "Focus grammaire",
                    "description": "Révision des règles grammaticales",
                    "priority": "medium"
                })
            
            # Recommandations basées sur les faiblesses
            for weakness in weaknesses[:3]:  # Limiter à 3 recommandations
                if "grammaire" in weakness.lower():
                    recommendations.append({
                        "type": "grammar_review",
                        "title": "Révision grammaticale",
                        "description": "Travail spécifique sur la grammaire",
                        "priority": "medium"
                    })
                elif "vocabulaire" in weakness.lower():
                    recommendations.append({
                        "type": "vocabulary_expansion",
                        "title": "Expansion du vocabulaire",
                        "description": "Apprentissage de nouveaux mots",
                        "priority": "medium"
                    })
            
            return recommendations[:5]  # Limiter à 5 recommandations
            
        except Exception as e:
            print(f"❌ Erreur génération recommandations: {e}")
            return [{
                "type": "general_practice",
                "title": "Pratique générale",
                "description": "Continuer la pratique régulière",
                "priority": "medium"
            }]
    
    def _calculate_stability_score(self, difficulty_progression: List[Dict]) -> float:
        """Calcule le score de stabilité de la progression"""
        try:
            if len(difficulty_progression) < 3:
                return 0.5
            
            # Analyser la progression des 3 dernières questions
            recent = difficulty_progression[-3:]
            same_difficulty = all(step["difficulty"] == recent[0]["difficulty"] for step in recent)
            
            if same_difficulty:
                return 0.9  # Très stable
            elif len(set(step["difficulty"] for step in recent)) == 2:
                return 0.6  # Modérément stable
            else:
                return 0.3  # Instable
                
        except Exception as e:
            print(f"❌ Erreur calcul stabilité: {e}")
            return 0.5
    
    def _calculate_consistency_score(self, difficulty_progression: List[Dict]) -> float:
        """Calcule le score de cohérence des réponses"""
        try:
            if len(difficulty_progression) < 5:
                return 0.5
            
            # Analyser la cohérence des réponses
            correct_answers = sum(1 for step in difficulty_progression if step.get("was_correct", False))
            total_answers = len(difficulty_progression)
            
            return correct_answers / total_answers if total_answers > 0 else 0.5
            
        except Exception as e:
            print(f"❌ Erreur calcul cohérence: {e}")
            return 0.5
    
    def _analyze_response_patterns(self, difficulty_progression: List[Dict]) -> Dict[str, int]:
        """Analyse les patterns de réponses par difficulté"""
        try:
            patterns = {
                "easy_correct": 0,
                "easy_errors": 0,
                "medium_correct": 0,
                "medium_errors": 0,
                "hard_correct": 0,
                "hard_errors": 0
            }
            
            for step in difficulty_progression:
                difficulty = step.get("difficulty", "easy")
                was_correct = step.get("was_correct", False)
                
                if difficulty in ["easy", "A0", "A1"]:
                    if was_correct:
                        patterns["easy_correct"] += 1
                    else:
                        patterns["easy_errors"] += 1
                elif difficulty in ["medium", "A2", "B1"]:
                    if was_correct:
                        patterns["medium_correct"] += 1
                    else:
                        patterns["medium_errors"] += 1
                elif difficulty in ["hard", "B2", "C1", "C2"]:
                    if was_correct:
                        patterns["hard_correct"] += 1
                    else:
                        patterns["hard_errors"] += 1
            
            return patterns
            
        except Exception as e:
            print(f"❌ Erreur analyse patterns: {e}")
            return {}
    
    def _get_max_difficulty_reached(self, difficulty_progression: List[Dict]) -> str:
        """Détermine la difficulté maximale atteinte"""
        try:
            if not difficulty_progression:
                return "easy"
            
            difficulties = [step.get("difficulty", "easy") for step in difficulty_progression]
            
            # Hiérarchie des difficultés
            difficulty_hierarchy = ["easy", "A0", "A1", "medium", "A2", "B1", "hard", "B2", "C1", "C2"]
            
            max_difficulty = "easy"
            for diff in difficulties:
                if diff in difficulty_hierarchy:
                    diff_index = difficulty_hierarchy.index(diff)
                    max_index = difficulty_hierarchy.index(max_difficulty)
                    if diff_index > max_index:
                        max_difficulty = diff
            
            return max_difficulty
            
        except Exception as e:
            print(f"❌ Erreur difficulté maximale: {e}")
            return "easy"
    
    def _calculate_confidence_score(self, score_percentage: float, stability: float, total_questions: int) -> float:
        """Calcule le score de confiance du profil"""
        try:
            # Score basé sur la performance
            performance_score = score_percentage / 100
            
            # Score basé sur la stabilité
            stability_score = stability
            
            # Score basé sur le nombre de questions
            questions_score = min(total_questions / 20, 1.0)  # Normaliser sur 20 questions
            
            # Score de confiance pondéré
            confidence = (performance_score * 0.5 + stability_score * 0.3 + questions_score * 0.2)
            
            return min(max(confidence, 0.1), 0.95)  # Limiter entre 0.1 et 0.95
            
        except Exception as e:
            print(f"❌ Erreur calcul confiance: {e}")
            return 0.5
    
    def _generate_fallback_profile(self, student_id: int) -> Dict[str, Any]:
        """Génère un profil de fallback si l'analyse échoue"""
        return {
            "student_id": student_id,
            "real_french_level": "A1",
            "confidence_score": 0.5,
            "learning_style": "visual",
            "preferred_pace": "moyen",
            "strengths": json.dumps(["Motivation", "Persévérance"]),
            "weaknesses": json.dumps(["Bases", "Pratique"]),
            "cognitive_profile": json.dumps({
                "learning_style": "visual",
                "preferred_pace": "moyen",
                "memory_type": "visual",
                "attention_span": "moyen",
                "problem_solving": "analytical",
                "learning_speed": "moyen",
                "confidence_level": "medium"
            }),
            "recommendations": json.dumps([{
                "type": "general_practice",
                "title": "Pratique générale",
                "description": "Continuer la pratique régulière",
                "priority": "medium"
            }]),
            "ai_generated": False,
            "generated_at": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    print("🧠 Service de profil intelligent créé avec succès!")
    print("Ce service génère des profils personnalisés basés sur l'analyse des performances")











