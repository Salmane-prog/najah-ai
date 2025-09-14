#!/usr/bin/env python3
"""
Script pour générer un token de test valide
"""

import jwt
from datetime import datetime, timedelta
from core.config import settings

def generate_test_token():
    """Génère un token de test valide pour un enseignant"""
    
    # Données du token
    payload = {
        "sub": "teacher@example.com",  # Email de l'utilisateur
        "role": "teacher",             # Rôle de l'utilisateur
        "exp": datetime.utcnow() + timedelta(days=30),  # Expiration dans 30 jours
        "iat": datetime.utcnow(),      # Date de création
    }
    
    try:
        # Générer le token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        print("🔑 TOKEN DE TEST GÉNÉRÉ AVEC SUCCÈS !")
        print("=" * 60)
        print(f"Token: {token}")
        print("=" * 60)
        print("\n📋 INFORMATIONS DU TOKEN :")
        print(f"Email: {payload['sub']}")
        print(f"Rôle: {payload['role']}")
        print(f"Expiration: {payload['exp']}")
        print(f"Algorithme: {settings.ALGORITHM}")
        
        print("\n🔧 POUR TESTER LE FRONTEND :")
        print("1. Ouvre la console du navigateur (F12)")
        print("2. Exécute cette commande :")
        print(f"   localStorage.setItem('najah_token', '{token}')")
        print("3. Rafraîchis la page")
        print("4. Essaie de créer une évaluation formative")
        
        return token
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du token: {e}")
        return None

def verify_token(token):
    """Vérifie que le token généré est valide"""
    
    try:
        # Décoder le token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        print("\n✅ VÉRIFICATION DU TOKEN :")
        print(f"Token valide: OUI")
        print(f"Email: {payload.get('sub')}")
        print(f"Rôle: {payload.get('role')}")
        print(f"Expiration: {payload.get('exp')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du token: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Générateur de token de test pour l'API formative evaluations")
    print("=" * 70)
    
    # Générer le token
    token = generate_test_token()
    
    if token:
        # Vérifier le token
        verify_token(token)
        
        print("\n🎯 TOKEN PRÊT À UTILISER !")
        print("Copie le token ci-dessus et utilise-le dans le frontend.")
    else:
        print("\n❌ ÉCHEC DE LA GÉNÉRATION DU TOKEN")
