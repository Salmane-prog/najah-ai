#!/usr/bin/env python3
"""
Script pour initialiser les données du forum d'entraide
"""

from core.database import SessionLocal
from models.forum import ForumCategory, ForumThread, ForumReply
from models.user import User
from datetime import datetime
import json

def init_forum_data():
    db = SessionLocal()
    try:
        print("🚀 Initialisation du forum d'entraide...")
        
        # Créer les catégories par défaut
        categories_data = [
            {
                "name": "Mathématiques",
                "description": "Questions et discussions sur les mathématiques",
                "subject": "Mathématiques",
                "level": "Tous niveaux"
            },
            {
                "name": "Français",
                "description": "Questions et discussions sur le français",
                "subject": "Français",
                "level": "Tous niveaux"
            },
            {
                "name": "Sciences",
                "description": "Questions et discussions sur les sciences",
                "subject": "Sciences",
                "level": "Tous niveaux"
            },
            {
                "name": "Histoire",
                "description": "Questions et discussions sur l'histoire",
                "subject": "Histoire",
                "level": "Tous niveaux"
            },
            {
                "name": "Général",
                "description": "Questions générales et discussions diverses",
                "subject": "Général",
                "level": "Tous niveaux"
            }
        ]
        
        # Créer ou récupérer les catégories
        categories = {}
        for cat_data in categories_data:
            existing = db.query(ForumCategory).filter(ForumCategory.name == cat_data["name"]).first()
            if existing:
                categories[cat_data["name"]] = existing
                print(f"✅ Catégorie '{cat_data['name']}' déjà existante")
            else:
                category = ForumCategory(**cat_data)
                db.add(category)
                db.commit()
                db.refresh(category)
                categories[cat_data["name"]] = category
                print(f"✅ Catégorie '{cat_data['name']}' créée")
        
        # Récupérer un utilisateur étudiant pour créer des exemples
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("❌ Aucun étudiant trouvé pour créer des exemples")
            return
        
        # Créer quelques threads d'exemple
        example_threads = [
            {
                "title": "Aide avec les équations du second degré",
                "content": "Bonjour ! J'ai du mal à comprendre comment résoudre les équations du type ax² + bx + c = 0. Pouvez-vous m'expliquer la méthode du discriminant ?",
                "category": "Mathématiques",
                "tags": json.dumps(["équations", "second degré", "discriminant"])
            },
            {
                "title": "Conjugaison du verbe 'avoir'",
                "content": "Je voudrais réviser la conjugaison du verbe 'avoir' au présent. Quelqu'un peut-il me donner un rappel ?",
                "category": "Français",
                "tags": json.dumps(["conjugaison", "verbe avoir", "présent"])
            },
            {
                "title": "Photosynthèse : explication simple",
                "content": "Quelqu'un peut-il m'expliquer simplement le processus de photosynthèse ? Je ne comprends pas bien comment les plantes produisent leur nourriture.",
                "category": "Sciences",
                "tags": json.dumps(["photosynthèse", "plantes", "biologie"])
            }
        ]
        
        for thread_data in example_threads:
            # Vérifier si le thread existe déjà
            existing = db.query(ForumThread).filter(
                ForumThread.title == thread_data["title"],
                ForumThread.author_id == student.id
            ).first()
            
            if existing:
                print(f"✅ Thread '{thread_data['title']}' déjà existant")
                continue
            
            # Créer le thread
            thread = ForumThread(
                title=thread_data["title"],
                content=thread_data["content"],
                category_id=categories[thread_data["category"]].id,
                author_id=student.id,
                tags=thread_data["tags"]
            )
            
            db.add(thread)
            db.commit()
            db.refresh(thread)
            
            # Créer une réponse d'exemple
            reply = ForumReply(
                thread_id=thread.id,
                author_id=student.id,
                content="Voici un exemple de réponse pour vous aider ! N'hésitez pas à poser d'autres questions."
            )
            
            db.add(reply)
            db.commit()
            
            print(f"✅ Thread '{thread_data['title']}' créé avec une réponse")
        
        print("🎉 Initialisation du forum terminée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_forum_data()
