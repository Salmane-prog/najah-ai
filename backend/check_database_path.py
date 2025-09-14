#!/usr/bin/env python3
"""
Script pour vérifier le chemin exact de la base de données utilisée
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import settings
from pathlib import Path

def check_database_path():
    """Vérifier le chemin de la base de données"""
    print("🗄️ VÉRIFICATION DU CHEMIN DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    # Chemin depuis la configuration
    db_url = settings.SQLALCHEMY_DATABASE_URL
    print(f"📋 URL de la base de données: {db_url}")
    
    # Analyser le chemin
    if db_url.startswith("sqlite:///"):
        # Extraire le chemin relatif
        relative_path = db_url.replace("sqlite:///", "")
        print(f"📁 Chemin relatif: {relative_path}")
        
        # Chemin absolu depuis le backend
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(backend_dir, relative_path)
        print(f"📍 Chemin absolu depuis backend: {absolute_path}")
        
        # Chemin absolu depuis la racine du projet
        project_root = os.path.dirname(backend_dir)
        absolute_path_from_root = os.path.join(project_root, relative_path)
        print(f"🏠 Chemin absolu depuis racine: {absolute_path_from_root}")
        
        # Vérifier si le fichier existe
        if os.path.exists(absolute_path):
            print(f"✅ Base de données trouvée: {absolute_path}")
            file_size = os.path.getsize(absolute_path)
            print(f"📊 Taille du fichier: {file_size} octets")
        else:
            print(f"❌ Base de données non trouvée: {absolute_path}")
        
        if os.path.exists(absolute_path_from_root):
            print(f"✅ Base de données trouvée (racine): {absolute_path_from_root}")
            file_size = os.path.getsize(absolute_path_from_root)
            print(f"📊 Taille du fichier: {file_size} octets")
        else:
            print(f"❌ Base de données non trouvée (racine): {absolute_path_from_root}")
    
    print("\n📂 STRUCTURE DES RÉPERTOIRES:")
    print("-" * 40)
    
    # Afficher la structure des répertoires
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    
    print(f"📁 Backend: {backend_dir}")
    print(f"🏠 Racine projet: {project_root}")
    
    # Vérifier les fichiers de base de données
    possible_paths = [
        os.path.join(backend_dir, "data", "app.db"),
        os.path.join(project_root, "data", "app.db"),
        os.path.join(backend_dir, "app.db"),
        os.path.join(project_root, "app.db")
    ]
    
    print(f"\n🔍 RECHERCHE DE FICHIERS DE BASE DE DONNÉES:")
    for path in possible_paths:
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            print(f"✅ {path} ({file_size} octets)")
        else:
            print(f"❌ {path} (n'existe pas)")

if __name__ == "__main__":
    check_database_path() 