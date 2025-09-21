#!/usr/bin/env python3
"""
Script pour déployer directement sur Railway sans passer par GitHub
"""
import os
import subprocess
import sys

def install_railway_cli():
    """Installe Railway CLI"""
    print("🚀 Installation de Railway CLI...")
    
    # Windows
    if os.name == 'nt':
        try:
            subprocess.run(["winget", "install", "railway"], check=True)
            print("✅ Railway CLI installé via winget")
            return True
        except:
            print("⚠️ Winget non disponible, installation manuelle nécessaire")
            print("📥 Téléchargez Railway CLI depuis: https://railway.app/cli")
            return False
    
    return False

def deploy_to_railway():
    """Déploie le projet sur Railway"""
    
    print("🚀 DÉPLOIEMENT DIRECT SUR RAILWAY")
    print("="*50)
    
    # Vérifier si Railway CLI est installé
    try:
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
        print(f"✅ Railway CLI détecté: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Railway CLI non installé")
        if not install_railway_cli():
            return False
    
    # Se connecter à Railway
    print("\n🔑 Connexion à Railway...")
    subprocess.run(["railway", "login"])
    
    # Créer un nouveau projet
    print("\n📁 Création du projet...")
    subprocess.run(["railway", "init"])
    
    # Déployer le backend
    print("\n🚀 Déploiement du backend...")
    os.chdir("backend")
    subprocess.run(["railway", "up"])
    
    print("\n✅ Déploiement terminé !")
    print("🌐 Votre application sera accessible sur Railway")

if __name__ == "__main__":
    deploy_to_railway()

