#!/usr/bin/env python3
"""
Script pour corriger le mot de passe de l'utilisateur student1
"""

import sqlite3
import bcrypt
import os
import sys

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.database import get_db
from backend.core.security import get_password_hash

def fix_user_password():
    """Corriger le mot de passe de l'utilisateur student1"""
    
    print("🔧 Correction du mot de passe utilisateur...")
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Nouveau mot de passe
        new_password = "password123"
        
        # Hasher le nouveau mot de passe
        hashed_password = get_password_hash(new_password)
        
        print(f"🔑 Nouveau hash généré : {hashed_password}")
        
        # Mettre à jour le mot de passe de l'utilisateur student1
        cursor.execute("""
            UPDATE users 
            SET hashed_password = ? 
            WHERE username = 'student1'
        """, (hashed_password,))
        
        # Vérifier si la mise à jour a été effectuée
        if cursor.rowcount > 0:
            print("✅ Mot de passe mis à jour avec succès !")
            
            # Vérifier la mise à jour
            cursor.execute("""
                SELECT username, email, hashed_password 
                FROM users 
                WHERE username = 'student1'
            """)
            
            user = cursor.fetchone()
            if user:
                print(f"👤 Utilisateur : {user[0]}")
                print(f"📧 Email : {user[1]}")
                print(f"🔑 Nouveau hash : {user[2]}")
                print(f"🔑 Mot de passe : {new_password}")
        else:
            print("❌ Aucun utilisateur 'student1' trouvé")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Mot de passe corrigé !")
        print(f"📝 Identifiants de test :")
        print(f"   Email : salmane.hajouji@najah.ai")
        print(f"   Mot de passe : {new_password}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_user_password() 