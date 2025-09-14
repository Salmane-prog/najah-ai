#!/usr/bin/env python3
"""
🚀 SCRIPT DE DÉMARRAGE AVEC RÉPARATION AUTOMATIQUE
Lance le serveur d'évaluation après avoir réparé la base de données
"""

import sys
import os
import subprocess
from pathlib import Path

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"\n🔧 {description}...")
    print(f"   Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} réussi")
            if result.stdout.strip():
                print(f"   Sortie: {result.stdout.strip()}")
        else:
            print(f"❌ {description} échoué")
            if result.stderr.strip():
                print(f"   Erreur: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de {description.lower()}: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    
    print("🚀 SYSTÈME D'ÉVALUATION INITIALE - DÉMARRAGE AVEC RÉPARATION")
    print("=" * 70)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("fix_database.py").exists():
        print("❌ ERREUR: Ce script doit être exécuté depuis le répertoire backend/")
        print("   Veuillez exécuter: cd backend && python start_fixed_assessment.py")
        return False
    
    print("📋 Étapes de démarrage:")
    print("   1. 🔧 Réparation de la base de données")
    print("   2. 🧪 Test rapide du système")
    print("   3. 🚀 Démarrage du serveur")
    print("   4. 🌐 Test des endpoints")
    
    # Étape 1: Réparation de la base de données
    print("\n" + "=" * 50)
    print("🔧 ÉTAPE 1: RÉPARATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    if not run_command("python fix_database.py", "Réparation de la base de données"):
        print("\n❌ La réparation de la base de données a échoué")
        print("   Le serveur ne peut pas démarrer sans une base de données valide")
        return False
    
    # Étape 2: Test rapide du système
    print("\n" + "=" * 50)
    print("🧪 ÉTAPE 2: TEST RAPIDE DU SYSTÈME")
    print("=" * 50)
    
    if not run_command("python quick_test.py", "Test rapide du système"):
        print("\n⚠️  Le test rapide a échoué")
        print("   Le serveur peut quand même fonctionner, mais il y a des problèmes")
        
        response = input("\nVoulez-vous continuer quand même ? (o/n): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("❌ Démarrage annulé")
            return False
    
    # Étape 3: Démarrage du serveur
    print("\n" + "=" * 50)
    print("🚀 ÉTAPE 3: DÉMARRAGE DU SERVEUR")
    print("=" * 50)
    
    print("📍 Le serveur sera accessible sur:")
    print("   • API: http://localhost:8000")
    print("   • Documentation: http://localhost:8000/docs")
    print("   • Test: http://localhost:8000/test-assessment")
    print("")
    print("📱 Pour tester le frontend:")
    print("   • Page d'évaluation: http://localhost:3001/dashboard/student/assessment")
    print("")
    print("⚠️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("")
    
    # Démarrer le serveur
    try:
        run_command("python start_assessment_system.py", "Démarrage du serveur")
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté par l'utilisateur")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n🎉 DÉMARRAGE TERMINÉ AVEC SUCCÈS !")
            print("✅ Le système d'évaluation est maintenant opérationnel")
            print("✅ La base de données a été réparée")
            print("✅ Le serveur a été lancé")
        else:
            print("\n❌ LE DÉMARRAGE A ÉCHOUÉ")
            print("   Vérifiez les erreurs ci-dessus et relancez le script")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    input("Appuyez sur Entrée pour quitter...")





