#!/usr/bin/env python3
"""
Script pour redémarrer le serveur avec un moteur SQLAlchemy propre
"""

import os
import sys
import subprocess
import time

def restart_server_clean():
    print("=== REDÉMARRAGE DU SERVEUR AVEC MOTEUR PROPRE ===")
    
    # Arrêter le serveur existant s'il tourne
    print("1. Arrêt du serveur existant...")
    try:
        # Sur Windows, chercher le processus uvicorn
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        if 'uvicorn' in result.stdout:
            print("⚠️  Serveur détecté en cours d'exécution")
            print("   Veuillez arrêter manuellement le serveur (Ctrl+C)")
            print("   puis relancer ce script")
            return
    except Exception as e:
        print(f"⚠️  Impossible de vérifier les processus: {e}")
    
    print("✅ Serveur arrêté ou non détecté")
    
    # Nettoyer les fichiers de cache Python
    print("\n2. Nettoyage des caches Python...")
    cache_dirs = ['__pycache__', '.pytest_cache']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"✅ Cache supprimé: {cache_dir}")
            except Exception as e:
                print(f"⚠️  Impossible de supprimer {cache_dir}: {e}")
    
    # Supprimer les fichiers .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"✅ Fichier .pyc supprimé: {file}")
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {file}: {e}")
    
    print("✅ Nettoyage terminé")
    
    # Vérifier la base de données
    print("\n3. Vérification de la base de données...")
    try:
        import sqlite3
        db_path = "data/app.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Vérifier la table contents
            cursor.execute("PRAGMA table_info(contents)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print(f"✅ Base de données trouvée avec {len(columns)} colonnes")
            
            # Vérifier les colonnes critiques
            critical_columns = ['content_type', 'created_by']
            for col in critical_columns:
                if col in column_names:
                    print(f"✅ Colonne '{col}' présente")
                else:
                    print(f"❌ Colonne '{col}' manquante")
            
            conn.close()
        else:
            print("❌ Base de données non trouvée")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la base: {e}")
    
    # Redémarrer le serveur
    print("\n4. Redémarrage du serveur...")
    print("   Commande: uvicorn app:app --reload --port 8000")
    print("   Appuyez sur Ctrl+C pour arrêter le serveur")
    print("\n" + "="*50)
    
    try:
        # Lancer le serveur
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app:app', '--reload', '--port', '8000'
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n✅ Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")

if __name__ == "__main__":
    restart_server_clean() 