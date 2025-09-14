#!/usr/bin/env python3
"""
Script pour démarrer le serveur backend avec toutes les nouvelles fonctionnalités
- Gestion des Devoirs
- Calendrier Avancé
- Collaboration
- IA Avancée
- Rapports Détaillés
"""

import uvicorn
import os
import sys
from pathlib import Path

def start_server():
    """Démarrer le serveur backend"""
    
    print("🚀 Démarrage du serveur backend Najah AI...")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    current_dir = Path(__file__).parent
    if not (current_dir / "app.py").exists():
        print("❌ Erreur: app.py non trouvé dans le répertoire courant")
        print(f"   Répertoire actuel: {current_dir}")
        print("   Assurez-vous d'exécuter ce script depuis le dossier backend/")
        return False
    
    print(f"📁 Répertoire de travail: {current_dir}")
    
    # Vérifier que la base de données existe
    db_path = current_dir.parent / "data" / "app.db"
    if not db_path.exists():
        print(f"❌ Erreur: Base de données non trouvée: {db_path}")
        print("   Exécutez d'abord create_missing_tables.py")
        return False
    
    print(f"🗄️ Base de données trouvée: {db_path}")
    
    # Configuration du serveur
    host = "0.0.0.0"  # Accessible depuis n'importe quelle interface
    port = 8000
    reload = True  # Rechargement automatique en développement
    
    print(f"🌐 Configuration du serveur:")
    print(f"   - Host: {host}")
    print(f"   - Port: {port}")
    print(f"   - Rechargement automatique: {'Activé' if reload else 'Désactivé'}")
    
    # Vérifier les dépendances
    print("\n🔍 Vérification des dépendances...")
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI non installé")
        return False
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy non installé")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn non installé")
        return False
    
    # Vérifier que l'application peut être importée
    print("\n🔧 Vérification de l'application...")
    
    try:
        # Ajouter le répertoire courant au path Python
        sys.path.insert(0, str(current_dir))
        
        # Importer l'application
        from app import app
        print("✅ Application FastAPI importée avec succès")
        
        # Vérifier les routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"✅ {len(routes)} routes configurées")
        
        # Afficher quelques routes importantes
        important_routes = [
            "/api/v1/calendar/events",
            "/api/v1/collaboration/study-groups",
            "/api/v1/ai_advanced/recommendations",
            "/api/v1/homework/assignments",
            "/api/v1/ai_advanced/analytics/performance"
        ]
        
        print("\n🔗 Routes importantes disponibles:")
        for route in important_routes:
            if any(route in r for r in routes):
                print(f"   ✅ {route}")
            else:
                print(f"   ❌ {route}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import de l'application: {e}")
        return False
    
    print("\n🎯 Démarrage du serveur...")
    print("   - Appuyez sur Ctrl+C pour arrêter le serveur")
    print("   - Le serveur sera accessible sur http://localhost:8000")
    print("   - Documentation API: http://localhost:8000/docs")
    print("   - Documentation alternative: http://localhost:8000/redoc")
    print("=" * 60)
    
    try:
        # Démarrer le serveur
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
        return True
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage du serveur: {e}")
        return False

if __name__ == "__main__":
    success = start_server()
    
    if success:
        print("\n✅ Serveur arrêté proprement")
    else:
        print("\n❌ Erreur lors de l'exécution du serveur")
        print("\n🔧 Actions recommandées:")
        print("   1. Vérifier que toutes les dépendances sont installées")
        print("   2. Vérifier que la base de données existe")
        print("   3. Vérifier que app.py est accessible")
        print("   4. Vérifier les logs d'erreur pour plus de détails")




