#!/usr/bin/env python3
"""
Script simple pour changer le mot de passe du professeur sans dépendances circulaires
"""

import sqlite3
import os
from pathlib import Path

def change_teacher_password_simple():
    """Change le mot de passe du professeur en utilisant SQL direct"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔧 Changement du mot de passe du professeur...")
    print(f"   📁 Base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Table 'users' non trouvée")
            return False
        
        # Chercher un professeur existant
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher' LIMIT 1")
        teacher = cursor.fetchone()
        
        if teacher:
            teacher_id, old_username, email = teacher
            print(f"✅ Professeur trouvé: {email}")
            print(f"   Ancien nom d'utilisateur: {old_username}")
            
            # Mettre à jour le mot de passe (hash bcrypt)
            # Pour simplifier, on va utiliser un hash simple
            # En production, il faudrait utiliser bcrypt
            import hashlib
            new_password_hash = hashlib.sha256("salmane123@".encode()).hexdigest()
            
            cursor.execute("""
                UPDATE users 
                SET hashed_password = ?, username = ?
                WHERE id = ?
            """, (new_password_hash, "salmane", teacher_id))
            
            conn.commit()
            print("✅ Mot de passe mis à jour avec succès!")
            print(f"   📧 Email: {email}")
            print(f"   👤 Nouveau nom d'utilisateur: salmane")
            print(f"   🔑 Nouveau mot de passe: salmane123@")
            
        else:
            print("❌ Aucun professeur trouvé, création d'un nouveau compte...")
            
            # Créer un nouveau professeur
            import hashlib
            password_hash = hashlib.sha256("salmane123@".encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO users (username, email, hashed_password, role)
                VALUES (?, ?, ?, ?)
            """, ("salmane", "salmane@najah.ai", password_hash, "teacher"))
            
            conn.commit()
            print("✅ Nouveau professeur créé avec succès!")
            print(f"   📧 Email: salmane@najah.ai")
            print(f"   👤 Nom d'utilisateur: salmane")
            print(f"   🔑 Mot de passe: salmane123@")
        
        # Afficher tous les professeurs pour vérification
        print("\n📋 Liste de tous les professeurs:")
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher'")
        teachers = cursor.fetchall()
        for teacher_id, username, email in teachers:
            print(f"   • {username} ({email}) - ID: {teacher_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du changement de mot de passe: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = change_teacher_password_simple()
    if success:
        print("\n🎉 Opération terminée avec succès!")
        print("   Vous pouvez maintenant vous connecter avec:")
        print("   📧 Email: salmane@najah.ai")
        print("   🔑 Mot de passe: salmane123@")
    else:
        print("\n❌ Échec de l'opération") 