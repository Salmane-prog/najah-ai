#!/usr/bin/env python3
"""
Script pour créer les tables manquantes du forum
"""

from core.database import engine, Base
from models.forum import ForumCategory, ForumThread, ForumReply

def create_forum_tables():
    try:
        print("🔨 Création des tables du forum...")
        
        # Créer les tables ForumThread et ForumReply
        ForumThread.__table__.create(engine, checkfirst=True)
        ForumReply.__table__.create(engine, checkfirst=True)
        
        print("✅ Tables forum_threads et forum_replies créées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")

if __name__ == "__main__":
    create_forum_tables() 