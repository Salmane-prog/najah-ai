#!/usr/bin/env python3
"""
Script de migration PostgreSQL pour Railway
"""
import os
import sys
from pathlib import Path

def main():
    print("🗄️ Migration PostgreSQL...")
    
    # Vérifier DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL non configurée")
        return False
    
    print(f"📁 Base de données: {db_url[:30]}...")
    
    if not db_url.startswith('postgresql://'):
        print("⚠️ DATABASE_URL n'est pas PostgreSQL")
        return False
    
    try:
        # Importer les modèles
        from models import Base
        from sqlalchemy import create_engine, text
        
        # Créer le moteur
        engine = create_engine(db_url)
        
        # Tester la connexion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connexion PostgreSQL réussie: {version[:50]}...")
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
        
        # Compter les tables
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.scalar()
            print(f"📊 Nombre de tables créées: {table_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de migration: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
