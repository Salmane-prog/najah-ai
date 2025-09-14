#!/usr/bin/env python3
"""
Script pour mettre à jour le mot de passe de l'utilisateur salmane
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from passlib.context import CryptContext

def update_user_password():
    """Mettre à jour le mot de passe de l'utilisateur salmane"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    # Contexte de hachage
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Nouveau mot de passe
    new_password = "password123"
    hashed_password = pwd_context.hash(new_password)
    
    try:
        with engine.connect() as conn:
            # Mettre à jour le mot de passe
            result = conn.execute(text("""
                UPDATE users 
                SET hashed_password = :hashed_password 
                WHERE email = 'salmane.hajouji@najah.ai'
            """), {"hashed_password": hashed_password})
            
            # Commit les changements
            conn.commit()
            
            # Vérifier si l'utilisateur a été mis à jour
            if result.rowcount > 0:
                print(f"✅ Mot de passe mis à jour pour salmane.hajouji@najah.ai")
                print(f"   Nouveau mot de passe: {new_password}")
                print(f"   Hash: {hashed_password[:50]}...")
                
                # Vérifier que le hash fonctionne
                is_valid = pwd_context.verify(new_password, hashed_password)
                print(f"   Vérification du hash: {'✅' if is_valid else '❌'}")
                
            else:
                print("❌ Utilisateur non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    update_user_password() 