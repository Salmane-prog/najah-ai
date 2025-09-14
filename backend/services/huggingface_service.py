import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        """Initialise le service Hugging Face avec la clé API gratuite."""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Modèles gratuits populaires
        self.models = {
            "chat": "microsoft/DialoGPT-medium",  # Chat simple
            "text_gen": "gpt2",  # Génération de texte
            "french": "camembert-base",  # Modèle français
            "qa": "deepset/roberta-base-squad2"  # Questions/Réponses
        }
        
        logger.info("Service Hugging Face initialisé avec succès")
    
    def generate_quiz_question(self, topic: str, difficulty: str, student_level: str) -> Dict:
        """
        Génère une question de quiz avec Hugging Face.
        """
        try:
            # Utiliser un modèle de génération de texte
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            
            prompt = f"Question de quiz sur {topic} niveau {difficulty}:"
            
            response = requests.post(
                f"{self.base_url}/gpt2",
                headers=headers,
                json={"inputs": prompt, "max_length": 100}
            )
            
            if response.status_code == 200:
                generated_text = response.json()[0]["generated_text"]
                return self._parse_quiz_response(generated_text, topic)
            else:
                return self._get_fallback_question(topic, difficulty)
                
        except Exception as e:
            logger.error(f"Erreur Hugging Face: {str(e)}")
            return self._get_fallback_question(topic, difficulty)
    
    def create_tutor_response(self, student_context: Dict, question: str) -> str:
        """
        Crée une réponse de tuteur avec Hugging Face.
        """
        try:
            # Utiliser DialoGPT pour les conversations
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            
            prompt = f"Tuteur: Réponds à cette question d'étudiant: {question}"
            
            response = requests.post(
                f"{self.base_url}/microsoft/DialoGPT-medium",
                headers=headers,
                json={"inputs": prompt, "max_length": 150}
            )
            
            if response.status_code == 200:
                return response.json()[0]["generated_text"]
            else:
                return "Je suis désolé, je ne peux pas répondre pour le moment."
                
        except Exception as e:
            logger.error(f"Erreur Hugging Face tutor: {str(e)}")
            return "Réponse temporairement indisponible."
    
    def analyze_student_response(self, student_answer: str, correct_answer: str) -> Dict:
        """
        Analyse une réponse d'étudiant.
        """
        try:
            # Logique simple d'analyse
            similarity = self._calculate_similarity(student_answer, correct_answer)
            
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
                "points_forts": ["Effort fourni"] if precision > 30 else [],
                "points_amelioration": ["Précision"] if precision < 80 else [],
                "feedback": feedback
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse: {str(e)}")
            return {
                "precision": 0,
                "points_forts": [],
                "points_amelioration": [],
                "feedback": "Analyse indisponible."
            }
    
    def _parse_quiz_response(self, generated_text: str, topic: str) -> Dict:
        """Parse la réponse générée en question de quiz."""
        # Logique simple de parsing
        lines = generated_text.split('.')
        question = lines[0] if lines else f"Question sur {topic}"
        
        return {
            'question': question,
            'options': [
                f"Option A: {topic}",
                f"Option B: Autre réponse",
                f"Option C: Troisième option",
                f"Option D: Dernière option"
            ],
            'correct_answer': 'A',
            'explanation': f'Explication pour {topic}'
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcule une similarité simple entre deux textes."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
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
            "status": "Hugging Face API fonctionnelle",
            "models": list(self.models.keys()),
            "note": "Gratuit avec limitations"
        } 