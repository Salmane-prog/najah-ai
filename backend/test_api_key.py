#!/usr/bin/env python3
"""
Script simple pour tester la clé API OpenAI.
"""
import os
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_api_key():
    """Test simple de la clé API OpenAI."""
    print("🔑 Test de la clé API OpenAI")
    print("=" * 40)
    
    # Récupérer la clé API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Erreur: OPENAI_API_KEY non trouvée dans .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    
    try:
        # Initialiser le client OpenAI
        client = openai.OpenAI(api_key=api_key)
        print("✅ Client OpenAI initialisé")
        
        # Test simple avec GPT-3.5-turbo
        print("🧪 Test de génération...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Dis-moi simplement 'Bonjour!' en français"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        # Afficher la réponse
        message = response.choices[0].message.content
        print(f"✅ Réponse reçue: {message}")
        
        # Afficher les détails de la requête
        print(f"📊 Tokens utilisés: {response.usage.total_tokens}")
        print(f"💰 Coût estimé: ~${response.usage.total_tokens * 0.000002:.6f}")
        
        return True
        
    except openai.AuthenticationError:
        print("❌ Erreur d'authentification: Clé API invalide")
        return False
    except openai.RateLimitError:
        print("❌ Limite de taux dépassée: Trop de requêtes")
        return False
    except openai.QuotaExceededError:
        print("❌ Quota dépassé: Crédits insuffisants")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def test_different_models():
    """Test avec différents modèles."""
    print("\n🤖 Test avec différents modèles")
    print("=" * 40)
    
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)
    
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-turbo-preview"
    ]
    
    for model in models_to_test:
        try:
            print(f"🧪 Test du modèle: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Test"}
                ],
                max_tokens=10
            )
            print(f"✅ {model} - OK")
        except Exception as e:
            print(f"❌ {model} - Erreur: {str(e)}")

if __name__ == "__main__":
    success = test_api_key()
    
    if success:
        print("\n🎉 Votre clé API fonctionne parfaitement!")
        print("Vous pouvez maintenant utiliser OpenAI dans votre application.")
        
        # Test optionnel avec d'autres modèles
        response = input("\nVoulez-vous tester d'autres modèles? (y/n): ")
        if response.lower() == 'y':
            test_different_models()
    else:
        print("\n❌ Problème avec la clé API.")
        print("Vérifiez:")
        print("1. La clé API dans le fichier .env")
        print("2. Votre quota OpenAI")
        print("3. Votre connexion internet") 