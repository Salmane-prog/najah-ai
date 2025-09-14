#!/usr/bin/env python3
"""
Script pour vérifier l'intégration de la sidebar dans toutes les pages
"""

import os
import re

def check_sidebar_integration():
    """Vérifier que toutes les pages ont la sidebar intégrée"""
    
    # Pages à vérifier
    pages_to_check = [
        "../frontend/src/app/dashboard/teacher/messages/page.tsx",
        "../frontend/src/app/dashboard/student/messages/page.tsx", 
        "../frontend/src/app/dashboard/student/notes/page.tsx",
        "../frontend/src/app/dashboard/student/assessment/page.tsx",
        "../frontend/src/app/dashboard/student/learning-path/page.tsx",
        "../frontend/src/app/dashboard/student/courses/page.tsx"
    ]
    
    print("🔍 Vérification de l'intégration de la sidebar...")
    
    for page_path in pages_to_check:
        if os.path.exists(page_path):
            print(f"\n📄 Vérification de {page_path}")
            
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier l'import de Sidebar
                sidebar_import = re.search(r'import.*Sidebar.*from', content)
                if sidebar_import:
                    print("   ✅ Import Sidebar trouvé")
                else:
                    print("   ❌ Import Sidebar manquant")
                
                # Vérifier l'utilisation de Sidebar dans le JSX
                sidebar_usage = re.search(r'<Sidebar\s*/>', content)
                if sidebar_usage:
                    print("   ✅ Composant Sidebar utilisé")
                else:
                    print("   ❌ Composant Sidebar non utilisé")
                
                # Vérifier la structure avec ml-64 (margin-left pour la sidebar)
                ml_64_usage = re.search(r'ml-64', content)
                if ml_64_usage:
                    print("   ✅ Structure avec ml-64 trouvée")
                else:
                    print("   ❌ Structure ml-64 manquante")
                
                # Vérifier la structure flex
                flex_structure = re.search(r'flex.*h-screen.*bg-gray-50', content)
                if flex_structure:
                    print("   ✅ Structure flex correcte")
                else:
                    print("   ❌ Structure flex manquante")
                    
            except Exception as e:
                print(f"   ❌ Erreur lors de la lecture: {e}")
        else:
            print(f"\n❌ Fichier non trouvé: {page_path}")
    
    print("\n✅ Vérification terminée !")

if __name__ == "__main__":
    check_sidebar_integration() 