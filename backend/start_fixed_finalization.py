#!/usr/bin/env python3
"""
🚀 DÉMARRAGE AVEC FINALISATION CORRIGÉE
Répare la base de données et teste la finalisation avant de démarrer le serveur
"""

import sys
import os
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """Exécuter un script Python"""
    print(f"\n🔧 {description}...")
    print(f"   Exécution de: {script_name}")
    
    try:
        result = subprocess.run([
            sys.executable, script_name
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"   ✅ {description} réussi")
            print(result.stdout)
            return True
        else:
            print(f"   ❌ {description} échoué")
            print(f"   Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de l'exécution: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE AVEC FINALISATION CORRIGÉE")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    current_dir = Path(__file__).parent
    if not (current_dir / "services").exists():
        print("❌ Ce script doit être exécuté depuis le répertoire backend")
        return False
    
    print(f"📁 Répertoire de travail: {current_dir}")
    
    # Étape 1: Réparer la base de données
    if not run_script("repair_test_database.py", "Réparation de la base de données"):
        print("❌ Impossible de réparer la base de données")
        return False
    
    # Étape 2: Tester la finalisation
    if not run_script("test_finalization.py", "Test de la finalisation"):
        print("❌ Le test de finalisation a échoué")
        print("   La finalisation n'est pas encore corrigée")
        return False
    
    # Étape 3: Démarrer le serveur
    print("\n🚀 Démarrage du serveur d'évaluation...")
    print("   Le serveur va démarrer sur http://localhost:8000")
    print("   Le frontend est accessible sur http://localhost:3001")
    print("\n   Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 50)
    
    try:
        # Démarrer le serveur
        subprocess.run([
            sys.executable, "start_assessment_system.py"
        ], cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
        return True
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage du serveur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 DÉMARRAGE AVEC FINALISATION CORRIGÉE")
    print("=" * 50)
    
    success = main()
    
    if success:
        print("\n🎉 DÉMARRAGE RÉUSSI !")
        print("✅ Base de données réparée")
        print("✅ Finalisation testée et validée")
        print("✅ Serveur démarré")
        print("\n📱 Testez maintenant:")
        print("   Frontend: http://localhost:3001/dashboard/student/assessment")
        print("   Backend: http://localhost:8000")
    else:
        print("\n❌ DÉMARRAGE ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus")
    
    print("\n" + "=" * 50)





