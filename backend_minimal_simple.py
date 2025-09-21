#!/usr/bin/env python3
"""
Script simple pour créer un backend minimal
"""
import os
import shutil

def create_minimal():
    """Crée un backend minimal"""
    
    print("🚀 Création du backend minimal...")
    
    # Créer le dossier
    if os.path.exists("backend_minimal"):
        shutil.rmtree("backend_minimal")
    os.makedirs("backend_minimal")
    
    # Fichiers essentiels à copier
    files_to_copy = [
        ("najah_ai_complete/backend/main.py", "backend_minimal/main.py"),
        ("najah_ai_complete/backend/api_router.py", "backend_minimal/api_router.py"),
        ("najah_ai_complete/backend/requirements.txt", "backend_minimal/requirements.txt"),
        ("backend/init_production_data.py", "backend_minimal/init_production_data.py"),
        ("backend/import_data.py", "backend_minimal/import_data.py"),
        ("backend/railway_start.py", "backend_minimal/railway_start.py")
    ]
    
    # Copier les fichiers
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ {os.path.basename(dst)}")
        else:
            print(f"⚠️ {src} non trouvé")
    
    # Copier les dossiers essentiels
    dirs_to_copy = [
        ("najah_ai_complete/backend/api", "backend_minimal/api"),
        ("najah_ai_complete/backend/app", "backend_minimal/app"),
        ("najah_ai_complete/backend/models", "backend_minimal/models"),
        ("najah_ai_complete/backend/schemas", "backend_minimal/schemas"),
        ("najah_ai_complete/backend/services", "backend_minimal/services"),
        ("najah_ai_complete/backend/core", "backend_minimal/core")
    ]
    
    for src, dst in dirs_to_copy:
        if os.path.exists(src):
            try:
                shutil.copytree(src, dst)
                print(f"📁 {os.path.basename(dst)}/")
            except Exception as e:
                print(f"⚠️ Erreur copie {src}: {e}")
        else:
            print(f"⚠️ {src} non trouvé")
    
    # Calculer la taille
    total_size = 0
    for root, dirs, files in os.walk("backend_minimal"):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    size_mb = total_size / (1024 * 1024)
    
    print(f"\n✅ Backend minimal créé !")
    print(f"📁 Dossier: backend_minimal/")
    print(f"📏 Taille: {size_mb:.2f} MB")
    
    if size_mb < 50:
        print("✅ Taille acceptable pour Railway CLI")
    else:
        print("⚠️ Encore un peu volumineux")

if __name__ == "__main__":
    create_minimal()

