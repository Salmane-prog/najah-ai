#!/usr/bin/env python3
"""
Crée un dossier backend minimal pour Railway
Inclut seulement les fichiers essentiels
"""
import os
import shutil
from pathlib import Path

def create_minimal_backend():
    """Crée un backend minimal pour Railway"""
    
    print("🚀 CRÉATION D'UN BACKEND MINIMAL POUR RAILWAY")
    print("="*50)
    
    # Créer le dossier minimal
    minimal_dir = "backend_minimal"
    if os.path.exists(minimal_dir):
        shutil.rmtree(minimal_dir)
    os.makedirs(minimal_dir)
    
    # Fichiers essentiels à copier
    essential_files = [
        "main.py",
        "requirements.txt", 
        "api_router.py"
    ]
    
    # Dossiers essentiels à copier
    essential_dirs = [
        "api",
        "app", 
        "core",
        "models",
        "schemas",
        "services"
    ]
    
    # Scripts d'initialisation
    init_scripts = [
        "init_production_data.py",
        "import_data.py", 
        "railway_start.py"
    ]
    
    print("📁 Copie des fichiers essentiels...")
    
    # Copier les fichiers essentiels
    for file in essential_files:
        src = f"backend/{file}"
        if os.path.exists(src):
            shutil.copy2(src, f"{minimal_dir}/{file}")
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file} non trouvé")
    
    # Copier les scripts d'initialisation
    for script in init_scripts:
        src = f"backend/{script}"
        if os.path.exists(src):
            shutil.copy2(src, f"{minimal_dir}/{script}")
            print(f"✅ {script}")
        else:
            print(f"⚠️ {script} non trouvé")
    
    # Copier les dossiers essentiels
    for dir_name in essential_dirs:
        src = f"backend/{dir_name}"
        dst = f"{minimal_dir}/{dir_name}"
        if os.path.exists(src):
            shutil.copytree(src, dst, ignore=ignore_files)
            print(f"📁 {dir_name}/")
        else:
            print(f"⚠️ {dir_name}/ non trouvé")
    
    # Copier les données d'export
    data_files = [
        "data_export_app_db.json",
        "data_export_najah_ai_db.json"
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            shutil.copy2(data_file, f"{minimal_dir}/{data_file}")
            print(f"📊 {data_file}")
    
    # Créer un .railwayignore simple
    with open(f"{minimal_dir}/.railwayignore", "w") as f:
        f.write("""# Données temporaires
*.log
__pycache__/
.pytest_cache/
""")
    
    # Calculer la taille
    total_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(minimal_dir)
        for filename in filenames
    ) / (1024 * 1024)  # En MB
    
    print(f"\n📦 Backend minimal créé:")
    print(f"📁 Dossier: {minimal_dir}/")
    print(f"📏 Taille: {total_size:.2f} MB")
    
    if total_size > 500:
        print("⚠️ Toujours trop volumineux, vérifiez le contenu")
    else:
        print("✅ Taille acceptable pour Railway")
    
    return minimal_dir

def ignore_files(dir, files):
    """Ignore les fichiers inutiles lors de la copie"""
    ignore = []
    for file in files:
        if (file.endswith(('.db', '.sqlite', '.log', '.pyc')) or
            file.startswith(('test_', 'check_', 'fix_', 'debug_')) or
            file in ['__pycache__', 'node_modules', 'venv', '.pytest_cache')):
            ignore.append(file)
    return ignore

if __name__ == "__main__":
    minimal_dir = create_minimal_backend()
    print(f"\n🚀 Maintenant exécutez:")
    print(f"cd {minimal_dir}")
    print(f"railway up")

