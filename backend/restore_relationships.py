#!/usr/bin/env python3
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
