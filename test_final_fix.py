#!/usr/bin/env python3
"""
Test final après toutes les corrections du dashboard professeur
"""

import requests
import json

def test_final_fix():
    """Test final complet"""
    print("🧪 Test final après toutes les corrections")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000"
    
    # 1. Test de base du serveur
    print("\n1️⃣ Test de base du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Serveur accessible mais status inattendu: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Serveur non accessible: {e}")
        return False
    
    # 2. Test de connexion professeur
    print("\n2️⃣ Test de connexion professeur...")
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }, timeout=5)
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Connexion réussie")
        else:
            print(f"❌ Échec de connexion: {login_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # 3. Test de l'endpoint students (corrigé)
    print("\n3️⃣ Test de l'endpoint /api/v1/teacher-dashboard/students...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès ! {data.get('total_count', 0)} étudiants trouvés")
            
            if data.get('students'):
                print("📊 Données des étudiants:")
                for i, student in enumerate(data['students'][:3]):
                    print(f"   {i+1}. ID: {student.get('id')}, Nom: {student.get('name')}, Classe: {student.get('class_name')}")
                    print(f"      Score: {student.get('average_score')}, Tentatives: {student.get('total_attempts')}")
            else:
                print("⚠️ Aucun étudiant trouvé (normal si pas de données)")
            
            return True
        elif response.status_code == 500:
            print("❌ Erreur 500 - Problème dans le code backend")
            print("💡 Vérifiez les logs du serveur")
            return False
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_final_fix()
    if success:
        print("\n🎉 Toutes les corrections fonctionnent !")
        print("💡 Le dashboard professeur devrait maintenant marcher")
    else:
        print("\n💥 Il reste des problèmes à résoudre")
        print("💡 Vérifiez les logs du serveur")






