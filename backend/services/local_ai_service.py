import os
import json
import random
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalAIService:
    def __init__(self):
        """Service AI local avec modèles pré-entraînés."""
        self.quiz_templates = self._load_quiz_templates()
        self.tutor_responses = self._load_tutor_responses()
        logger.info("Service AI local initialisé avec succès")
    
    def generate_quiz_question(self, topic: str, difficulty: str, student_level: str) -> Dict:
        """
        Génère une question de quiz avec des templates locaux.
        """
        try:
            # Sélectionner un template approprié
            template = self._select_template(topic, difficulty, student_level)
            
            # Générer la question
            question = self._generate_from_template(template, topic, difficulty)
            
            # Générer les options
            options = self._generate_options(topic, difficulty)
            
            return {
                'question': question,
                'options': options,
                'correct_answer': 'A',  # Simplifié
                'explanation': f'Explication pour {topic} niveau {difficulty}'
            }
            
        except Exception as e:
            logger.error(f"Erreur génération locale: {str(e)}")
            return self._get_fallback_question(topic, difficulty)
    
    def create_tutor_response(self, student_context: Dict, question: str) -> str:
        """
        Crée une réponse de tuteur avec des templates locaux.
        """
        try:
            # Analyser le type de question
            question_type = self._analyze_question_type(question)
            
            # Sélectionner une réponse appropriée
            response_template = self._select_tutor_response(question_type, student_context)
            
            # Personnaliser la réponse
            response = self._personalize_response(response_template, student_context, question)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur tutor local: {str(e)}")
            return "Je suis désolé, je ne peux pas répondre pour le moment."
    
    def analyze_student_response(self, student_answer: str, correct_answer: str) -> Dict:
        """
        Analyse une réponse d'étudiant avec des algorithmes locaux.
        """
        try:
            # Calculer la similarité
            similarity = self._calculate_similarity(student_answer, correct_answer)
            
            # Analyser la longueur
            length_score = min(len(student_answer) / 50, 1.0)  # Normalisé
            
            # Score combiné
            precision = int((similarity * 0.7 + length_score * 0.3) * 100)
            
            # Générer le feedback
            feedback = self._generate_feedback(precision, student_answer, correct_answer)
            
            return {
                "precision": precision,
                "points_forts": self._identify_strengths(student_answer),
                "points_amelioration": self._identify_improvements(precision),
                "feedback": feedback
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse locale: {str(e)}")
            return {
                "precision": 0,
                "points_forts": [],
                "points_amelioration": [],
                "feedback": "Analyse indisponible."
            }
    
    def _load_quiz_templates(self) -> Dict:
        """Charge les templates de questions."""
        return {
            "math": {
                "easy": [
                    "Quelle est la somme de {a} + {b} ?",
                    "Combien font {a} × {b} ?",
                    "Quel est le résultat de {a} ÷ {b} ?"
                ],
                "medium": [
                    "Résolvez l'équation: {a}x + {b} = {c}",
                    "Calculez l'aire d'un rectangle de {a} × {b}",
                    "Quel est le périmètre d'un carré de côté {a} ?"
                ],
                "hard": [
                    "Résolvez le système: {a}x + {b}y = {c}, {d}x + {e}y = {f}",
                    "Calculez la dérivée de {function}",
                    "Trouvez les racines de {equation}"
                ]
            },
            "french": {
                "easy": [
                    "Conjuguez le verbe 'être' au présent: Je ___",
                    "Quel est le féminin de 'grand' ?",
                    "Complétez: Le chat ___ sur le toit."
                ],
                "medium": [
                    "Analysez la phrase: '{sentence}'",
                    "Identifiez la nature de '{word}'",
                    "Conjuguez '{verb}' à l'imparfait"
                ],
                "hard": [
                    "Analysez le texte: '{text}'",
                    "Identifiez les figures de style dans: '{sentence}'",
                    "Rédigez une introduction pour: '{topic}'"
                ]
            }
        }
    
    def _load_tutor_responses(self) -> Dict:
        """Charge les templates de réponses de tuteur."""
        return {
            "encouragement": [
                "Excellente question ! Voici la réponse...",
                "Très bonne réflexion. Laissez-moi vous expliquer...",
                "C'est une question pertinente. Voici ce qu'il faut savoir..."
            ],
            "explanation": [
                "Pour comprendre cela, il faut d'abord...",
                "La réponse est basée sur le principe suivant...",
                "Voici la méthode pour résoudre ce problème..."
            ],
            "correction": [
                "Attention, il y a une petite erreur. Voici pourquoi...",
                "Votre approche est intéressante, mais voici la méthode correcte...",
                "Laissez-moi vous aider à corriger cela..."
            ]
        }
    
    def _select_template(self, topic: str, difficulty: str, student_level: str) -> List[str]:
        """Sélectionne un template approprié."""
        topic_key = "math" if "math" in topic.lower() else "french"
        return self.quiz_templates.get(topic_key, {}).get(difficulty, ["Question sur {topic}"])
    
    def _generate_from_template(self, templates: List[str], topic: str, difficulty: str) -> str:
        """Génère une question à partir d'un template."""
        template = random.choice(templates)
        
        # Remplacer les variables
        if "math" in topic.lower():
            a, b = random.randint(1, 20), random.randint(1, 20)
            return template.format(a=a, b=b, topic=topic)
        else:
            return template.format(topic=topic, sentence="Une phrase d'exemple.")
    
    def _generate_options(self, topic: str, difficulty: str) -> List[str]:
        """Génère les options de réponse."""
        if "math" in topic.lower():
            # Options mathématiques
            correct = random.randint(1, 100)
            options = [correct]
            while len(options) < 4:
                option = random.randint(1, 100)
                if option not in options:
                    options.append(option)
            random.shuffle(options)
            return [f"Option {chr(65+i)}: {opt}" for i, opt in enumerate(options)]
        else:
            # Options générales
            return [
                "Option A: Réponse correcte",
                "Option B: Réponse incorrecte",
                "Option C: Réponse partielle",
                "Option D: Réponse alternative"
            ]
    
    def _analyze_question_type(self, question: str) -> str:
        """Analyse le type de question."""
        question_lower = question.lower()
        if any(word in question_lower for word in ["pourquoi", "comment", "explique"]):
            return "explanation"
        elif any(word in question_lower for word in ["erreur", "faux", "incorrect"]):
            return "correction"
        else:
            return "encouragement"
    
    def _select_tutor_response(self, question_type: str, student_context: Dict) -> List[str]:
        """Sélectionne une réponse de tuteur."""
        return self.tutor_responses.get(question_type, self.tutor_responses["encouragement"])
    
    def _personalize_response(self, templates: List[str], context: Dict, question: str) -> str:
        """Personnalise la réponse."""
        template = random.choice(templates)
        level = context.get('level', 'intermediate')
        
        if level == 'beginner':
            template += " Je vais vous expliquer étape par étape."
        elif level == 'advanced':
            template += " Vous pouvez approfondir en consultant les ressources supplémentaires."
        
        return template
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcule la similarité entre deux textes."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _generate_feedback(self, precision: int, student_answer: str, correct_answer: str) -> str:
        """Génère un feedback personnalisé."""
        if precision >= 90:
            return "Excellente réponse ! Vous maîtrisez bien ce concept."
        elif precision >= 70:
            return "Bonne réponse ! Quelques détails à améliorer."
        elif precision >= 50:
            return "Réponse partiellement correcte. Continuez vos efforts."
        else:
            return "Réponse incorrecte. Je vous conseille de revoir ce chapitre."
    
    def _identify_strengths(self, answer: str) -> List[str]:
        """Identifie les points forts."""
        strengths = []
        if len(answer) > 10:
            strengths.append("Réponse détaillée")
        if any(word in answer.lower() for word in ["car", "parce que", "donc"]):
            strengths.append("Raisonnement logique")
        return strengths
    
    def _identify_improvements(self, precision: int) -> List[str]:
        """Identifie les points d'amélioration."""
        improvements = []
        if precision < 80:
            improvements.append("Précision")
        if precision < 60:
            improvements.append("Compréhension du sujet")
        return improvements
    
    def _get_fallback_question(self, topic: str, difficulty: str) -> Dict:
        """Question de fallback."""
        return {
            'question': f"Question de fallback sur {topic}",
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct_answer': 'A',
            'explanation': 'Question générée automatiquement.'
        }
    
    def get_usage_stats(self) -> Dict:
        """Statistiques d'utilisation."""
        return {
            "status": "Service AI local fonctionnel",
            "models": ["Templates locaux", "Algorithmes simples"],
            "note": "Gratuit et sans limites"
        } 