#!/usr/bin/env python3
"""
⚙️ CONFIGURATION DU SYSTÈME D'ÉVALUATION INITIALE
Paramètres et constantes pour le système d'évaluation
"""

import os
from pathlib import Path

# ============================================================================
# 🗄️ CONFIGURATION DE LA BASE DE DONNÉES
# ============================================================================

# Chemin de la base de données
DATABASE_PATH = Path(__file__).parent / "data" / "app.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Créer le répertoire data s'il n'existe pas
DATABASE_PATH.parent.mkdir(exist_ok=True)

# ============================================================================
# 🎯 CONFIGURATION DE L'ÉVALUATION
# ============================================================================

# Nombre exact de questions par évaluation
TOTAL_QUESTIONS = 20

# Répartition des questions par difficulté
DIFFICULTY_DISTRIBUTION = {
    "easy": 7,      # 7 questions faciles
    "medium": 6,    # 6 questions moyennes  
    "hard": 7       # 7 questions difficiles
}

# Validation de la répartition
assert sum(DIFFICULTY_DISTRIBUTION.values()) == TOTAL_QUESTIONS, \
    f"La répartition des difficultés doit totaliser {TOTAL_QUESTIONS} questions"

# ============================================================================
# 📊 CONFIGURATION DES SCORES
# ============================================================================

# Points par question
POINTS_PER_QUESTION = 5
MAX_SCORE = TOTAL_QUESTIONS * POINTS_PER_QUESTION

# Seuils de niveau selon le score
LEVEL_THRESHOLDS = {
    "A1": (0, 30),      # 0-30 points
    "A2": (31, 50),     # 31-50 points
    "B1": (51, 70),     # 51-70 points
    "B2": (71, 85),     # 71-85 points
    "C1": (86, 100)     # 86-100 points
}

# ============================================================================
# 🎓 CONFIGURATION DES PROFILS D'APPRENTISSAGE
# ============================================================================

# Styles d'apprentissage possibles
LEARNING_STYLES = [
    "Autonome",      # Apprend seul, auto-motivé
    "Structuré",     # Aime les plans et programmes
    "Guidé"          # Préfère l'accompagnement
]

# Rythmes d'apprentissage possibles
LEARNING_PACES = [
    "Rapide",        # Progression rapide
    "Modéré",        # Progression équilibrée
    "Lent"           # Progression progressive
]

# ============================================================================
# ⏱️ CONFIGURATION DES TIMEOUTS
# ============================================================================

# Temps maximum par question (en secondes)
MAX_TIME_PER_QUESTION = 120  # 2 minutes

# Temps maximum total pour l'évaluation (en secondes)
MAX_TOTAL_TIME = 3600  # 1 heure

# ============================================================================
# 🔒 CONFIGURATION DE SÉCURITÉ
# ============================================================================

# Clé secrète pour les tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY", "najah-ai-secret-key-2024")

# Algorithme de hachage
ALGORITHM = "HS256"

# Durée de validité des tokens (en heures)
ACCESS_TOKEN_EXPIRE_HOURS = 24

# ============================================================================
# 🌐 CONFIGURATION DU SERVEUR
# ============================================================================

# Configuration du serveur FastAPI
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,  # Désactiver en production
    "log_level": "info"
}

# Configuration CORS
CORS_ORIGINS = [
    "http://localhost:3000",    # Frontend Next.js
    "http://localhost:3001",    # Frontend alternatif
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

# ============================================================================
# 📝 CONFIGURATION DES LOGS
# ============================================================================

# Niveau de log
LOG_LEVEL = "INFO"

# Format des logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Fichier de log
LOG_FILE = Path(__file__).parent / "logs" / "assessment.log"

# Créer le répertoire logs s'il n'existe pas
LOG_FILE.parent.mkdir(exist_ok=True)

# ============================================================================
# 🧪 CONFIGURATION DES TESTS
# ============================================================================

# Mode test
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# ID d'étudiant de test
TEST_STUDENT_ID = 999

# Base de données de test
TEST_DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'data' / 'test.db'}"

# ============================================================================
# 📊 CONFIGURATION DES MÉTRIQUES
# ============================================================================

# Activer les métriques de performance
ENABLE_METRICS = True

# Intervalle de collecte des métriques (en secondes)
METRICS_INTERVAL = 60

# ============================================================================
# 🔧 FONCTIONS UTILITAIRES
# ============================================================================

def get_level_from_score(score: float) -> str:
    """Détermine le niveau selon le score"""
    percentage = (score / MAX_SCORE) * 100
    
    for level, (min_score, max_score) in LEVEL_THRESHOLDS.items():
        if min_score <= percentage <= max_score:
            return level
    
    return "A1"  # Niveau par défaut

def get_learning_style_from_score(score: float) -> str:
    """Détermine le style d'apprentissage selon le score"""
    percentage = (score / MAX_SCORE) * 100
    
    if percentage >= 80:
        return "Autonome"
    elif percentage >= 60:
        return "Structuré"
    else:
        return "Guidé"

def get_learning_pace_from_score(score: float) -> str:
    """Détermine le rythme d'apprentissage selon le score"""
    percentage = (score / MAX_SCORE) * 100
    
    if percentage >= 75:
        return "Rapide"
    elif percentage >= 50:
        return "Modéré"
    else:
        return "Lent"

def validate_configuration():
    """Valide la configuration du système"""
    errors = []
    
    # Vérifier la répartition des questions
    if sum(DIFFICULTY_DISTRIBUTION.values()) != TOTAL_QUESTIONS:
        errors.append(f"La répartition des difficultés doit totaliser {TOTAL_QUESTIONS} questions")
    
    # Vérifier les seuils de niveau
    for level, (min_score, max_score) in LEVEL_THRESHOLDS.items():
        if min_score < 0 or max_score > 100:
            errors.append(f"Les seuils pour le niveau {level} doivent être entre 0 et 100")
    
    # Vérifier les timeouts
    if MAX_TIME_PER_QUESTION <= 0 or MAX_TOTAL_TIME <= 0:
        errors.append("Les timeouts doivent être positifs")
    
    if MAX_TOTAL_TIME < MAX_TIME_PER_QUESTION * TOTAL_QUESTIONS:
        errors.append("Le temps total doit être supérieur au temps par question × nombre de questions")
    
    if errors:
        raise ValueError(f"Erreurs de configuration:\n" + "\n".join(f"  • {error}" for error in errors))
    
    return True

# Validation automatique au chargement
if __name__ == "__main__":
    try:
        validate_configuration()
        print("✅ Configuration validée avec succès !")
        print(f"   📊 Questions totales: {TOTAL_QUESTIONS}")
        print(f"   🎯 Score maximum: {MAX_SCORE}")
        print(f"   ⏱️ Temps maximum: {MAX_TOTAL_TIME // 60} minutes")
        print(f"   🌐 Serveur: {SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        exit(1)
else:
    # Validation silencieuse en mode import
    try:
        validate_configuration()
    except ValueError:
        pass  # Ignorer les erreurs en mode import





