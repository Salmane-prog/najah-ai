#!/usr/bin/env python3
"""
Script pour créer un ZIP optimisé pour upload GitHub
Inclut seulement les fichiers nécessaires pour le déploiement
"""
import os
import zipfile
import shutil
from pathlib import Path

def create_github_zip():
    """Crée un ZIP optimisé pour GitHub"""
    
    zip_filename = "najah_ai_github.zip"
    
    # Dossiers à inclure complètement
    include_dirs = [
        "frontend",
        "backend", 
        "api"
    ]
    
    # Dossiers à inclure partiellement (sans certains fichiers)
    partial_dirs = {
        "data": [".db", ".sqlite", ".sqlite3"]  # Exclure les bases de données
    }
    
    # Fichiers spécifiques à inclure
    include_files = [
        ".gitignore",
        "requirements.txt", 
        "railway.toml",
        "Procfile",
        "railway.json",
        "docker-compose.yml",
        "docker-compose.prod.yml", 
        "Dockerfile.frontend",
        "Dockerfile.backend",
        "nginx.conf",
        "README.md",
        "DEPLOYMENT_COMPLETE_GUIDE.md",
        "export_data.py"
    ]
    
    # Fichiers d'export de données (optionnel)
    data_files = [
        "data_export_app_db.json",
        "data_export_najah_ai_db.json", 
        "summary_app_db.txt",
        "summary_najah_ai_db.txt"
    ]
    
    # Extensions à exclure globalement
    exclude_extensions = [".db", ".sqlite", ".sqlite3", ".log"]
    
    # Dossiers à exclure globalement
    exclude_dirs = ["node_modules", "__pycache__", ".next", "tmp", "temp", ".git"]
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            print(f"🚀 Création du ZIP pour GitHub: {zip_filename}")
            print("="*50)
            
            # Ajouter les dossiers complets
            for dir_name in include_dirs:
                if os.path.exists(dir_name):
                    print(f"📁 Ajout du dossier: {dir_name}/")
                    add_directory_to_zip(zipf, dir_name, exclude_dirs, exclude_extensions)
                else:
                    print(f"⚠️ Dossier non trouvé: {dir_name}")
            
            # Ajouter les dossiers partiels
            for dir_name, exclude_exts in partial_dirs.items():
                if os.path.exists(dir_name):
                    print(f"📁 Ajout partiel du dossier: {dir_name}/ (sans {exclude_exts})")
                    add_directory_to_zip(zipf, dir_name, exclude_dirs, exclude_exts)
                else:
                    print(f"⚠️ Dossier non trouvé: {dir_name}")
            
            # Ajouter les fichiers spécifiques
            for file_name in include_files:
                if os.path.exists(file_name):
                    zipf.write(file_name)
                    print(f"📄 Ajout du fichier: {file_name}")
                else:
                    print(f"⚠️ Fichier non trouvé: {file_name}")
            
            # Ajouter les fichiers de données (optionnel)
            print(f"\n📊 Fichiers de données (optionnel):")
            for file_name in data_files:
                if os.path.exists(file_name):
                    zipf.write(file_name)
                    print(f"📄 Ajout des données: {file_name}")
                else:
                    print(f"⚠️ Données non trouvées: {file_name}")
        
        # Informations sur le ZIP créé
        zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # En MB
        print(f"\n✅ ZIP créé avec succès!")
        print(f"📦 Fichier: {zip_filename}")
        print(f"📏 Taille: {zip_size:.2f} MB")
        print(f"\n🚀 Prêt pour upload sur GitHub!")
        
        return zip_filename
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du ZIP: {e}")
        return None

def add_directory_to_zip(zipf, dir_path, exclude_dirs, exclude_extensions):
    """Ajoute un dossier au ZIP en excluant certains éléments"""
    
    for root, dirs, files in os.walk(dir_path):
        # Exclure les dossiers indésirables
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Exclure les extensions indésirables
            if not any(file.endswith(ext) for ext in exclude_extensions):
                file_path = os.path.join(root, file)
                zipf.write(file_path)

def show_zip_contents():
    """Affiche le contenu du ZIP créé"""
    zip_filename = "najah_ai_github.zip"
    
    if not os.path.exists(zip_filename):
        print(f"❌ Fichier ZIP non trouvé: {zip_filename}")
        return
    
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            files = zipf.namelist()
            print(f"\n📋 CONTENU DU ZIP ({len(files)} fichiers):")
            print("="*50)
            
            # Grouper par dossiers
            dirs = {}
            for file in files:
                if '/' in file:
                    dir_name = file.split('/')[0]
                    if dir_name not in dirs:
                        dirs[dir_name] = []
                    dirs[dir_name].append(file)
                else:
                    if 'root' not in dirs:
                        dirs['root'] = []
                    dirs['root'].append(file)
            
            for dir_name, dir_files in dirs.items():
                print(f"\n📁 {dir_name}/ ({len(dir_files)} fichiers)")
                for file in sorted(dir_files[:10]):  # Limiter l'affichage
                    print(f"   📄 {file}")
                if len(dir_files) > 10:
                    print(f"   ... et {len(dir_files) - 10} autres fichiers")
    
    except Exception as e:
        print(f"❌ Erreur lecture ZIP: {e}")

if __name__ == "__main__":
    print("🎯 CRÉATION DU ZIP POUR GITHUB")
    print("="*50)
    
    zip_file = create_github_zip()
    
    if zip_file:
        print("\n" + "="*50)
        show_zip_contents()
        
        print(f"\n🎯 INSTRUCTIONS POUR GITHUB:")
        print(f"1. Aller sur https://github.com/Salmane-prog/Najah_AI")
        print(f"2. Cliquer 'Add file' → 'Upload files'")
        print(f"3. Glisser-déposer le fichier: {zip_file}")
        print(f"4. GitHub l'extraira automatiquement")
        print(f"5. Commit: 'Upload complete Najah AI project'")

