"""
Test the deployed Render endpoint
"""
import requests
import json
import time

# Your deployed URL
DEPLOYED_URL = "https://guvi-honeypot-dvsq.onrender.com/api/message"
API_KEY = "9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(
            "https://guvi-honeypot-dvsq.onrender.com/health",
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_message_endpoint():
    """Test the exact payload GUVI sends"""
    print("\n" + "="*60)
    print("Testing Message Endpoint (GUVI Format)")
    print("="*60)
    
    payload = {
        "sessionId": "1fc994e9-f4c5-47ee-8806-90aeb969928f",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately.",
            "timestamp": 1769776085000
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
    
    print(f"\nRequest URL: {DEPLOYED_URL}")
    print(f"Request Body:")
    print(json.dumps(payload, indent=2))
    
    try:
        start_time = time.time()
        response = requests.post(
            DEPLOYED_URL,
            json=payload,
            headers=headers,
            timeout=30  # GUVI uses 30 second timeout
        )
        elapsed = time.time() - start_time
        
        print(f"\n✅ Response received in {elapsed:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        # Validate response format
        data = response.json()
        if "status" in data and "reply" in data:
            print("\n✅ Response format is correct!")
            print(f"✅ Reply: {data['reply']}")
            return True
        else:
            print("\n❌ Response format is incorrect!")
            return False
            
    except requests.Timeout:
        print(f"\n❌ Request timed out after 30 seconds")
        print("This is the same error GUVI is seeing!")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_multiple_turns():
    """Test a multi-turn conversation"""
    print("\n" + "="*60)
    print("Testing Multi-Turn Conversation")
    print("="*60)
    
    session_id = f"test-{int(time.time())}"
    
    messages = [
        "Your bank account will be blocked today. Verify immediately.",
        "Click this link to verify: http://fake-bank.com",
        "Share your UPI ID to avoid suspension."
    ]
    
    conversation_history = []
    
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Turn {i} ---")
        print(f"Scammer: {msg}")
        
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": msg,
                "timestamp": int(time.time() * 1000)
            },
            "conversationHistory": conversation_history,
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
        
        try:
            start_time = time.time()
            response = requests.post(DEPLOYED_URL, json=payload, headers=headers, timeout=30)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "")
                print(f"Agent ({elapsed:.2f}s): {reply}")
                
                # Update conversation history
                conversation_history.append({
                    "sender": "scammer",
                    "text": msg,
                    "timestamp": int(time.time() * 1000)
                })
                conversation_history.append({
                    "sender": "user",
                    "text": reply,
                    "timestamp": int(time.time() * 1000)
                })
            else:
                print(f"❌ Error: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        time.sleep(1)
    
    print("\n✅ Multi-turn conversation completed successfully!")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEPLOYED ENDPOINT TEST")
    print("="*60)
    print(f"URL: {DEPLOYED_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    
    # Run tests
    health_ok = test_health()
    time.sleep(2)
    
    message_ok = test_message_endpoint()
    time.sleep(2)
    
    if message_ok:
        multi_ok = test_multiple_turns()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Message Endpoint: {'✅ PASS' if message_ok else '❌ FAIL'}")
    print("="*60)
    
    if health_ok and message_ok:
        print("\n🎉 All tests passed! Your endpoint is ready for GUVI submission.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above and fix before submitting.")
