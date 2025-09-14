#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test dans la base de données
"""

import sqlite3
import os
import hashlib
from datetime import datetime

def create_test_user():
    """Crée un utilisateur de test dans la base de données"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "app.db")
    
    print(f"🗄️ Base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("✅ Connexion à la base de données réussie")
        
        # Vérifier si la table users existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if not cursor.fetchone():
            print("❌ Table 'users' non trouvée")
            return False
        
        # Vérifier si l'utilisateur de test existe déjà
        cursor.execute("""
            SELECT id, email, role FROM users 
            WHERE email = 'teacher@example.com'
        """)
        
        existing_user = cursor.fetchone()
        
        if existing_user:
            user_id, email, role = existing_user
            print(f"✅ Utilisateur de test déjà existant:")
            print(f"   ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Rôle: {role}")
            return True
        
        # Créer l'utilisateur de test
        test_user = {
            'email': 'teacher@example.com',
            'password': 'teacher123',  # Mot de passe en clair
            'first_name': 'Test',
            'last_name': 'Teacher',
            'role': 'teacher',
            'is_active': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Hasher le mot de passe (SHA256 comme dans le système)
        hashed_password = hashlib.sha256(test_user['password'].encode()).hexdigest()
        
        # Insérer l'utilisateur
        cursor.execute("""
            INSERT INTO users (email, password, first_name, last_name, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_user['email'],
            hashed_password,
            test_user['first_name'],
            test_user['last_name'],
            test_user['role'],
            test_user['is_active'],
            test_user['created_at'],
            test_user['updated_at']
        ))
        
        # Récupérer l'ID de l'utilisateur créé
        user_id = cursor.lastrowid
        
        # Valider la transaction
        conn.commit()
        
        print("✅ Utilisateur de test créé avec succès:")
        print(f"   ID: {user_id}")
        print(f"   Email: {test_user['email']}")
        print(f"   Mot de passe: {test_user['password']}")
        print(f"   Rôle: {test_user['role']}")
        
        # Vérifier que l'utilisateur a été créé
        cursor.execute("""
            SELECT id, email, role, first_name, last_name FROM users 
            WHERE email = 'teacher@example.com'
        """)
        
        created_user = cursor.fetchone()
        if created_user:
            print(f"\n🔍 Vérification en base:")
            print(f"   ID: {created_user[0]}")
            print(f"   Email: {created_user[1]}")
            print(f"   Rôle: {created_user[2]}")
            print(f"   Nom: {created_user[3]} {created_user[4]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def test_user_login():
    """Teste la connexion de l'utilisateur de test"""
    
    print("\n🧪 Test de connexion de l'utilisateur de test...")
    
    try:
        import requests
        
        # Données de connexion
        login_data = {
            "email": "teacher@example.com",
            "password": "teacher123"
        }
        
        # Appel à l'API de connexion
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Connexion réussie !")
            print(f"Token: {token[:50]}...")
            
            # Tester le token avec l'endpoint protégé
            headers = {"Authorization": f"Bearer {token}"}
            
            test_response = requests.post(
                "http://localhost:8000/api/v1/ai-formative-evaluations/generate-evaluation/",
                headers=headers,
                json={
                    "title": "Test",
                    "subject": "Test",
                    "assessment_type": "project",
                    "description": "Test",
                    "target_level": "intermediate",
                    "duration_minutes": 60,
                    "max_students": 30,
                    "learning_objectives": ["Test"],
                    "custom_requirements": ""
                }
            )
            
            print(f"\n🔍 Test endpoint protégé:")
            print(f"Status: {test_response.status_code}")
            
            if test_response.status_code == 200:
                print("✅ L'endpoint protégé fonctionne avec le token de connexion !")
            else:
                print(f"❌ L'endpoint protégé ne fonctionne pas: {test_response.text}")
                
        else:
            print(f"❌ Échec de la connexion: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")

if __name__ == "__main__":
    print("👤 Créateur d'utilisateur de test pour l'API formative evaluations")
    print("=" * 70)
    
    # Créer l'utilisateur de test
    if create_test_user():
        print("\n🎯 Utilisateur de test créé !")
        
        # Tester la connexion
        test_user_login()
        
        print("\n✅ Processus terminé avec succès !")
        print("\n🔧 POUR TESTER LE FRONTEND :")
        print("1. Va sur la page de connexion")
        print("2. Connecte-toi avec:")
        print("   Email: teacher@example.com")
        print("   Mot de passe: teacher123")
        print("3. Va sur la page des évaluations formatives")
        print("4. Essaie de créer une évaluation formative")
    else:
        print("\n❌ ÉCHEC DE LA CRÉATION DE L'UTILISATEUR") 