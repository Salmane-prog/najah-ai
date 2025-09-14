#!/usr/bin/env python3
"""
Test script pour vérifier l'API des devoirs étudiants
"""

import requests
import json
from datetime import datetime

def test_student_homework_api():
    """Test de l'API des devoirs étudiants"""
    
    base_url = "http://localhost:8000/api/v1/student-organization"
    
    print("🧪 Test de l'API des devoirs étudiants")
    print("=" * 50)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Test de l'endpoint homework (sans auth pour débogage)
        print("\n1. 📋 Test de l'endpoint /homework...")
        response = requests.get(f"{base_url}/homework", headers=headers)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 403:
            print("✅ Endpoint protégé correctement (403 Forbidden)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
            print(f"Réponse: {response.text}")
        
        # 2. Vérifier que le serveur répond
        print("\n2. 🔍 Test de connectivité du serveur...")
        try:
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Serveur accessible et fonctionnel")
            else:
                print(f"⚠️  Serveur accessible mais statut: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Serveur non accessible")
            return
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return
        
        # 3. Vérifier les données existantes dans la base
        print("\n3. 📊 Vérification des données dans la base...")
        import sqlite3
        from pathlib import Path
        
        db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Compter les devoirs
            cursor.execute("SELECT COUNT(*) FROM homework")
            homework_count = cursor.fetchone()[0]
            print(f"📝 Nombre de devoirs dans la base: {homework_count}")
            
            # Afficher les devoirs récents
            if homework_count > 0:
                cursor.execute("""
                    SELECT id, title, subject, status, assigned_to, due_date 
                    FROM homework 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """)
                homeworks = cursor.fetchall()
                print(f"📋 Devoirs récents:")
                for hw in homeworks:
                    print(f"   - ID: {hw[0]}, Titre: {hw[1]}, Matière: {hw[2]}, Statut: {hw[3]}, Assigné à: {hw[4]}")
            
            conn.close()
        else:
            print("❌ Base de données non trouvée")
        
        print("\n✅ Test terminé!")
        print("\n💡 Pour tester avec authentification:")
        print("   1. Connectez-vous en tant qu'étudiant")
        print("   2. Allez sur le dashboard étudiant")
        print("   3. Vérifiez si les devoirs apparaissent dans le widget")
        
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_student_homework_api()