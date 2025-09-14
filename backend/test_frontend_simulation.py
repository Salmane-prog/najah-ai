import requests
import json

def test_frontend_simulation():
    """Simulate the exact frontend request"""
    url = "http://localhost:8000/notes-advanced/"
    
    # Headers that a browser would send
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3001',
        'Referer': 'http://localhost:3001/dashboard/student/notes-advanced',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Data exactly as frontend sends it
    data = {
        "title": "Test Frontend Note",
        "content": "This is a test note from frontend simulation",
        "subject": "Mathématiques",
        "chapter": "Test chapter",
        "tags": "[\"test\", \"frontend\", \"simulation\"]",
        "color": "bg-blue-100"
    }
    
    print(f"Simulating frontend request to: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        # First test OPTIONS (preflight)
        print("\n1. Testing OPTIONS (preflight):")
        options_response = requests.options(url, headers=headers)
        print(f"OPTIONS Status: {options_response.status_code}")
        print(f"OPTIONS Headers: {dict(options_response.headers)}")
        
        # Then test POST
        print("\n2. Testing POST:")
        post_response = requests.post(url, json=data, headers=headers)
        print(f"POST Status: {post_response.status_code}")
        print(f"POST Response: {post_response.text}")
        
        if post_response.status_code == 200:
            print("✅ Frontend simulation successful!")
        else:
            print("❌ Frontend simulation failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_frontend_simulation() 