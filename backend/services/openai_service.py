import os
import openai
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        """Initialise le service OpenAI avec la clé API sécurisée."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY non trouvée dans les variables d'environnement")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Modèle plus accessible et économique
        logger.info("Service OpenAI initialisé avec succès")
    
    def generate_quiz_question(self, topic: str, difficulty: str, student_level: str) -> Dict:
        """
        Génère une question de quiz personnalisée.
        
        Args:
            topic: Sujet de la question
            difficulty: Niveau de difficulté (easy, medium, hard)
            student_level: Niveau de l'étudiant (beginner, intermediate, advanced)
        
        Returns:
            Dict contenant la question générée
        """
        try:
            prompt = f"""
            Créer une question de quiz sur {topic} niveau {difficulty} 
            pour un étudiant de niveau {student_level}.
            
            Format requis :
            Question : [question claire et précise]
            A) [option A]
            B) [option B]
            C) [option C]
            D) [option D]
            Réponse correcte : [lettre]
            Explication : [explication pédagogique]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            return self._parse_quiz_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de quiz: {str(e)}")
            return self._get_fallback_question(topic, difficulty)
    
    def create_tutor_response(self, student_context: Dict, question: str) -> str:
        """
        Crée une réponse de tuteur virtuel personnalisée.
        
        Args:
            student_context: Contexte de l'étudiant
            question: Question de l'étudiant
        
        Returns:
            Réponse du tuteur
        """
        try:
            system_prompt = f"""
            Tu es un tuteur virtuel pour un étudiant avec ce profil :
            - Niveau : {student_context.get('level', 'intermediate')}
            - Matières fortes : {student_context.get('strong_subjects', [])}
            - Matières faibles : {student_context.get('weak_subjects', [])}
            - Style d'apprentissage : {student_context.get('learning_style', 'visual')}
            
            Réponds de manière pédagogique, encourageante et adaptée au niveau de l'étudiant.
            Utilise des exemples concrets et des explications claires.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de réponse tuteur: {str(e)}")
            return "Je suis désolé, je ne peux pas répondre pour le moment. Veuillez réessayer plus tard."
    
    def analyze_student_response(self, student_answer: str, correct_answer: str) -> Dict:
        """
        Analyse une réponse d'étudiant par rapport à la réponse correcte.
        
        Args:
            student_answer: Réponse de l'étudiant
            correct_answer: Réponse correcte
        
        Returns:
            Dict avec l'analyse
        """
        try:
            prompt = f"""
            Analyse cette réponse d'étudiant par rapport à la réponse correcte :
            
            Réponse de l'étudiant : {student_answer}
            Réponse correcte : {correct_answer}
            
            Évalue :
            1. La précision (0-100%)
            2. Les points forts
            3. Les points à améliorer
            4. Un feedback constructif
            
            Format de réponse :
            Précision : [pourcentage]
            Points forts : [liste]
            Points à améliorer : [liste]
            Feedback : [texte encourageant]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de réponse: {str(e)}")
            return {
                "precision": 0,
                "points_forts": [],
                "points_amelioration": [],
                "feedback": "Analyse temporairement indisponible."
            }
    
    def _parse_quiz_response(self, response_text: str) -> Dict:
        """Parse la réponse de génération de quiz."""
        lines = response_text.split('\n')
        question_data = {
            'question': '',
            'options': [],
            'correct_answer': '',
            'explanation': ''
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('Question :'):
                question_data['question'] = line.replace('Question :', '').strip()
            elif line.startswith('A)'):
                question_data['options'].append(line[2:].strip())
            elif line.startswith('B)'):
                question_data['options'].append(line[2:].strip())
            elif line.startswith('C)'):
                question_data['options'].append(line[2:].strip())
            elif line.startswith('D)'):
                question_data['options'].append(line[2:].strip())
            elif line.startswith('Réponse correcte :'):
                question_data['correct_answer'] = line.replace('Réponse correcte :', '').strip()
            elif line.startswith('Explication :'):
                question_data['explanation'] = line.replace('Explication :', '').strip()
        
        return question_data
    
    def _parse_analysis_response(self, response_text: str) -> Dict:
        """Parse la réponse d'analyse."""
        lines = response_text.split('\n')
        analysis = {
            "precision": 0,
            "points_forts": [],
            "points_amelioration": [],
            "feedback": ""
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('Précision :'):
                try:
                    precision = line.replace('Précision :', '').strip().replace('%', '')
                    analysis["precision"] = int(precision)
                except:
                    pass
            elif line.startswith('Points forts :'):
                points = line.replace('Points forts :', '').strip()
                analysis["points_forts"] = [p.strip() for p in points.split(',')]
            elif line.startswith('Points à améliorer :'):
                points = line.replace('Points à améliorer :', '').strip()
                analysis["points_amelioration"] = [p.strip() for p in points.split(',')]
            elif line.startswith('Feedback :'):
                analysis["feedback"] = line.replace('Feedback :', '').strip()
        
        return analysis
    
    def _get_fallback_question(self, topic: str, difficulty: str) -> Dict:
        """Question de fallback en cas d'erreur API."""
        return {
            'question': f"Question de fallback sur {topic}",
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct_answer': 'A',
            'explanation': 'Question générée automatiquement.'
        }
    
    def get_usage_stats(self) -> Dict:
        """Récupère les statistiques d'utilisation de l'API."""
        try:
            # Note: Cette fonctionnalité nécessite un compte OpenAI avec accès aux statistiques
            return {
                "status": "API fonctionnelle",
                "model": self.model,
                "note": "Statistiques détaillées disponibles dans le dashboard OpenAI"
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {str(e)}")
            return {"status": "Erreur de récupération des statistiques"} 