#!/usr/bin/env python3
"""
Script pour forcer la recréation complète de la base de données
"""

import os
import sys
import sqlite3

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def force_recreate_database():
    """Force la recréation complète de la base de données"""
    print("Suppression forcée de la base de donnees...")
    
    # Chemin de la base de données
    db_path = "data/app.db"
    
    # Supprimer le fichier s'il existe
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Base de donnees supprimee avec succes")
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
    else:
        print("Base de donnees n'existait pas")
    
    # Créer le répertoire data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    # Créer une nouvelle base de données vide
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        print("Nouvelle base de donnees creee")
    except Exception as e:
        print(f"Erreur lors de la creation: {e}")
        return False
    
    print("Base de donnees prete pour la recreation")
    return True

if __name__ == "__main__":
    print("Demarrage de la suppression forcee de la base de donnees...")
    if force_recreate_database():
        print("Maintenant lancez: python simple_recreate_database.py")
    else:
        print("Erreur lors de la suppression")
