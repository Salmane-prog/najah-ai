#!/usr/bin/env python3
"""
Script de diagnostic pour vérifier l'enregistrement des routers
"""

from app import fastapi_app
import json

def diagnose_routers():
    """Diagnostique l'état des routers enregistrés"""
    print("🔍 DIAGNOSTIC DES ROUTERS")
    print("=" * 50)
    
    # Vérifier les routers enregistrés
    print("📋 Routers enregistrés dans l'application:")
    for route in fastapi_app.routes:
        if hasattr(route, 'path'):
            print(f"   ✅ {route.path} - {getattr(route, 'tags', ['No tags'])}")
    
    print(f"\n📊 Total des routes: {len(fastapi_app.routes)}")
    
    # Vérifier les imports spécifiques
    print("\n🔍 Vérification des imports...")
    
    try:
        from api.v1 import teacher_dashboard
        print("   ✅ teacher_dashboard importé avec succès")
        print(f"   📍 Router: {teacher_dashboard.router}")
        print(f"   🏷️ Tags: {teacher_dashboard.router.tags}")
        print(f"   🔗 Préfixe: {teacher_dashboard.router.prefix}")
    except Exception as e:
        print(f"   ❌ Erreur import teacher_dashboard: {e}")
    
    try:
        from api.v1 import ai_models
        print("   ✅ ai_models importé avec succès")
        print(f"   📍 Router: {ai_models.router}")
        print(f"   🏷️ Tags: {ai_models.router.tags}")
        print(f"   🔗 Préfixe: {ai_models.router.prefix}")
    except Exception as e:
        print(f"   ❌ Erreur import ai_models: {e}")
    
    try:
        from api.v1 import data_collection
        print("   ✅ data_collection importé avec succès")
        print(f"   📍 Router: {data_collection.router}")
        print(f"   🏷️ Tags: {data_collection.router.tags}")
        print(f"   🔗 Préfixe: {data_collection.router.prefix}")
    except Exception as e:
        print(f"   ❌ Erreur import data_collection: {e}")
    
    try:
        from api.v1 import training_sessions
        print("   ✅ training_sessions importé avec succès")
        print(f"   📍 Router: {training_sessions.router}")
        print(f"   🏷️ Tags: {training_sessions.router.tags}")
        print(f"   🔗 Préfixe: {training_sessions.router.prefix}")
    except Exception as e:
        print(f"   ❌ Erreur import training_sessions: {e}")
    
    try:
        from api.v1 import adaptive_evaluation
        print("   ✅ adaptive_evaluation importé avec succès")
        print(f"   📍 Router: {adaptive_evaluation.router}")
        print(f"   🏷️ Tags: {adaptive_evaluation.router.tags}")
        print(f"   🔗 Préfixe: {adaptive_evaluation.router.prefix}")
    except Exception as e:
        print(f"   ❌ Erreur import adaptive_evaluation: {e}")
    
    # Vérifier la structure de l'application
    print("\n🏗️ Structure de l'application:")
    print(f"   📱 Titre: {fastapi_app.title}")
    print(f"   📋 Version: {fastapi_app.version}")
    print(f"   🔗 Base URL: {getattr(fastapi_app, 'root_path', 'Non défini')}")
    
    print("\n🏁 Diagnostic terminé!")

if __name__ == "__main__":
    diagnose_routers()


























