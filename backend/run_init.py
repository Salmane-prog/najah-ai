#!/usr/bin/env python3
"""
Script d'initialisation des données de test pour NajahAI
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from init_test_data import init_test_data

def main():
    print("🚀 Initialisation des données de test pour NajahAI")
    print("=" * 50)
    
    try:
        init_test_data()
        print("\n✅ Initialisation terminée avec succès !")
        print("\n📋 Prochaines étapes :")
        print("1. Redémarrez le serveur backend")
        print("2. Redémarrez le serveur frontend")
        print("3. Testez l'application")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 