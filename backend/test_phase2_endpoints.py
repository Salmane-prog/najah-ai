#!/usr/bin/env python3
"""
Script pour tester les endpoints de la Phase 2: Tests Adaptatifs et Évaluation
"""
import requests
import json

BASE_URL = "http://localhost:8000"
token = None

def get_auth_token():
    """Obtenir le token d'authentification"""
    global token
    
    # Utiliser les bonnes informations d'authentification
    try:
        print(f"🔐 Tentative avec marie.dubois@najah.ai...")
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "marie.dubois@najah.ai",
            "password": "salmane123@"
        })
        
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Réponse: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Authentification réussie avec marie.dubois@najah.ai")
            return token
        else:
            print(f"❌ Échec avec marie.dubois@najah.ai: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    return None

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Tester un endpoint"""
    global token
    
    if not token:
        print("❌ Pas de token d'authentification")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ {description}: {len(result) if isinstance(result, list) else 'OK'}")
            if isinstance(result, list) and len(result) > 0:
                print(f"   📊 Premier élément: {result[0]}")
            return True
        else:
            print(f"❌ {description}: {response.status_code}")
            print(f"   📝 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {description}: Erreur - {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test des endpoints Phase 2: Tests Adaptatifs et Évaluation")
    print("=" * 60)
    
    # 1. Authentification
    print("\n🔐 Test d'authentification...")
    if not get_auth_token():
        print("❌ Impossible de s'authentifier")
        return
    
    # 2. Tests Phase 2.1: Tests Adaptatifs
    print("\n🧠 Phase 2.1: Tests Adaptatifs")
    print("-" * 40)
    test_endpoint("/api/v1/ai/analyze-student/4", description="Analyse cognitive étudiant")
    test_endpoint("/api/v1/ai/predict-success/4", description="Prédiction de succès")
    test_endpoint("/api/v1/ai/recommend-content/4", description="Recommandations adaptatives")
    test_endpoint("/api/v1/ai/class-insights/1", description="Insights de classe")
    
    # 3. Tests Phase 2.2: Algorithmes de Difficulté Adaptative
    print("\n⚡ Phase 2.2: Algorithmes de Difficulté Adaptative")
    print("-" * 40)
    test_endpoint("/api/v1/ai-unified/real-time-adaptation", method="POST", 
                  data={"student_response": "La réponse est 5", "current_difficulty": "medium", "topic": "Mathématiques"},
                  description="Adaptation temps réel")
    test_endpoint("/api/v1/ai-unified/comprehensive-analysis", method="POST",
                  data={"student_id": 4, "include_content_generation": True},
                  description="Analyse complète IA")
    test_endpoint("/api/v1/ai-unified/virtual-tutor", method="POST",
                  data={"student_question": "Comment résoudre une équation du premier degré ?", "context": "mathématiques"},
                  description="Tuteur virtuel")
    
    # 4. Tests Phase 2.3: Auto-évaluations Guidées
    print("\n📝 Phase 2.3: Auto-évaluations Guidées")
    print("-" * 40)
    test_endpoint("/api/v1/continuous_assessment/competencies", description="Liste des compétences")
    test_endpoint("/api/v1/continuous_assessment/student/4/competencies", description="Compétences étudiant")
    test_endpoint("/api/v1/continuous_assessment/assessments", description="Évaluations continues")
    
    # 5. Tests Phase 2.4: Cartographie des Compétences
    print("\n🗺️ Phase 2.4: Cartographie des Compétences")
    print("-" * 40)
    test_endpoint("/api/v1/advanced_analytics/performance-predictions", description="Prédictions performance")
    test_endpoint("/api/v1/advanced_analytics/difficulty-detection", description="Détection difficultés")
    test_endpoint("/api/v1/student_performance/4", description="Performance détaillée")
    test_endpoint("/api/v1/learning_history/student/4", description="Historique apprentissage")
    
    # 6. Tests Phase 2.5: Feedback Immédiat
    print("\n💬 Phase 2.5: Feedback Immédiat")
    print("-" * 40)
    test_endpoint("/api/v1/quiz_results/student/4", description="Résultats quiz avec feedback")
    test_endpoint("/api/v1/analytics/student/4/progress", description="Progression détaillée")
    test_endpoint("/api/v1/recommendations/student/4/personalized", description="Recommandations personnalisées")
    
    # 7. Tests Phase 2.6: Visualisation des Compétences
    print("\n📊 Phase 2.6: Visualisation des Compétences")
    print("-" * 40)
    test_endpoint("/api/v1/analytics-advanced/interactive-charts/1", description="Graphiques interactifs")
    test_endpoint("/api/v1/analytics-advanced/export-pdf/1", description="Export PDF")
    test_endpoint("/api/v1/analytics-advanced/export-excel/1", description="Export Excel")
    
    print("\n" + "=" * 60)
    print("✅ Tests Phase 2 terminés!")
    print("\n📋 Résumé Phase 2:")
    print("   • Tests adaptatifs avec algorithmes IA")
    print("   • Cartographie des compétences en temps réel")
    print("   • Feedback immédiat et remédiation")
    print("   • Visualisation avancée des données")
    print("   • Auto-évaluations guidées")
    print("   • Prédictions de performance")

if __name__ == "__main__":
    main() 