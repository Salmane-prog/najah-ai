#!/usr/bin/env python3
"""
Script d'initialisation des données de production pour Najah AI
Crée les données de base nécessaires au fonctionnement
"""
import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime
import hashlib

def hash_password(password: str) -> str:
    """Hash un mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_production_data():
    """Initialise les données de production"""
    
    # URL de la base de données (Railway PostgreSQL)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL non trouvée")
        return False
    
    try:
        # Connexion à la base
        engine = create_engine(database_url)
        
        print("🔗 Connexion à la base de données...")
        
        with engine.connect() as conn:
            # Vérifier si des données existent déjà
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            
            if user_count > 0:
                print(f"✅ Base déjà initialisée avec {user_count} utilisateurs")
                return True
            
            print("📝 Initialisation des données de base...")
            
            # Créer un utilisateur admin
            admin_password = hash_password("admin123")
            conn.execute(text("""
                INSERT INTO users (username, email, password_hash, role, is_active, created_at)
                VALUES ('admin', 'admin@najah-ai.com', :password, 'admin', true, :created_at)
            """), {
                "password": admin_password,
                "created_at": datetime.now()
            })
            
            # Créer un professeur de test
            teacher_password = hash_password("teacher123")
            conn.execute(text("""
                INSERT INTO users (username, email, password_hash, role, is_active, created_at)
                VALUES ('teacher', 'teacher@najah-ai.com', :password, 'teacher', true, :created_at)
            """), {
                "password": teacher_password,
                "created_at": datetime.now()
            })
            
            # Créer un étudiant de test
            student_password = hash_password("student123")
            conn.execute(text("""
                INSERT INTO users (username, email, password_hash, role, is_active, created_at)
                VALUES ('student', 'student@najah-ai.com', :password, 'student', true, :created_at)
            """), {
                "password": student_password,
                "created_at": datetime.now()
            })
            
            # Créer une classe de test
            conn.execute(text("""
                INSERT INTO classes (name, description, created_at)
                VALUES ('Classe Test', 'Classe de démonstration', :created_at)
            """), {
                "created_at": datetime.now()
            })
            
            # Commit les changements
            conn.commit()
            
            print("✅ Données de base créées avec succès !")
            print("👤 Admin: admin@najah-ai.com / admin123")
            print("👨‍🏫 Teacher: teacher@najah-ai.com / teacher123") 
            print("👨‍🎓 Student: student@najah-ai.com / student123")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

if __name__ == "__main__":
    success = init_production_data()
    if not success:
        sys.exit(1)

