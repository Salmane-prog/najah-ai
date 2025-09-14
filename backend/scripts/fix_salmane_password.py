#!/usr/bin/env python3
"""
Script pour définir un mot de passe simple pour salmane
"""

import sqlite3
from pathlib import Path
import hashlib

def fix_salmane_password():
    """Définir un mot de passe simple pour salmane."""
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== CORRECTION MOT DE PASSE SALMANE ===")
        
        # Vérifier si l'utilisateur existe
        cursor.execute("""
            SELECT id, email, username 
            FROM users 
            WHERE email = 'salmane.hajouji@najah.ai'
        """)
        
        user = cursor.fetchone()
        
        if not user:
            print("❌ Utilisateur salmane.hajouji@najah.ai non trouvé")
            return
        
        user_id, email, username = user
        print(f"✅ Utilisateur trouvé: {email}")
        print(f"   Username: {username}")
        print(f"   ID: {user_id}")
        
        # Créer un hash simple pour "password123"
        new_password = "password123"
        # Hash simple (pas bcrypt pour éviter les problèmes)
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Mettre à jour le mot de passe
        cursor.execute("""
            UPDATE users 
            SET hashed_password = ? 
            WHERE id = ?
        """, (hashed_password, user_id))
        
        conn.commit()
        
        print(f"✅ Mot de passe mis à jour pour '{email}'")
        print(f"   Nouveau mot de passe: {new_password}")
        print(f"   Hash: {hashed_password}")
        
        # Vérifier la mise à jour
        cursor.execute("""
            SELECT hashed_password 
            FROM users 
            WHERE id = ?
        """, (user_id,))
        
        updated_hash = cursor.fetchone()[0]
        print(f"✅ Vérification: Hash mis à jour: {updated_hash[:20]}...")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_salmane_password() 