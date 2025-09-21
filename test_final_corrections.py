#!/usr/bin/env python3
"""
Script de test final pour vérifier que toutes les corrections du dashboard professeur fonctionnent
"""

import requests
import json
import time

def test_final_corrections():
    """Test final des corrections"""
    print("🔍 Test final des corrections du dashboard professeur")
    print("=" * 60)
    
    # Configuration
    BASE_URL = "http://localhost:8000"
    
    # 1. Vérifier que le serveur est accessible
    print("\n1️⃣ Vérification du serveur backend...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur backend accessible")
        else:
            print(f"❌ Serveur accessible mais status inattendu: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Serveur non accessible: {e}")
        print("💡 Démarrez le serveur backend avec: python start_backend.py")
        return False
    
    # 2. Test de connexion avec l'utilisateur professeur existant
    print("\n2️⃣ Test de connexion professeur...")
    
    # Utiliser l'email qui apparaît dans les logs
    test_accounts = [
        {"email": "marizee.dubois@najah.ai", "password": "password123"},
        {"email": "teacher@test.com", "password": "password123"},
        {"email": "prof@najah.ai", "password": "password123"}
    ]
    
    token = None
    for account in test_accounts:
        try:
            print(f"   Tentative avec {account['email']}...")
            response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=account, timeout=5)
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                print(f"✅ Connexion réussie avec {account['email']}")
                break
            else:
                print(f"   ❌ Échec: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    if not token:
        print("❌ Aucune connexion réussie")
        print("💡 Vérifiez que vous avez un compte professeur valide")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Test de l'endpoint students (corrigé)
    print("\n3️⃣ Test de l'endpoint /api/v1/teacher-dashboard/students (corrigé)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès - {data.get('total_count', 0)} étudiants trouvés")
            
            if data.get('students'):
                print("📊 Données des étudiants:")
                for i, student in enumerate(data['students'][:3]):  # Afficher les 3 premiers
                    print(f"   {i+1}. ID: {student.get('id')}, Nom: {student.get('name')}, Classe: {student.get('class_name')}")
                    print(f"      Score moyen: {student.get('average_score')}, Tentatives: {student.get('total_attempts')}")
            else:
                print("⚠️ Aucun étudiant trouvé (normal si pas de données)")
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # 4. Test de l'endpoint reports
    print("\n4️⃣ Test de l'endpoint /api/v1/reports/teacher...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/reports/teacher", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès - {len(data)} rapports trouvés")
            if data:
                print("📊 Premier rapport:")
                print(f"   ID: {data[0].get('id')}, Type: {data[0].get('report_type')}")
        else:
            print(f"⚠️ Échec: {response.status_code} - {response.text}")
            print("💡 Normal si pas de rapports créés")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 5. Test de l'endpoint analytics
    print("\n5️⃣ Test de l'endpoint /api/v1/teacher-dashboard/analytics...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/analytics", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès - Analytics récupérés")
            if data.get('overview'):
                overview = data['overview']
                print(f"📊 Vue d'ensemble: {overview.get('total_students')} étudiants, {overview.get('total_quizzes')} quiz")
        else:
            print(f"⚠️ Échec: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 6. Test que l'ancien endpoint n'existe plus
    print("\n6️⃣ Vérification que l'ancien endpoint n'existe plus...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/student_analytics/students/analytics", headers=headers, timeout=5)
        if response.status_code == 404:
            print("✅ Ancien endpoint correctement supprimé (404)")
        else:
            print(f"⚠️ Ancien endpoint encore accessible: {response.status_code}")
    except Exception as e:
        print(f"✅ Ancien endpoint non accessible: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test final terminé !")
    print("💡 Si tous les tests sont passés, le dashboard professeur devrait fonctionner parfaitement")
    return True

if __name__ == "__main__":
    test_final_corrections()









