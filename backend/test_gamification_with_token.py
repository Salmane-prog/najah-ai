#!/usr/bin/env python3
"""
Script pour tester l'endpoint gamification avec un token valide
"""

import os
import sys
import requests
import json

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gamification_with_token():
    """Tester l'endpoint gamification avec un token valide"""
    
    try:
        from core.security import create_access_token
        from models.user import User
        from core.database import SessionLocal
        
        # Créer un token pour un utilisateur existant
        db = SessionLocal()
        user = db.query(User).first()
        
        if not user:
            print("❌ Aucun utilisateur trouvé dans la base de données")
            return
        
        print(f"👤 Utilisateur trouvé: {user.username} (ID: {user.id})")
        
        # Créer un token valide
        token = create_access_token(data={"sub": user.email})
        print(f"🔑 Token créé: {token[:50]}...")
        
        # Tester l'endpoint gamification
        response = requests.get(
            'http://localhost:8000/api/v1/gamification/user/stats',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"\n📊 Test endpoint gamification:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès! Données reçues:")
            print(f"      - User ID: {data.get('user_id')}")
            print(f"      - Level: {data.get('level')}")
            print(f"      - Badges: {data.get('badges_count')}")
            print(f"      - Achievements: {data.get('achievements_count')}")
            print(f"      - Challenges: {data.get('challenges_count')}")
            print(f"      - Quizzes: {data.get('total_quizzes')}")
            print(f"      - Score moyen: {data.get('average_score')}%")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gamification_with_token()