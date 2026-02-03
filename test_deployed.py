"""
Test the deployed Render endpoint
"""
import requests
import json

# Your deployed URL
DEPLOYED_URL = "https://guvi-honeypot-dvsq.onrender.com/api/message"
API_KEY = "9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd"

def test_deployed_endpoint():
    """Test the exact format GUVI expects"""
    
    payload = {
        "sessionId": "test-deployed-123",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately.",
            "timestamp": 1770005528731
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print("Testing deployed endpoint...")
    print(f"URL: {DEPLOYED_URL}")
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(DEPLOYED_URL, json=payload, headers=headers, timeout=30)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Deployed endpoint is working!")
            return True
        else:
            print(f"\n❌ Deployed endpoint returned error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out - Render might be cold starting")
        print("Wait 30 seconds and try again")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_deployed_endpoint()
