#!/usr/bin/env python3
"""
Script pour corriger les problèmes de dépendances
"""
import subprocess
import sys
import os

def fix_dependencies():
    """Corrige les problèmes de dépendances"""
    print("🔧 Correction des dépendances...")
    
    # Désinstaller uvicorn corrompu
    print("1. Désinstallation d'uvicorn corrompu...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "uvicorn", "-y"], 
                      capture_output=True, text=True)
        print("✅ Uvicorn désinstallé")
    except Exception as e:
        print(f"⚠️ Erreur: {e}")
    
    # Réinstaller uvicorn
    print("2. Réinstallation d'uvicorn...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"], 
                      capture_output=True, text=True)
        print("✅ Uvicorn réinstallé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Vérifier python-jose
    print("3. Vérification de python-jose...")
    try:
        import jose
        print("✅ Python-jose OK")
    except ImportError:
        print("4. Installation de python-jose...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "python-jose[cryptography]"], 
                          capture_output=True, text=True)
            print("✅ Python-jose installé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    # Vérifier les autres dépendances
    print("5. Vérification des autres dépendances...")
    dependencies = [
        "fastapi",
        "sqlalchemy", 
        "passlib[bcrypt]",
        "python-multipart"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace("[", "_").replace("]", ""))
            print(f"✅ {dep}")
        except ImportError:
            print(f"6. Installation de {dep}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                              capture_output=True, text=True)
                print(f"✅ {dep} installé")
            except Exception as e:
                print(f"❌ Erreur avec {dep}: {e}")
    
    print("\n✅ Toutes les dépendances sont corrigées!")
    return True

def test_imports():
    """Teste tous les imports nécessaires"""
    print("\n🧪 Test des imports...")
    
    try:
        import fastapi
        print("✅ FastAPI")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn")
    except ImportError as e:
        print(f"❌ Uvicorn: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy")
    except ImportError as e:
        print(f"❌ SQLAlchemy: {e}")
        return False
    
    try:
        import passlib
        print("✅ Passlib")
    except ImportError as e:
        print(f"❌ Passlib: {e}")
        return False
    
    try:
        import jose
        print("✅ Python-Jose")
    except ImportError as e:
        print(f"❌ Python-Jose: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Correction des dépendances...")
    print("=" * 50)
    
    # Corriger les dépendances
    if fix_dependencies():
        # Tester les imports
        if test_imports():
            print("\n🎉 Toutes les dépendances sont OK!")
            print("✅ Vous pouvez maintenant démarrer le serveur:")
            print("   python start_simple.py")
        else:
            print("\n❌ Certains imports échouent encore")
    else:
        print("\n❌ Erreur lors de la correction des dépendances") 