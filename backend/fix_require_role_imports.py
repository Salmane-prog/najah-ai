#!/usr/bin/env python3
"""
Script pour corriger automatiquement tous les imports require_role
"""

import os
import re

def fix_require_role_imports():
    """Corriger tous les imports require_role dans les fichiers Python"""
    
    # Liste des fichiers à corriger
    files_to_fix = [
        "api/v1/notifications.py",
        "api/v1/quiz_json.py", 
        "api/v1/recommendations.py",
        "api/v1/reports.py",
        "api/v1/score_corrections.py",
        "api/v1/quizzes.py",
        "api/v1/student_performance.py",
        "api/v1/teacher_collaboration.py",
        "api/v1/settings.py",
        "api/v1/remediation.py",
        "api/v1/learning_paths.py",
        "api/v1/learning_history.py",
        "api/v1/teacher_messaging.py",
        "api/v1/gamification.py",
        "api/v1/external_integrations.py",
        "api/v1/teacher_schedule.py",
        "api/v1/export_reports.py",
        "api/v1/continuous_assessment.py",
        "api/v1/contents.py",
        "api/v1/class_groups.py",
        "api/v1/categories.py",
        "api/v1/badges.py",
        "api/v1/calendar.py",
        "api/v1/auto_correction.py",
        "api/v1/advanced_analytics.py",
        "api/v1/activity.py"
    ]
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            print(f"⚠️  Fichier non trouvé: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si le fichier contient l'import problématique
            if "from api.v1.users import" in content and "require_role" in content:
                # Remplacer l'import
                old_import = "from api.v1.users import get_current_user, require_role"
                new_import = "from api.v1.users import get_current_user\nfrom api.v1.auth import require_role"
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    print(f"✅ Corrigé: {file_path}")
                    fixed_count += 1
                else:
                    # Chercher d'autres patterns
                    pattern = r"from api\.v1\.users import.*require_role"
                    if re.search(pattern, content):
                        # Remplacer par l'import séparé
                        content = re.sub(pattern, "from api.v1.users import get_current_user\nfrom api.v1.auth import require_role", content)
                        print(f"✅ Corrigé (pattern): {file_path}")
                        fixed_count += 1
                    else:
                        print(f"⚠️  Pattern non trouvé dans: {file_path}")
            
            # Écrire le fichier modifié
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    print(f"\n📊 Résumé: {fixed_count} fichiers corrigés")
    return fixed_count

if __name__ == "__main__":
    print("🔧 Correction des imports require_role...")
    fixed = fix_require_role_imports()
    if fixed > 0:
        print("✅ Corrections terminées!")
    else:
        print("⚠️  Aucune correction nécessaire") 