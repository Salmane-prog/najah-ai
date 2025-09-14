#!/usr/bin/env python3
import os
import sqlite3
import datetime
from core.database import SessionLocal, engine
from core.config import settings
from models.user import User, UserRole
from core.security import get_password_hash

def check_database_path():
    """Vérifier le chemin exact de la base de données"""
    print("🗄️ Vérification du chemin de la base de données...")
    
    # Vérifier la configuration
    print(f"📋 Configuration:")
    print(f"   SQLALCHEMY_DATABASE_URL: {settings.SQLALCHEMY_DATABASE_URL}")
    
    # Vérifier le chemin absolu
    db_path = os.path.abspath("../../data/app.db")
    print(f"   Chemin absolu: {db_path}")
    
    # Vérifier si le fichier existe
    if os.path.exists(db_path):
        print(f"✅ Fichier de base de données trouvé: {db_path}")
        file_size = os.path.getsize(db_path)
        print(f"   Taille: {file_size} bytes")
        
        # Vérifier la date de modification
        mtime = os.path.getmtime(db_path)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   Dernière modification: {mtime_str}")
    else:
        print(f"❌ Fichier de base de données non trouvé: {db_path}")
    
    # Vérifier le chemin via SQLAlchemy
    print(f"\n🔗 Chemin via SQLAlchemy:")
    if "sqlite" in str(engine.url):
        abs_path = os.path.abspath(engine.url.database)
        print(f"   Chemin SQLAlchemy: {abs_path}")
        if os.path.exists(abs_path):
            print(f"   ✅ Fichier SQLAlchemy trouvé")
        else:
            print(f"   ❌ Fichier SQLAlchemy non trouvé")

def check_database_content():
    """Vérifier le contenu de la base de données"""
    print(f"\n📊 Contenu de la base de données:")
    
    try:
        # Connexion directe à SQLite
        db_path = os.path.abspath("../../data/app.db")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Lister toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"   Tables trouvées: {[table[0] for table in tables]}")
            
            # Vérifier la table users
            if ('users',) in tables:
                cursor.execute("SELECT COUNT(*) FROM users;")
                user_count = cursor.fetchone()[0]
                print(f"   Nombre d'utilisateurs: {user_count}")
                
                # Afficher tous les utilisateurs
                cursor.execute("SELECT id, username, email, role FROM users;")
                users = cursor.fetchall()
                print(f"   Utilisateurs:")
                for user in users:
                    print(f"     • ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
            
            conn.close()
        else:
            print("   ❌ Fichier de base de données non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")

def sync_users_with_real_data():
    """Synchroniser les utilisateurs avec les vraies données"""
    print(f"\n🔄 Synchronisation des utilisateurs...")
    
    db = SessionLocal()
    try:
        # Supprimer tous les utilisateurs existants
        print("🗑️ Suppression des anciens utilisateurs...")
        db.query(User).delete()
        db.commit()
        print("✅ Anciens utilisateurs supprimés")
        
        # Créer les utilisateurs réels basés sur votre interface
        real_users = [
            {
                "username": "admin",
                "email": "admin@najah.ai",
                "password": "admin123",
                "role": UserRole.teacher
            },
            {
                "username": "salmane",
                "email": "marie.dubois@najah.ai",
                "password": "salmane123@",
                "role": UserRole.teacher
            },
            {
                "username": "teacher2",
                "email": "ahmed.benali@najah.ai",
                "password": "teacher123",
                "role": UserRole.teacher
            },
            {
                "username": "student1",
                "email": "salmane.hajouji@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "student2",
                "email": "fatima.alami@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "student3",
                "email": "omar.benjelloun@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "teacher_test",
                "email": "teacher@test.com",
                "password": "password123",
                "role": UserRole.teacher
            },
            {
                "username": "student_test",
                "email": "student@test.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "marie.dubois",
                "email": "marie.dubois@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "jean.martin",
                "email": "jean.martin@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "sophie.bernard",
                "email": "sophie.bernard@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "pierre.durand",
                "email": "pierre.durand@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "superadmin",
                "email": "superadmin@najah.ai",
                "password": "admin123",
                "role": UserRole.admin
            }
        ]
        
        print("👥 Création des utilisateurs réels...")
        for user_data in real_users:
            hashed_password = get_password_hash(user_data["password"])
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            db.add(new_user)
            print(f"   ✅ {user_data['email']} ({user_data['password']}) - {user_data['role']}")
        
        db.commit()
        print("✅ Synchronisation terminée!")
        
        # Afficher tous les utilisateurs
        print("\n📋 Liste des utilisateurs disponibles:")
        users = db.query(User).all()
        for user in users:
            print(f"   • {user.username} ({user.email}) - {user.role}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        db.rollback()
    finally:
        db.close()

def test_login_marie():
    """Tester la connexion avec marie.dubois@najah.ai"""
    print("\n🔐 Test de connexion avec marie.dubois@najah.ai...")
    
    import requests
    import json
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "email": "marie.dubois@najah.ai",
                "password": "salmane123@"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie!")
            print(f"   Token: {data.get('access_token', '')[:20]}...")
            print(f"   Role: {data.get('role', '')}")
            print(f"   ID: {data.get('id', '')}")
            print(f"   Name: {data.get('name', '')}")
            return True
        else:
            print("❌ Échec de connexion")
            try:
                error_data = response.json()
                print(f"   Erreur: {error_data.get('detail', '')}")
            except:
                print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    print("🔧 Correction du chemin de base de données - Najah AI")
    print("=" * 60)
    
    # Vérifier le chemin de la base de données
    check_database_path()
    check_database_content()
    
    # Synchroniser les utilisateurs
    sync_users_with_real_data()
    
    # Tester la connexion
    test_login_marie()
    
    print("\n" + "=" * 60)
    print("🏁 Correction terminée")
    print("\n📋 Comptes principaux:")
    print("   • marie.dubois@najah.ai (salmane123@) - Enseignant")
    print("   • student@test.com (password123) - Étudiant")
    print("   • teacher@test.com (password123) - Enseignant")
    print("   • admin@najah.ai (admin123) - Administrateur")

if __name__ == "__main__":
    main() 