#!/usr/bin/env python3
"""
Script pour démarrer le serveur avec une configuration minimale
"""

import uvicorn
import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_server_simple():
    print("=== DÉMARRAGE DU SERVEUR AVEC CONFIGURATION MINIMALE ===")
    
    # Importer les modules essentiels seulement
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Créer l'app FastAPI
        app = FastAPI(title="Najah AI API", version="1.0.0")
        
        # Configuration CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3001"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Importer les routes essentielles seulement
        from api.v1 import auth, users, quiz_results, badges, messages, quizzes
        
        # Inclure les routes
        app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
        app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
        app.include_router(quiz_results.router, prefix="/api/v1/quiz_results", tags=["quiz_results"])
        app.include_router(badges.router, prefix="/api/v1/badges", tags=["badges"])
        app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
        app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["quizzes"])
        
        # Route de test
        @app.get("/")
        def read_root():
            return {"message": "Najah AI API - Configuration minimale"}
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy"}
        
        print("✅ Application FastAPI créée avec succès")
        print("✅ Routes essentielles incluses")
        print("✅ CORS configuré")
        
        # Démarrer le serveur
        print("\n🚀 Démarrage du serveur...")
        print("   URL: http://localhost:8000")
        print("   Appuyez sur Ctrl+C pour arrêter")
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("Détails de l'erreur:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server_simple() 