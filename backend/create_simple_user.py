#!/usr/bin/env python3
"""
Script simple pour créer un utilisateur de test dans la base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from core.config import settings

def create_simple_test_user():
    # Créer une connexion directe à la base de données
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        # Vérifier si l'utilisateur existe déjà
        result = conn.execute(text("SELECT id FROM users WHERE email = 'teacher@test.com'"))
        if result.fetchone():
            print("Utilisateur teacher@test.com existe déjà")
            return
        
        # Créer un utilisateur professeur de test avec mot de passe hashé
        from core.security import get_password_hash
        hashed_password = get_password_hash("teacher123")
        
        # Insérer directement dans la base de données
        conn.execute(text("""
            INSERT INTO users (username, email, hashed_password, role)
            VALUES ('teacher_test', 'teacher@test.com', :password, 'teacher')
        """), {"password": hashed_password})
        
        # Créer aussi un étudiant de test
        result = conn.execute(text("SELECT id FROM users WHERE email = 'student@test.com'"))
        if not result.fetchone():
            hashed_password_student = get_password_hash("student123")
            conn.execute(text("""
                INSERT INTO users (username, email, hashed_password, role)
                VALUES ('student_test', 'student@test.com', :password, 'student')
            """), {"password": hashed_password_student})
        
        conn.commit()
        
        print("Utilisateurs créés avec succès!")
        print("Professeur:")
        print("  Email: teacher@test.com")
        print("  Mot de passe: teacher123")
        print("Étudiant:")
        print("  Email: student@test.com")
        print("  Mot de passe: student123")

if __name__ == "__main__":
    create_simple_test_user() 