#!/usr/bin/env python3
"""
Script pour corriger temporairement les relations problématiques
"""

import os
import sys

def fix_relationships():
    print("=== CORRECTION DES RELATIONSHIPS PROBLÉMATIQUES ===")
    
    # Liste des fichiers à modifier temporairement
    files_to_fix = [
        "models/user.py",
        "models/content.py",
        "models/category.py",
        "models/learning_path.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"\nVérification de {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Sauvegarder le fichier original
            backup_path = f"{file_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Sauvegarde créée: {backup_path}")
            
            # Commenter les relations problématiques
            lines = content.split('\n')
            modified = False
            
            for i, line in enumerate(lines):
                # Commenter les relations qui font référence à d'autres modèles
                if any(keyword in line for keyword in [
                    'relationship("Content"',
                    'relationship("User"',
                    'relationship("Category"',
                    'relationship("LearningPath"',
                    'back_populates="contents"',
                    'back_populates="creator"',
                    'back_populates="category"',
                    'back_populates="learning_paths"'
                ]) and not line.strip().startswith('#'):
                    lines[i] = f"# {line}  # Commenté temporairement"
                    modified = True
                    print(f"  - Commenté: {line.strip()}")
            
            if modified:
                # Écrire le fichier modifié
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                print(f"✅ Fichier modifié: {file_path}")
            else:
                print(f"✅ Aucune modification nécessaire: {file_path}")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")
    
    print("\n=== CRÉATION D'UN SCRIPT DE RESTAURATION ===")
    
    # Créer un script de restauration
    restore_script = '''#!/usr/bin/env python3
"""
Script pour restaurer les fichiers originaux
"""

import os
import glob

def restore_files():
    print("=== RESTAURATION DES FICHIERS ORIGINAUX ===")
    
    # Restaurer tous les fichiers .backup
    backup_files = glob.glob("*.backup")
    
    for backup_file in backup_files:
        original_file = backup_file.replace('.backup', '')
        
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(original_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            os.remove(backup_file)
            print(f"✅ Restauré: {original_file}")
    
    print("🎉 Restauration terminée!")

if __name__ == "__main__":
    restore_files()
'''
    
    with open('restore_relationships.py', 'w', encoding='utf-8') as f:
        f.write(restore_script)
    
    print("✅ Script de restauration créé: restore_relationships.py")
    print("\n🎉 Correction des relationships terminée!")
    print("\nPour restaurer les fichiers originaux plus tard:")
    print("  python restore_relationships.py")

if __name__ == "__main__":
    fix_relationships() 