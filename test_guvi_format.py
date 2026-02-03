"""
Test script to verify GUVI format compliance
Tests the exact format specified in the problem statement
"""
import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api/message"
API_KEY = "9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd"
SESSION_ID = f"wertyu-dfghj-ertyui-{int(time.time())}"

def test_first_message():
    """Test the first message format from GUVI spec"""
    print("\n" + "="*60)
    print("TEST 1: First Message (No Conversation History)")
    print("="*60)
    
    payload = {
        "sessionId": SESSION_ID,
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
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("✅ First message test PASSED")
            return response.json()["reply"]
        else:
            print("❌ First message test FAILED")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_second_message(first_reply):
    """Test the second message format with conversation history"""
    print("\n" + "="*60)
    print("TEST 2: Second Message (With Conversation History)")
    print("="*60)
    
    payload = {
        "sessionId": SESSION_ID,
        "message": {
            "sender": "scammer",
            "text": "Share your UPI ID to avoid account suspension.",
            "timestamp": 1770005528731
        },
        "conversationHistory": [
            {
                "sender": "scammer",
                "text": "Your bank account will be blocked today. Verify immediately.",
                "timestamp": 1770005528731
            },
            {
                "sender": "user",
                "text": first_reply,
                "timestamp": 1770005528731
            }
        ],
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
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("✅ Second message test PASSED")
            return True
        else:
            print("❌ Second message test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_without_metadata():
    """Test without metadata (should use defaults)"""
    print("\n" + "="*60)
    print("TEST 3: Message Without Metadata (Optional)")
    print("="*60)
    
    payload = {
        "sessionId": f"test-no-metadata-{int(time.time())}",
        "message": {
            "sender": "scammer",
            "text": "Urgent! Your account needs verification.",
            "timestamp": 1770005528731
        },
        "conversationHistory": []
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("✅ No metadata test PASSED")
            return True
        else:
            print("❌ No metadata test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_response_format():
    """Verify response format matches spec"""
    print("\n" + "="*60)
    print("TEST 4: Response Format Validation")
    print("="*60)
    
    payload = {
        "sessionId": f"test-format-{int(time.time())}",
        "message": {
            "sender": "scammer",
            "text": "Click here to verify: http://fake-bank.com",
            "timestamp": 1770005528731
        },
        "conversationHistory": []
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()
        
        # Check required fields
        has_status = "status" in data
        has_reply = "reply" in data
        status_is_success = data.get("status") == "success"
        reply_is_string = isinstance(data.get("reply"), str)
        
        print(f"\n✓ Has 'status' field: {has_status}")
        print(f"✓ Has 'reply' field: {has_reply}")
        print(f"✓ Status is 'success': {status_is_success}")
        print(f"✓ Reply is string: {reply_is_string}")
        
        if all([has_status, has_reply, status_is_success, reply_is_string]):
            print("\n✅ Response format test PASSED")
            print(f"\nExpected format: {{'status': 'success', 'reply': '...'}}")
            print(f"Actual format: {json.dumps(data, indent=2)}")
            return True
        else:
            print("\n❌ Response format test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("GUVI FORMAT COMPLIANCE TEST")
    print("="*60)
    print(f"\nTesting endpoint: {API_URL}")
    print(f"Using API key: {API_KEY[:20]}...")
    
    time.sleep(2)
    
    # Run tests
    first_reply = test_first_message()
    
    if first_reply:
        time.sleep(1)
        test_second_message(first_reply)
    
    time.sleep(1)
    test_without_metadata()
    
    time.sleep(1)
    test_response_format()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)
