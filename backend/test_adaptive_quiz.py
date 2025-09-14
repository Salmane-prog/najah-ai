import requests

def test_adaptive_quiz():
    try:
        url = "http://localhost:8000/api/v1/adaptive_quizzes/generate-test/5"
        params = {
            "subject": "Français",
            "question_count": 5
        }
        
        print("🧪 Test de l'endpoint de quiz adaptatif...")
        print(f"URL: {url}")
        print(f"Paramètres: {params}")
        
        response = requests.post(url, params=params)
        
        print(f"\n📊 Résultat:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Quiz ID: {data.get('quiz_id', 'N/A')}")
            print(f"Questions: {data.get('total_questions', 0)}")
            print(f"Difficulté: {data.get('difficulty', 'N/A')}")
        else:
            print("❌ Erreur!")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_adaptive_quiz()










