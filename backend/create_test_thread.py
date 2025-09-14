#!/usr/bin/env python3
"""
Script pour créer un thread de test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.thread import Thread
from models.messages import Message
from models.user import User
from models.forum import ForumCategory
from datetime import datetime

def create_test_thread():
    """Créer un thread de test"""
    db = SessionLocal()
    
    try:
        # Récupérer un utilisateur existant
        user = db.query(User).first()
        if not user:
            print("❌ Aucun utilisateur trouvé dans la base de données")
            return
        
        # Récupérer une catégorie
        category = db.query(ForumCategory).first()
        if not category:
            print("❌ Aucune catégorie trouvée dans la base de données")
            return
        
        # Créer le thread
        thread = Thread(
            title="Comment résoudre une équation du premier degré ?",
            created_by=user.id,
            category_id=category.id,
            created_at=datetime.now()
        )
        db.add(thread)
        db.flush()
        
        # Créer le premier message
        message = Message(
            content="Bonjour à tous !\n\nJe suis en train de réviser les équations du premier degré et j'ai un peu de mal avec cette équation :\n\n2x + 5 = 3x - 1\n\nJe sais qu'il faut isoler x, mais je ne suis pas sûr de ma méthode. Quelqu'un peut m'expliquer étape par étape comment procéder ?\n\nMerci d'avance pour votre aide !",
            user_id=user.id,
            thread_id=thread.id,
            created_at=datetime.now()
        )
        db.add(message)
        
        # Créer une réponse
        response = Message(
            content="Salut ! Pour résoudre cette équation, voici la méthode étape par étape :\n\n1) Regrouper tous les termes avec x d'un côté :\n   2x - 3x = -1 - 5\n\n2) Simplifier :\n   -x = -6\n\n3) Multiplier par -1 des deux côtés :\n   x = 6\n\nLa solution est donc x = 6.\n\nPour vérifier : 2(6) + 5 = 3(6) - 1\n               12 + 5 = 18 - 1\n               17 = 17 ✓",
            user_id=user.id,
            thread_id=thread.id,
            created_at=datetime.now()
        )
        db.add(response)
        
        db.commit()
        
        print("✅ Thread de test créé avec succès !")
        print(f"   - Titre: {thread.title}")
        print(f"   - Auteur: {user.first_name} {user.last_name}" if user.first_name else f"   - Auteur: {user.username}")
        print(f"   - Catégorie: {category.name}")
        print(f"   - Messages: 2")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du thread : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_thread() 