#!/usr/bin/env python3
"""
Script pour forcer la synchronisation de SQLAlchemy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, SessionLocal
from models.content import Content
from sqlalchemy import text

def force_sqlalchemy_sync():
    print("=== FORÇAGE DE LA SYNCHRONISATION SQLALCHEMY ===")
    
    # Créer une nouvelle session
    db = SessionLocal()
    
    try:
        print("1. Test de connexion à la base de données...")
        
        # Test de connexion directe
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données réussie")
        
        print("\n2. Vérification de la table contents via SQLAlchemy...")
        
        # Vérifier si la table existe via SQLAlchemy
        with engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='contents'"))
            table_exists = result.fetchone()
            
            if table_exists:
                print("✅ La table 'contents' existe (SQLAlchemy)")
            else:
                print("❌ La table 'contents' n'existe pas (SQLAlchemy)")
                return
        
        print("\n3. Vérification des colonnes via SQLAlchemy...")
        
        # Vérifier les colonnes via SQLAlchemy
        with engine.connect() as connection:
            result = connection.execute(text("PRAGMA table_info(contents)"))
            columns = result.fetchall()
            
            print(f"Colonnes trouvées ({len(columns)}):")
            column_names = []
            for col in columns:
                column_name = col[1]
                column_type = col[2]
                column_names.append(column_name)
                print(f"  - {column_name} ({column_type})")
            
            if 'content_type' in column_names:
                print("✅ La colonne 'content_type' existe (SQLAlchemy)")
            else:
                print("❌ La colonne 'content_type' n'existe pas (SQLAlchemy)")
        
        print("\n4. Test de requête SQLAlchemy ORM...")
        
        try:
            # Test de requête simple
            contents = db.query(Content).limit(3).all()
            print(f"✅ Requête ORM simple réussie: {len(contents)} résultats")
            
            for content in contents:
                print(f"  - ID: {content.id}, Title: {content.title}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête ORM simple: {e}")
        
        print("\n5. Test de la requête qui échoue...")
        
        try:
            # Test de la requête qui échoue dans l'API
            contents = db.query(Content).filter(Content.subject.ilike("%None%")).all()
            print(f"✅ Requête problématique réussie: {len(contents)} résultats")
            
        except Exception as e:
            print(f"❌ Erreur lors de la requête problématique: {e}")
            print("Détails de l'erreur:")
            print(f"  - Type: {type(e).__name__}")
            print(f"  - Message: {str(e)}")
        
        print("\n6. Test de requête SQL brute via SQLAlchemy...")
        
        try:
            with engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT contents.id, contents.title, contents.description, 
                           contents.content_type, contents.subject, contents.level, 
                           contents.difficulty, contents.estimated_time, contents.content_data, 
                           contents.file_url, contents.thumbnail_url, contents.tags, 
                           contents.learning_objectives, contents.prerequisites, 
                           contents.skills_targeted, contents.created_by, contents.category_id, 
                           contents.created_at, contents.updated_at, contents.is_active
                    FROM contents
                    WHERE lower(contents.subject) LIKE lower(:subject)
                """), {"subject": "%None%"})
                
                rows = result.fetchall()
                print(f"✅ Requête SQL brute réussie: {len(rows)} résultats")
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête SQL brute: {e}")
        
        print("\n7. Vérification du modèle Content...")
        
        # Vérifier les attributs du modèle
        content_attrs = Content.__table__.columns.keys()
        print(f"Attributs du modèle Content ({len(content_attrs)}):")
        for attr in content_attrs:
            print(f"  - {attr}")
        
        # Vérifier si content_type est dans les attributs
        if 'content_type' in content_attrs:
            print("✅ L'attribut 'content_type' est défini dans le modèle")
        else:
            print("❌ L'attribut 'content_type' n'est pas défini dans le modèle")
        
        print("\n8. Test de création d'un objet Content...")
        
        try:
            # Test de création d'un objet Content (sans sauvegarder)
            test_content = Content(
                title="Test Content",
                description="Test Description",
                subject="Test Subject",
                level="beginner",
                content_type="text"
            )
            print("✅ Création d'objet Content réussie")
            print(f"  - content_type: {test_content.content_type}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création d'objet Content: {e}")
        
        print("\n🎉 Vérification SQLAlchemy terminée!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    force_sqlalchemy_sync() 