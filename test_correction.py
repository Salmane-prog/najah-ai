#!/usr/bin/env python3
"""
Test de la correction de l'erreur 500
"""

import requests

def test_correction():
    """Tester la correction"""
    print("🧪 Test de la correction de l'erreur 500")
    print("=" * 50)
    
    BASE_URL = "http://localhost:8000"
    
    # Connexion
    try:
        print("1️⃣ Connexion professeur...")
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        })
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Connexion réussie")
            
            # Test endpoint
            print("\n2️⃣ Test endpoint /api/v1/teacher-dashboard/students...")
            response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                students = data.get('students', [])
                print(f"✅ {len(students)} étudiants récupérés")
                
                # Vérifier les IDs
                ids = [s.get('id') for s in students]
                unique_ids = set(ids)
                print(f"IDs uniques: {len(unique_ids)} sur {len(ids)} total")
                
                if len(unique_ids) == len(ids):
                    print("🎉 Aucun doublon détecté !")
                else:
                    print("❌ Doublons détectés")
                    
                # Afficher les détails
                print(f"\n📊 Détails des étudiants:")
                for i, student in enumerate(students):
                    print(f"   {i+1}. ID: {student.get('id')}, Nom: {student.get('name')}, Classe: {student.get('class_name')}")
                    
            else:
                print(f"❌ Erreur {response.status_code}")
                if response.status_code == 500:
                    print("💥 Erreur 500 - Problème dans le code backend")
                print("💡 Vérifiez les logs du serveur")
                
        else:
            print(f"❌ Connexion échouée: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_correction()









