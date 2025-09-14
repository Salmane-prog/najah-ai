#!/usr/bin/env python3
"""
Script pour créer des données réelles pour le forum
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

from core.database import engine, SessionLocal
from core.config import settings
from models.forum import ForumCategory, ForumTag, ThreadTag, ForumVote, ForumReport, ForumModeration
from models.thread import Thread
from models.messages import Message
from models.user import User

# Créer la connexion à la base de données
# engine = create_engine(SQLALCHEMY_DATABASE_URL) # This line is removed as per the edit hint
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # This line is removed as per the edit hint

def create_forum_data():
    """Créer des données réelles pour le forum"""
    db = SessionLocal()
    
    try:
        # Vérifier si les données existent déjà
        existing_categories = db.query(ForumCategory).count()
        if existing_categories > 0:
            print("Les données du forum existent déjà.")
            return
        
        # Créer les catégories
        categories_data = [
            {
                "name": "Mathématiques",
                "description": "Discussions sur les mathématiques",
                "subject": "Mathématiques",
                "level": "Tous niveaux",
                "is_active": True
            },
            {
                "name": "Sciences",
                "description": "Questions scientifiques",
                "subject": "Sciences",
                "level": "Tous niveaux",
                "is_active": True
            },
            {
                "name": "Langues",
                "description": "Apprentissage des langues",
                "subject": "Langues",
                "level": "Tous niveaux",
                "is_active": True
            },
            {
                "name": "Histoire-Géo",
                "description": "Histoire et géographie",
                "subject": "Histoire-Géo",
                "level": "Tous niveaux",
                "is_active": True
            },
            {
                "name": "Général",
                "description": "Discussions générales",
                "subject": "Général",
                "level": "Tous niveaux",
                "is_active": True
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = ForumCategory(**cat_data)
            db.add(category)
            db.flush()  # Pour générer l'ID
            categories.append(category)
        
        db.commit()
        
        # Récupérer les utilisateurs existants
        users = db.query(User).limit(5).all()
        if not users:
            print("Aucun utilisateur trouvé. Création d'utilisateurs de test...")
            # Créer des utilisateurs de test si nécessaire
            test_users = [
                {"email": "marie@test.com", "name": "Marie D.", "role": "student"},
                {"email": "thomas@test.com", "name": "Thomas L.", "role": "student"},
                {"email": "sophie@test.com", "name": "Sophie M.", "role": "student"},
                {"email": "prof@test.com", "name": "Prof. Martin", "role": "teacher"}
            ]
            
            for user_data in test_users:
                user = User(
                    email=user_data["email"],
                    name=user_data["name"],
                    role=user_data["role"],
                    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3ZxQQxq3Hy"  # password: test123
                )
                db.add(user)
            
            db.commit()
            users = db.query(User).limit(5).all()
        
        # Créer les threads
        threads_data = [
            {
                "title": "Aide pour résoudre une équation du second degré",
                "category_id": categories[0].id,  # Mathématiques
                "created_by": users[0].id,
                "created_at": datetime.now() - timedelta(hours=2)
            },
            {
                "title": "Explication sur la photosynthèse",
                "category_id": categories[1].id,  # Sciences
                "created_by": users[1].id,
                "created_at": datetime.now() - timedelta(hours=8)
            },
            {
                "title": "Conjugaison du verbe \"être\" au présent",
                "category_id": categories[2].id,  # Langues
                "created_by": users[2].id,
                "created_at": datetime.now() - timedelta(days=1)
            }
        ]
        
        threads = []
        for thread_data in threads_data:
            thread = Thread(**thread_data)
            db.add(thread)
            db.flush()  # Pour générer l'ID
            threads.append(thread)
        
        db.commit()
        
        # Créer les messages pour chaque thread
        messages_data = [
            # Messages pour le thread 1 (équation)
            {
                "content": "Je n'arrive pas à comprendre comment résoudre cette équation : x² + 5x + 6 = 0. Quelqu'un peut m'aider ?",
                "user_id": users[0].id,  # Marie D.
                "thread_id": threads[0].id,
                "created_at": datetime.now() - timedelta(hours=2)
            },
            {
                "content": "Pour résoudre x² + 5x + 6 = 0, tu peux utiliser la formule du discriminant : Δ = b² - 4ac = 25 - 24 = 1. Puis x = (-b ± √Δ) / 2a = (-5 ± 1) / 2. Donc x₁ = -2 et x₂ = -3.",
                "user_id": users[3].id,  # Prof. Martin
                "thread_id": threads[0].id,
                "created_at": datetime.now() - timedelta(hours=1, minutes=30)
            },
            {
                "content": "Merci beaucoup ! C'est beaucoup plus clair maintenant.",
                "user_id": users[0].id,  # Marie D.
                "thread_id": threads[0].id,
                "created_at": datetime.now() - timedelta(hours=1)
            },
            # Messages pour le thread 2 (photosynthèse)
            {
                "content": "Quelqu'un peut m'expliquer simplement le processus de photosynthèse ?",
                "user_id": users[1].id,  # Thomas L.
                "thread_id": threads[1].id,
                "created_at": datetime.now() - timedelta(hours=8)
            },
            {
                "content": "La photosynthèse est le processus par lequel les plantes convertissent la lumière solaire en énergie chimique. Elles utilisent le CO2 et l'eau pour produire du glucose et de l'oxygène.",
                "user_id": users[3].id,  # Prof. Martin
                "thread_id": threads[1].id,
                "created_at": datetime.now() - timedelta(hours=7)
            },
            # Messages pour le thread 3 (conjugaison)
            {
                "content": "Je révise la conjugaison et j'ai besoin d'aide pour le verbe être.",
                "user_id": users[2].id,  # Sophie M.
                "thread_id": threads[2].id,
                "created_at": datetime.now() - timedelta(days=1)
            },
            {
                "content": "Le verbe \"être\" au présent se conjugue : je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont.",
                "user_id": users[3].id,  # Prof. Martin
                "thread_id": threads[2].id,
                "created_at": datetime.now() - timedelta(hours=23)
            }
        ]
        
        for message_data in messages_data:
            message = Message(**message_data)
            db.add(message)
        
        db.commit()
        
        # Créer quelques tags
        tags_data = [
            {"name": "équation", "usage_count": 5},
            {"name": "second degré", "usage_count": 3},
            {"name": "maths", "usage_count": 8},
            {"name": "biologie", "usage_count": 4},
            {"name": "photosynthèse", "usage_count": 2},
            {"name": "plantes", "usage_count": 3},
            {"name": "français", "usage_count": 6},
            {"name": "conjugaison", "usage_count": 4},
            {"name": "grammaire", "usage_count": 5}
        ]
        
        tags = []
        for tag_data in tags_data:
            tag = ForumTag(**tag_data)
            db.add(tag)
            db.flush()  # Pour générer l'ID
            tags.append(tag)
        
        db.commit()
        
        # Associer des tags aux threads
        thread_tags = [
            {"thread_id": threads[0].id, "tag_id": tags[0].id},  # équation
            {"thread_id": threads[0].id, "tag_id": tags[1].id},  # second degré
            {"thread_id": threads[0].id, "tag_id": tags[2].id},  # maths
            {"thread_id": threads[1].id, "tag_id": tags[3].id},  # biologie
            {"thread_id": threads[1].id, "tag_id": tags[4].id},  # photosynthèse
            {"thread_id": threads[1].id, "tag_id": tags[5].id},  # plantes
            {"thread_id": threads[2].id, "tag_id": tags[6].id},  # français
            {"thread_id": threads[2].id, "tag_id": tags[7].id},  # conjugaison
            {"thread_id": threads[2].id, "tag_id": tags[8].id},  # grammaire
        ]
        
        for thread_tag_data in thread_tags:
            thread_tag = ThreadTag(**thread_tag_data)
            db.add(thread_tag)
        
        db.commit()
        
        print("✅ Données du forum créées avec succès !")
        print(f"   - {len(categories)} catégories créées")
        print(f"   - {len(threads)} threads créés")
        print(f"   - {len(messages_data)} messages créés")
        print(f"   - {len(tags)} tags créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_forum_data() 