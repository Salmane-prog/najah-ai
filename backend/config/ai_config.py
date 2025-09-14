#!/usr/bin/env python3
"""
Configuration des services IA pour Najah AI
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class AIConfig:
    """Configuration centralisée pour les services IA"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "400"))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # HuggingFace Configuration
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HUGGINGFACE_BASE_URL = "https://api-inference.huggingface.co/models"
    
    # Modèles HuggingFace disponibles
    HUGGINGFACE_MODELS = {
        "chat": "microsoft/DialoGPT-medium",
        "text_gen": "gpt2",
        "french": "camembert-base",
        "qa": "deepset/roberta-base-squad2",
        "sentiment": "cardiffnlp/twitter-roberta-base-sentiment"
    }
    
    # Configuration des prompts IA
    FRENCH_QUIZ_PROMPTS = {
        "grammar": "Créer une question de grammaire française sur {topic} niveau {difficulty} pour un étudiant de niveau {student_level}.",
        "vocabulary": "Créer une question de vocabulaire français sur {topic} niveau {difficulty} pour un étudiant de niveau {student_level}.",
        "comprehension": "Créer une question de compréhension française sur {topic} niveau {difficulty} pour un étudiant de niveau {student_level}."
    }
    
    # Configuration des seuils d'adaptation
    ADAPTATION_THRESHOLDS = {
        "easy_to_medium": 75,      # Score minimum pour passer de facile à moyen
        "medium_to_hard": 85,      # Score minimum pour passer de moyen à difficile
        "hard_to_medium": 60,      # Score minimum pour rester en difficile
        "confidence_high": 85,     # Score de confiance élevé
        "confidence_medium": 70    # Score de confiance moyen
    }
    
    # Configuration des styles d'apprentissage
    LEARNING_STYLE_INDICATORS = {
        "visual": ["voir", "regarder", "image", "couleur", "forme"],
        "auditory": ["écouter", "entendre", "son", "parler", "discuter"],
        "kinesthetic": ["toucher", "faire", "pratiquer", "bouger", "expérimenter"]
    }
    
    @classmethod
    def is_openai_available(cls) -> bool:
        """Vérifie si OpenAI est disponible"""
        return bool(cls.OPENAI_API_KEY)
    
    @classmethod
    def is_huggingface_available(cls) -> bool:
        """Vérifie si HuggingFace est disponible"""
        return bool(cls.HUGGINGFACE_API_KEY)
    
    @classmethod
    def get_ai_status(cls) -> dict:
        """Retourne le statut des services IA"""
        return {
            "openai": cls.is_openai_available(),
            "huggingface": cls.is_huggingface_available(),
            "models": list(cls.HUGGINGFACE_MODELS.keys()),
            "adaptation_thresholds": cls.ADAPTATION_THRESHOLDS
        }
