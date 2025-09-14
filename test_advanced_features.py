#!/usr/bin/env python3
"""
Script pour tester les nouvelles fonctionnalités avancées du dashboard professeur
"""

import requests
import json
from typing import Dict, List, Any

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEACHER_CREDENTIALS = {
    "username": "marie.dubois@najah.ai",
    "password": "salmane123@"
}

def get_auth_token() -> str:
    """Obtenir un token d'authentification pour un professeur"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=TEACHER_CREDENTIALS)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Erreur d'authentification: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def test_endpoint(method: str, endpoint: str, token: str = None, data: Dict = None) -> Dict:
    """Tester un endpoint"""
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"{response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_teacher_messaging(token: str):
    """Tester le système de messagerie professeur"""
    print("\n🔍 Test du système de messagerie professeur...")
    
    # Test 1: Récupérer les conversations
    result = test_endpoint("GET", "/teacher_messaging/conversations", token)
    if result["success"]:
        print("✅ Conversations récupérées avec succès")
        conversations = result["data"].get("conversations", [])
        print(f"   📧 {len(conversations)} conversations trouvées")
    else:
        print(f"❌ Erreur: {result['error']}")

def test_teacher_schedule(token: str):
    """Tester le système de planification"""
    print("\n📅 Test du système de planification...")
    
    # Test 1: Récupérer le planning
    result = test_endpoint("GET", "/teacher_schedule/schedule", token)
    if result["success"]:
        print("✅ Planning récupéré avec succès")
        events = result["data"].get("events", [])
        print(f"   📅 {len(events)} événements trouvés")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 2: Récupérer les événements à venir
    result = test_endpoint("GET", "/teacher_schedule/schedule/upcoming", token)
    if result["success"]:
        print("✅ Événements à venir récupérés avec succès")
        upcoming = result["data"].get("upcoming_events", [])
        print(f"   🚀 {len(upcoming)} événements à venir")
    else:
        print(f"❌ Erreur: {result['error']}")

def test_auto_correction(token: str):
    """Tester le système de correction automatique"""
    print("\n✅ Test du système de correction automatique...")
    
    # Test 1: Récupérer les corrections en attente
    result = test_endpoint("GET", "/auto_correction/pending-corrections", token)
    if result["success"]:
        print("✅ Corrections en attente récupérées avec succès")
        pending = result["data"].get("pending_corrections", [])
        print(f"   📝 {len(pending)} corrections en attente")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 2: Statistiques de correction
    result = test_endpoint("GET", "/auto_correction/correction-stats", token)
    if result["success"]:
        print("✅ Statistiques de correction récupérées avec succès")
        stats = result["data"]
        print(f"   📊 Total: {stats.get('total_results', 0)}")
        print(f"   ⏳ En attente: {stats.get('pending_corrections', 0)}")
        print(f"   ✅ Corrigés: {stats.get('corrected_results', 0)}")
    else:
        print(f"❌ Erreur: {result['error']}")

def test_remediation(token: str):
    """Tester le système de remédiation"""
    print("\n🎯 Test du système de remédiation...")
    
    # Test 1: Récupérer les ressources de remédiation
    result = test_endpoint("GET", "/remediation/remediation-resources", token)
    if result["success"]:
        print("✅ Ressources de remédiation récupérées avec succès")
        data = result["data"]
        contents = data.get("contents", [])
        paths = data.get("learning_paths", [])
        print(f"   📚 {len(contents)} contenus de remédiation")
        print(f"   🛤️ {len(paths)} parcours de remédiation")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 2: Statistiques de remédiation
    result = test_endpoint("GET", "/remediation/remediation-stats", token)
    if result["success"]:
        print("✅ Statistiques de remédiation récupérées avec succès")
        stats = result["data"]
        print(f"   📋 Total plans: {stats.get('total_plans', 0)}")
        print(f"   🔄 Plans actifs: {stats.get('active_plans', 0)}")
        print(f"   ✅ Plans complétés: {stats.get('completed_plans', 0)}")
    else:
        print(f"❌ Erreur: {result['error']}")

def test_teacher_collaboration(token: str):
    """Tester le système de collaboration entre professeurs"""
    print("\n🤝 Test du système de collaboration...")
    
    # Test 1: Récupérer les ressources partagées
    result = test_endpoint("GET", "/teacher_collaboration/shared-resources", token)
    if result["success"]:
        print("✅ Ressources partagées récupérées avec succès")
        data = result["data"]
        quizzes = data.get("shared_quizzes", [])
        contents = data.get("shared_contents", [])
        print(f"   📝 {len(quizzes)} quiz partagés")
        print(f"   📚 {len(contents)} contenus partagés")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 2: Statistiques de collaboration
    result = test_endpoint("GET", "/teacher_collaboration/collaboration-stats", token)
    if result["success"]:
        print("✅ Statistiques de collaboration récupérées avec succès")
        stats = result["data"]
        shared = stats.get("shared_resources", {})
        downloads = stats.get("downloads", {})
        ratings = stats.get("ratings", {})
        print(f"   📤 Ressources partagées: {shared.get('total', 0)}")
        print(f"   📥 Total téléchargements: {downloads.get('total_downloads', 0)}")
        print(f"   ⭐ Note moyenne: {ratings.get('average_rating', 0)}")
    else:
        print(f"❌ Erreur: {result['error']}")

def test_advanced_analytics(token: str):
    """Tester les analytics avancés"""
    print("\n📊 Test des analytics avancés...")
    
    # Test 1: Prédictions de performance
    result = test_endpoint("GET", "/advanced_analytics/performance-predictions", token)
    if result["success"]:
        print("✅ Prédictions de performance récupérées avec succès")
        data = result["data"]
        predictions = data.get("predictions", [])
        print(f"   🔮 {len(predictions)} prédictions générées")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 2: Détection des difficultés
    result = test_endpoint("GET", "/advanced_analytics/difficulty-detection", token)
    if result["success"]:
        print("✅ Détection des difficultés récupérée avec succès")
        data = result["data"]
        analysis = data.get("difficulties_analysis", [])
        print(f"   🎯 {len(analysis)} analyses de difficultés")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 3: Recommandations d'enseignement
    result = test_endpoint("GET", "/advanced_analytics/teaching-recommendations", token)
    if result["success"]:
        print("✅ Recommandations d'enseignement récupérées avec succès")
        data = result["data"]
        recommendations = data.get("teaching_recommendations", [])
        print(f"   💡 {len(recommendations)} recommandations générées")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    # Test 4: Comparaison inter-classes
    result = test_endpoint("GET", "/advanced_analytics/inter-class-comparison", token)
    if result["success"]:
        print("✅ Comparaison inter-classes récupérée avec succès")
        data = result["data"]
        comparison = data.get("class_comparison", [])
        print(f"   📈 {len(comparison)} classes comparées")
    else:
        print(f"❌ Erreur: {result['error']}")

def main():
    """Fonction principale de test"""
    print("🚀 Test des fonctionnalités avancées du dashboard professeur")
    print("=" * 60)
    
    # Obtenir le token d'authentification
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Authentification réussie")
    
    # Tester toutes les nouvelles fonctionnalités
    test_teacher_messaging(token)
    test_teacher_schedule(token)
    test_auto_correction(token)
    test_remediation(token)
    test_teacher_collaboration(token)
    test_advanced_analytics(token)
    
    print("\n" + "=" * 60)
    print("🎉 Tests terminés !")
    print("📋 Résumé des fonctionnalités testées:")
    print("   ✅ Système de messagerie professeur-élève")
    print("   ✅ Planification de cours et calendrier")
    print("   ✅ Correction automatique des quiz")
    print("   ✅ Système de remédiation personnalisé")
    print("   ✅ Collaboration entre professeurs")
    print("   ✅ Analytics avancés avec prédictions IA")
    print("   ✅ Détection automatique des difficultés")
    print("   ✅ Recommandations d'enseignement personnalisées")
    print("   ✅ Comparaison inter-classes")

if __name__ == "__main__":
    main() 