#!/usr/bin/env python3
"""
Configuration de l'application principale
Intègre tous les endpoints et services avancés
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

# Import des endpoints
from api.v1.advanced_analytics import router as advanced_analytics_router
from real_analytics_endpoints import router as real_analytics_router

# Configuration de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    print("🚀 Démarrage de Najah AI Backend...")
    print("📊 Services disponibles:")
    print("   - Analytics en temps réel")
    print("   - Analyse cognitive avancée")
    print("   - Moteur IRT")
    print("   - Banque de questions étendue")
    print("   - Dashboard avancé")
    
    yield
    
    print("🛑 Arrêt de Najah AI Backend...")

# Création de l'application FastAPI
app = FastAPI(
    title="Najah AI - Plateforme Éducative Intelligente",
    description="""
    🎓 Plateforme éducative avancée avec:
    
    ## 🧠 Analyse Cognitive Avancée
    - Détection de patterns d'apprentissage
    - Analyse des temps de réponse
    - Profils cognitifs personnalisés
    
    ## 📈 Moteur IRT (Item Response Theory)
    - Adaptation intelligente de la difficulté
    - Prédiction de performance
    - Gestion de la charge cognitive
    
    ## 🗃️ Banque de Questions Étendue
    - 100+ questions avec métadonnées riches
    - Support multilingue
    - Catégorisation avancée
    
    ## 📊 Dashboard Analytics Avancé
    - Visualisations interactives
    - Comparaisons de classe
    - Tendances temporelles
    - Recommandations IA
    
    ## 🔄 Analytics en Temps Réel
    - Suivi des sessions d'évaluation
    - Métriques de performance
    - Alertes intelligentes
    """,
    version="2.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
print("🔧 Inclusion des endpoints...")

# Endpoints d'analytics en temps réel
app.include_router(real_analytics_router, prefix="/api/v1")

# Endpoints avancés
app.include_router(advanced_analytics_router, prefix="/api/v1")

print("✅ Tous les endpoints ont été inclus!")

# Endpoint de santé global
@app.get("/health")
async def health_check():
    """Vérifier la santé de tous les services"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "real_time_analytics": "active",
            "advanced_cognitive_analysis": "active",
            "irt_engine": "active",
            "extended_question_bank": "active",
            "advanced_dashboard": "active"
        },
        "endpoints": {
            "real_time": "/api/v1/analytics/*",
            "advanced": "/api/v1/advanced/*",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Endpoint racine
@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🚀 Najah AI - Plateforme Éducative Intelligente",
        "version": "2.0.0",
        "description": "Système d'évaluation et d'analytics avancé avec IA",
        "features": [
            "🧠 Analyse cognitive avancée",
            "📈 Moteur IRT adaptatif",
            "🗃️ Banque de questions étendue",
            "📊 Dashboard analytics avancé",
            "🔄 Analytics en temps réel"
        ],
        "documentation": "/docs",
        "health": "/health"
    }

# Configuration pour le développement
if __name__ == "__main__":
    print("🚀 Démarrage du serveur Najah AI...")
    print("=" * 60)
    print("📚 Plateforme Éducative Intelligente v2.0.0")
    print("=" * 60)
    
    # Vérifier les variables d'environnement
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🌐 Serveur démarré sur {host}:{port}")
    print(f"🔄 Mode reload: {'activé' if reload else 'désactivé'}")
    print(f"📖 Documentation: http://{host}:{port}/docs")
    print(f"🏥 Santé: http://{host}:{port}/health")
    
    uvicorn.run(
        "app_config:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )















