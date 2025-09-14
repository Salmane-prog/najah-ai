#!/usr/bin/env python3
"""
SCRIPT DE DEMARRAGE SIMPLE - VERSION WINDOWS
Lance le serveur d'evaluation apres avoir repare la base de donnees
"""

import sys
import os
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executer une commande et afficher le resultat"""
    print(f"\n{description}...")
    print(f"   Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"OK: {description} reussi")
            if result.stdout.strip():
                print(f"   Sortie: {result.stdout.strip()}")
        else:
            print(f"ERREUR: {description} echoue")
            if result.stderr.strip():
                print(f"   Erreur: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"ERREUR lors de {description.lower()}: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    
    print("SYSTEME D'EVALUATION INITIALE - DEMARRAGE AVEC REPARATION")
    print("=" * 70)
    
    # Verifier que nous sommes dans le bon repertoire
    if not Path("fix_database_windows.py").exists():
        print("ERREUR: Ce script doit etre execute depuis le repertoire backend/")
        print("   Veuillez executer: cd backend && python start_windows.py")
        return False
    
    print("Etapes de demarrage:")
    print("   1. Reparation de la base de donnees")
    print("   2. Test rapide du systeme")
    print("   3. Demarrage du serveur")
    print("   4. Test des endpoints")
    
    # Etape 1: Reparation de la base de donnees
    print("\n" + "=" * 50)
    print("ETAPE 1: REPARATION DE LA BASE DE DONNEES")
    print("=" * 50)
    
    if not run_command("python fix_database_windows.py", "Reparation de la base de donnees"):
        print("\nLa reparation de la base de donnees a echoue")
        print("   Le serveur ne peut pas demarrer sans une base de donnees valide")
        return False
    
    # Etape 2: Test rapide du systeme
    print("\n" + "=" * 50)
    print("ETAPE 2: TEST RAPIDE DU SYSTEME")
    print("=" * 50)
    
    if not run_command("python quick_test.py", "Test rapide du systeme"):
        print("\nLe test rapide a echoue")
        print("   Le serveur peut quand meme fonctionner, mais il y a des problemes")
        
        response = input("\nVoulez-vous continuer quand meme ? (o/n): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("Demarrage annule")
            return False
    
    # Etape 3: Demarrage du serveur
    print("\n" + "=" * 50)
    print("ETAPE 3: DEMARRAGE DU SERVEUR")
    print("=" * 50)
    
    print("Le serveur sera accessible sur:")
    print("   • API: http://localhost:8000")
    print("   • Documentation: http://localhost:8000/docs")
    print("   • Test: http://localhost:8000/test-assessment")
    print("")
    print("Pour tester le frontend:")
    print("   • Page d'evaluation: http://localhost:3001/dashboard/student/assessment")
    print("")
    print("Appuyez sur Ctrl+C pour arreter le serveur")
    print("")
    
    # Demarrer le serveur
    try:
        run_command("python start_assessment_system.py", "Demarrage du serveur")
    except KeyboardInterrupt:
        print("\nServeur arrete par l'utilisateur")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\nDEMARRAGE TERMINE AVEC SUCCES !")
            print("Le systeme d'evaluation est maintenant operationnel")
            print("La base de donnees a ete reparee")
            print("Le serveur a ete lance")
        else:
            print("\nLE DEMARRAGE A ECHOUE")
            print("   Verifiez les erreurs ci-dessus et relancez le script")
        
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    input("Appuyez sur Entree pour quitter...")





