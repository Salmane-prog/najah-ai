import requests
import json

def test_notes_endpoint():
    """Test the notes endpoint with frontend data format"""
    url = "http://localhost:8000/notes-advanced/"
    
    # Data exactly as frontend sends it
    data = {
        "title": "Test Note",
        "content": "Test content",
        "subject": "Mathématiques", 
        "chapter": "Test chapter",
        "tags": "[\"test\", \"frontend\"]",
        "color": "bg-blue-100"
    }
    
    print(f"Testing POST to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Success!")
        else:
            print("❌ Failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_notes_endpoint() 