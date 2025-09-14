#!/usr/bin/env python3
"""
Script pour forcer la réinitialisation complète de SQLAlchemy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from core.config import settings

def force_sqlalchemy_refresh():
    print("=== FORÇAGE DE LA RÉINITIALISATION SQLALCHEMY ===")
    
    # Créer un nouveau moteur sans cache
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,  # Activer les logs SQL
        pool_pre_ping=True,
        pool_recycle=300
    )
    
    try:
        print("1. Test de connexion avec nouveau moteur...")
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Connexion réussie avec nouveau moteur")
        
        print("\n2. Vérification des métadonnées...")
        
        # Inspecter la base de données
        inspector = inspect(engine)
        
        # Vérifier les tables
        tables = inspector.get_table_names()
        print(f"Tables trouvées: {tables}")
        
        if 'contents' in tables:
            print("✅ Table 'contents' trouvée")
            
            # Vérifier les colonnes via l'inspecteur
            columns = inspector.get_columns('contents')
            print(f"Colonnes trouvées via inspecteur ({len(columns)}):")
            for col in columns:
                print(f"  - {col['name']} ({col['type']})")
            
            # Vérifier spécifiquement content_type
            column_names = [col['name'] for col in columns]
            if 'content_type' in column_names:
                print("✅ La colonne 'content_type' est visible via l'inspecteur")
            else:
                print("❌ La colonne 'content_type' n'est pas visible via l'inspecteur")
        else:
            print("❌ Table 'contents' non trouvée")
            return
        
        print("\n3. Test de requête SQL brute...")
        
        with engine.connect() as connection:
            # Test de requête simple
            result = connection.execute(text("SELECT COUNT(*) FROM contents"))
            count = result.fetchone()[0]
            print(f"✅ Nombre d'enregistrements: {count}")
            
            # Test de requête avec content_type
            result = connection.execute(text("SELECT id, title, content_type FROM contents LIMIT 3"))
            rows = result.fetchall()
            print("✅ Requête avec content_type réussie:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Type: {row[2]}")
        
        print("\n4. Test de requête complète...")
        
        with engine.connect() as connection:
            # Test de la requête qui échoue dans l'API
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
            print(f"✅ Requête complète réussie: {len(rows)} résultats")
        
        print("\n5. Test de session ORM...")
        
        # Créer une nouvelle session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Importer le modèle après avoir créé le moteur
            from models.content import Content
            
            # Test de requête ORM
            contents = db.query(Content).limit(3).all()
            print(f"✅ Requête ORM réussie: {len(contents)} résultats")
            
            for content in contents:
                print(f"  - ID: {content.id}, Title: {content.title}, Type: {content.content_type}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête ORM: {e}")
        finally:
            db.close()
        
        print("\n🎉 Réinitialisation SQLAlchemy terminée!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    force_sqlalchemy_refresh() 