#!/usr/bin/env python3
"""
Script pour corriger automatiquement toutes les utilisations de require_role
"""

import os
import re
import glob

def fix_require_role_in_file(file_path):
    """Corriger les utilisations de require_role dans un fichier"""
    print(f"Correction de {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver require_role("role1", "role2") ou require_role("role")
    pattern = r'require_role\("([^"]+)"(?:,\s*"([^"]+)")*\)'
    
    def replace_require_role(match):
        roles = [match.group(1)]
        if match.group(2):
            roles.append(match.group(2))
        return f'require_role({roles})'
    
    # Appliquer la correction
    new_content = re.sub(pattern, replace_require_role, content)
    
    # Écrire le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {file_path} corrigé")

def main():
    """Corriger tous les fichiers Python dans api/v1/"""
    api_dir = "api/v1"
    
    if not os.path.exists(api_dir):
        print(f"❌ Répertoire {api_dir} non trouvé")
        return
    
    # Trouver tous les fichiers Python
    python_files = glob.glob(f"{api_dir}/*.py")
    
    print(f"🔧 Correction de {len(python_files)} fichiers...")
    
    for file_path in python_files:
        try:
            fix_require_role_in_file(file_path)
        except Exception as e:
            print(f"❌ Erreur lors de la correction de {file_path}: {e}")
    
    print("🎉 Correction terminée !")

if __name__ == "__main__":
    main() 