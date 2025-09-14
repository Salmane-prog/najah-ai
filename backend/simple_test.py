#!/usr/bin/env python3
"""
Test très simple de la clé API OpenAI.
"""
import os
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def simple_test():
    """Test très simple de la clé API."""
    print("🔑 Test simple de la clé API")
    
    # Vérifier que la clé existe
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Clé API non trouvée")
        return
    
    print(f"✅ Clé trouvée: {api_key[:20]}...")
    
    try:
        # Test minimal
        client = openai.OpenAI(api_key=api_key)
        print("✅ Client créé avec succès")
        
        # Test avec un prompt très court
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        
        print("✅ API fonctionne!")
        print(f"Réponse: {response.choices[0].message.content}")
        
    except openai.AuthenticationError:
        print("❌ Clé API invalide")
    except openai.RateLimitError:
        print("⚠️ Limite de taux - Attendez quelques minutes")
    except openai.QuotaExceededError:
        print("❌ Quota dépassé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    simple_test() 