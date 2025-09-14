import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Import des services
from .openai_service import OpenAIService
from .huggingface_service import HuggingFaceService
from .local_ai_service import LocalAIService

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAIService:
    def __init__(self):
        """Service multi-provider avec fallback intelligent."""
        self.providers = []
        self.current_provider_index = 0
        
        # Initialiser les providers disponibles
        self._initialize_providers()
        logger.info(f"Service Multi-AI initialisé avec {len(self.providers)} providers")
    
    def _initialize_providers(self):
        """Initialise les providers disponibles."""
        # 1. OpenAI (si disponible)
        try:
            if os.getenv("OPENAI_API_KEY"):
                self.providers.append(("OpenAI", OpenAIService()))
                logger.info("✅ OpenAI provider ajouté")
        except Exception as e:
            logger.warning(f"❌ OpenAI non disponible: {e}")
        
        # 2. Hugging Face (si disponible)
        try:
            if os.getenv("HUGGINGFACE_API_KEY"):
                self.providers.append(("HuggingFace", HuggingFaceService()))
                logger.info("✅ HuggingFace provider ajouté")
        except Exception as e:
            logger.warning(f"❌ HuggingFace non disponible: {e}")
        
        # 3. Local AI (toujours disponible)
        try:
            self.providers.append(("Local", LocalAIService()))
            logger.info("✅ Local AI provider ajouté")
        except Exception as e:
            logger.error(f"❌ Local AI non disponible: {e}")
    
    def generate_quiz_question(self, topic: str, difficulty: str, student_level: str) -> Dict:
        """
        Génère une question avec fallback intelligent.
        """
        for i, (provider_name, provider) in enumerate(self.providers):
            try:
                logger.info(f"🧪 Tentative avec {provider_name}")
                result = provider.generate_quiz_question(topic, difficulty, student_level)
                
                # Vérifier que le résultat est valide
                if self._is_valid_quiz_result(result):
                    logger.info(f"✅ Succès avec {provider_name}")
                    return {
                        **result,
                        "generated_by": provider_name
                    }
                else:
                    logger.warning(f"⚠️ Résultat invalide de {provider_name}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur avec {provider_name}: {e}")
                continue
        
        # Fallback final
        logger.warning("⚠️ Utilisation du fallback final")
        return {
            'question': f"Question de fallback sur {topic}",
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct_answer': 'A',
            'explanation': 'Question générée automatiquement.',
            'generated_by': 'Fallback'
        }
    
    def create_tutor_response(self, student_context: Dict, question: str) -> str:
        """
        Crée une réponse de tuteur avec fallback.
        """
        for provider_name, provider in self.providers:
            try:
                logger.info(f"🧪 Tentative tutor avec {provider_name}")
                result = provider.create_tutor_response(student_context, question)
                
                if result and len(result) > 10:  # Réponse valide
                    logger.info(f"✅ Tutor succès avec {provider_name}")
                    return f"[{provider_name}] {result}"
                    
            except Exception as e:
                logger.error(f"❌ Erreur tutor avec {provider_name}: {e}")
                continue
        
        return "Je suis désolé, je ne peux pas répondre pour le moment."
    
    def analyze_student_response(self, student_answer: str, correct_answer: str) -> Dict:
        """
        Analyse une réponse avec fallback.
        """
        for provider_name, provider in self.providers:
            try:
                logger.info(f"🧪 Tentative analyse avec {provider_name}")
                result = provider.analyze_student_response(student_answer, correct_answer)
                
                if self._is_valid_analysis_result(result):
                    logger.info(f"✅ Analyse succès avec {provider_name}")
                    return {
                        **result,
                        "analyzed_by": provider_name
                    }
                    
            except Exception as e:
                logger.error(f"❌ Erreur analyse avec {provider_name}: {e}")
                continue
        
        # Fallback final
        return {
            "precision": 0,
            "points_forts": [],
            "points_amelioration": [],
            "feedback": "Analyse temporairement indisponible.",
            "analyzed_by": "Fallback"
        }
    
    def _is_valid_quiz_result(self, result: Dict) -> bool:
        """Vérifie si un résultat de quiz est valide."""
        required_fields = ['question', 'options', 'correct_answer']
        return all(field in result for field in required_fields) and len(result.get('options', [])) >= 2
    
    def _is_valid_analysis_result(self, result: Dict) -> bool:
        """Vérifie si un résultat d'analyse est valide."""
        required_fields = ['precision', 'feedback']
        return all(field in result for field in required_fields)
    
    def get_usage_stats(self) -> Dict:
        """Statistiques d'utilisation de tous les providers."""
        stats = {
            "status": "Multi-AI Service fonctionnel",
            "providers": [],
            "total_providers": len(self.providers)
        }
        
        for provider_name, provider in self.providers:
            try:
                provider_stats = provider.get_usage_stats()
                stats["providers"].append({
                    "name": provider_name,
                    "status": provider_stats.get("status", "Inconnu"),
                    "models": provider_stats.get("models", [])
                })
            except Exception as e:
                stats["providers"].append({
                    "name": provider_name,
                    "status": f"Erreur: {str(e)}",
                    "models": []
                })
        
        return stats
    
    def get_available_providers(self) -> List[str]:
        """Retourne la liste des providers disponibles."""
        return [name for name, _ in self.providers]
    
    def test_provider(self, provider_name: str) -> bool:
        """Teste un provider spécifique."""
        for name, provider in self.providers:
            if name.lower() == provider_name.lower():
                try:
                    # Test simple
                    result = provider.generate_quiz_question("test", "easy", "beginner")
                    return self._is_valid_quiz_result(result)
                except Exception as e:
                    logger.error(f"Test {provider_name} échoué: {e}")
                    return False
        return False 