#!/usr/bin/env python3
"""
Script pour redémarrer le backend et corriger les problèmes de tokens expirés
"""

import subprocess
import sys
import time
import os
import signal
import psutil

def kill_backend_processes():
    """Tuer tous les processus backend en cours"""
    print("🔄 Arrêt des processus backend...")
    
    # Chercher les processus Python qui exécutent le backend
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                cmdline = ' '.join(proc.info['cmdline'])
                if 'uvicorn' in cmdline or 'main.py' in cmdline or 'backend' in cmdline:
                    print(f"   Arrêt du processus {proc.info['pid']}: {cmdline}")
                    proc.terminate()
                    time.sleep(1)
                    if proc.is_running():
                        proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def start_backend():
    """Démarrer le backend"""
    print("🚀 Démarrage du backend...")
    
    # Changer vers le répertoire backend
    os.chdir('backend')
    
    # Démarrer le backend
    try:
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 'main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Backend démarré avec succès")
        print("📡 URL: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        
        return process
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du backend: {e}")
        return None

def check_backend_health():
    """Vérifier que le backend répond"""
    import requests
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ Backend opérationnel")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Tentative {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ Le backend ne répond pas après 60 secondes")
    return False

def main():
    print("🔧 Script de redémarrage du backend avec correction des tokens")
    print("=" * 60)
    
    # 1. Arrêter les processus existants
    kill_backend_processes()
    time.sleep(3)
    
    # 2. Démarrer le backend
    process = start_backend()
    if not process:
        print("❌ Impossible de démarrer le backend")
        sys.exit(1)
    
    # 3. Vérifier que le backend fonctionne
    if check_backend_health():
        print("\n🎉 Backend redémarré avec succès!")
        print("💡 Les nouveaux tokens générés ne devraient plus expirer immédiatement")
        print("\n📋 Prochaines étapes:")
        print("   1. Rafraîchir la page du navigateur")
        print("   2. Se reconnecter si nécessaire")
        print("   3. Vérifier que les erreurs 401 ont disparu")
        
        # Garder le processus en vie
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du backend...")
            process.terminate()
    else:
        print("❌ Échec du démarrage du backend")
        sys.exit(1)

if __name__ == "__main__":
    main()





