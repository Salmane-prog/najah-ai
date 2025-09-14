#!/usr/bin/env python3
"""
Test de la correction des doublons d'étudiants
"""

import requests
import json
from collections import Counter

def test_duplicate_fix():
    """Tester la correction des doublons"""
    print("🧪 Test de la correction des doublons d'étudiants")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000"
    
    # 1. Connexion professeur
    print("\n1️⃣ Connexion professeur...")
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
    
    # 2. Test de l'endpoint students (corrigé)
    print("\n2️⃣ Test de l'endpoint /api/v1/teacher-dashboard/students...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            print(f"✅ {len(students)} étudiants récupérés")
            
            # 3. Vérification des doublons
            print("\n3️⃣ Vérification des doublons...")
            
            # Vérifier les IDs dupliqués
            student_ids = [student.get('id') for student in students]
            id_counts = Counter(student_ids)
            duplicates = {id: count for id, count in id_counts.items() if count > 1}
            
            if duplicates:
                print("❌ Doublons d'IDs détectés:")
                for student_id, count in duplicates.items():
                    print(f"   ID {student_id}: {count} occurrences")
                    
                # Afficher les détails des doublons
                print("\n📊 Détails des étudiants avec ID dupliqué:")
                for student_id in duplicates:
                    duplicate_students = [s for s in students if s.get('id') == student_id]
                    for i, student in enumerate(duplicate_students):
                        print(f"   {i+1}. ID: {student.get('id')}, Nom: {student.get('name')}, Classe: {student.get('class_name')}")
                
                print("\n💥 La correction n'a pas fonctionné !")
                return False
            else:
                print("✅ Aucun doublon d'ID détecté - Correction réussie !")
            
            # Vérifier les noms dupliqués
            student_names = [student.get('name') for student in students]
            name_counts = Counter(student_names)
            name_duplicates = {name: count for name, count in name_counts.items() if count > 1}
            
            if name_duplicates:
                print("\n⚠️ Noms dupliqués détectés:")
                for name, count in name_duplicates.items():
                    print(f"   Nom '{name}': {count} occurrences")
            else:
                print("✅ Aucun nom dupliqué détecté")
            
            # Statistiques générales
            print(f"\n📈 Statistiques:")
            print(f"   Total étudiants: {len(students)}")
            print(f"   IDs uniques: {len(set(student_ids))}")
            print(f"   Noms uniques: {len(set(student_names))}")
            
            # Afficher les détails des étudiants
            print(f"\n📊 Détails des étudiants:")
            for i, student in enumerate(students):
                print(f"   {i+1}. ID: {student.get('id')}, Nom: {student.get('name')}, Classe: {student.get('class_name')}")
                print(f"      Score: {student.get('average_score')}, Tentatives: {student.get('total_attempts')}")
            
            return True
        else:
            print(f"❌ Échec de récupération: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_duplicate_fix()
    if success:
        print("\n🎉 Correction des doublons réussie !")
        print("💡 Le dashboard professeur devrait maintenant afficher des étudiants uniques")
    else:
        print("\n💥 Il reste des problèmes à résoudre")
        print("💡 Vérifiez les logs du serveur")






