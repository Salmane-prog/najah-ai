#!/usr/bin/env python3
"""
Script pour créer des utilisateurs de test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from datetime import datetime
from passlib.context import CryptContext

def create_test_users():
    """Créer des utilisateurs de test"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    # Contexte pour le hachage des mots de passe
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    try:
        with engine.connect() as conn:
            # Vérifier s'il y a déjà des utilisateurs
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            
            if user_count > 0:
                print(f"✅ {user_count} utilisateur(s) déjà présent(s) dans la base de données")
                return
            
            # Créer un professeur de test
            teacher_password = pwd_context.hash("teacher123")
            conn.execute(text("""
                INSERT INTO users (
                    username, email, hashed_password, role, is_active,
                    created_at, last_login
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """), (
                "prof_test", "prof@test.com", teacher_password, "teacher", True,
                datetime.utcnow(), datetime.utcnow()
            ))
            
            # Créer un étudiant de test
            student_password = pwd_context.hash("student123")
            conn.execute(text("""
                INSERT INTO users (
                    username, email, hashed_password, role, is_active,
                    created_at, last_login
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """), (
                "etudiant_test", "etudiant@test.com", student_password, "student", True,
                datetime.utcnow(), datetime.utcnow()
            ))
            
            # Commit les changements
            conn.commit()
            print("✅ Utilisateurs de test créés avec succès:")
            print("   - Professeur: prof_test (mot de passe: teacher123)")
            print("   - Étudiant: etudiant_test (mot de passe: student123)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs de test: {str(e)}")

if __name__ == "__main__":
    create_test_users() 