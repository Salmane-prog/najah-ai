#!/usr/bin/env python3
"""
Test du dashboard étudiant corrigé
"""

import requests

print("🧪 Test du dashboard étudiant corrigé")
print("=" * 50)

BASE_URL = "http://localhost:8000"

try:
    # Login en tant qu'étudiant (Salmane)
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    })

    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login étudiant OK")

        # Test endpoint /my-performance
        response = requests.get(f"{BASE_URL}/api/v1/student_performance/my-performance", headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées pour l'étudiant {data.get('student_name')}")
            
            print(f"\n📊 Données de performance:")
            print(f"   Total quiz: {data.get('total_quizzes')}")
            print(f"   Score moyen: {data.get('average_score')}%")
            print(f"   Pourcentage global: {data.get('overall_percentage')}%")
            print(f"   Tendance: {data.get('trend')}")
            print(f"   Activité récente: {data.get('recent_activity')}")
            print(f"   Dernière activité: {data.get('last_activity')}")

            # Vérifier la cohérence avec le dashboard professeur
            print(f"\n🔍 Vérification de cohérence:")
            expected_quizzes = 5  # Selon le dashboard professeur
            expected_score = 56.0  # Selon le dashboard professeur
            
            actual_quizzes = data.get('total_quizzes', 0)
            actual_score = data.get('average_score', 0)
            
            print(f"   Quiz attendus: {expected_quizzes}, Récupérés: {actual_quizzes}")
            print(f"   Score attendu: {expected_score}%, Récupéré: {actual_score}%")
            
            if actual_quizzes == expected_quizzes and abs(actual_score - expected_score) < 1:
                print("🎉 Données cohérentes avec le dashboard professeur !")
                print("   Le dashboard étudiant devrait maintenant afficher les bonnes données.")
            else:
                print("⚠️ Données incohérentes avec le dashboard professeur")
                print("   Vérifiez que l'endpoint /my-performance utilise les bonnes tables.")

        else:
            print(f"❌ Erreur {response.status_code}")
            print(f"   Détail: {response.text}")
    else:
        print(f"❌ Login étudiant échoué: {login.status_code}")

except Exception as e:
    print(f"❌ Erreur: {e}")









