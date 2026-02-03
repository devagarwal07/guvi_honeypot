"""
Test script for the Honey-Pot API
Simulates a scam conversation to test the system
"""
import requests
import json
import time
from typing import List, Dict

# Configuration
API_URL = "http://localhost:8000/api/message"
API_KEY = "9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd"  # Update with your API key
SESSION_ID = f"test-session-{int(time.time())}"

# Test scam messages (simulating a scammer)
SCAM_MESSAGES = [
    "Dear customer, your bank account will be blocked due to pending KYC verification. Update immediately.",
    "Click this link to verify: http://fake-bank-kyc.com/verify",
    "You need to enter your account number and UPI ID to complete verification.",
    "Please provide your bank account number for verification.",
    "What is your UPI ID? We need it to process your KYC update.",
    "You can also call our customer care at 9876543210 for assistance.",
    "Transfer Rs 1 to this UPI: scammer@paytm to verify your account is active.",
    "If you don't complete this within 24 hours, your account will be permanently blocked.",
]


def send_message(message_text: str, conversation_history: List[Dict]) -> Dict:
    """Send a message to the API and get response"""
    
    payload = {
        "sessionId": SESSION_ID,
        "message": {
            "sender": "scammer",
            "text": message_text,
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
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def run_test_conversation():
    """Run a test conversation simulating a scam"""
    
    print("=" * 60)
    print("HONEY-POT API TEST - Scam Conversation Simulation")
    print("=" * 60)
    print(f"Session ID: {SESSION_ID}\n")
    
    conversation_history = []
    
    for i, scam_msg in enumerate(SCAM_MESSAGES, 1):
        print(f"\n--- Turn {i} ---")
        print(f"Scammer: {scam_msg}")
        
        # Send message and get reply
        result = send_message(scam_msg, conversation_history)
        
        if result:
            reply = result.get("reply", "")
            print(f"Agent: {reply}")
            
            # Update conversation history
            conversation_history.append({
                "sender": "scammer",
                "text": scam_msg,
                "timestamp": int(time.time() * 1000)
            })
            conversation_history.append({
                "sender": "user",
                "text": reply,
                "timestamp": int(time.time() * 1000)
            })
        else:
            print("Failed to get response")
            break
        
        # Wait a bit between messages
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("Test conversation completed!")
    print("Check logs for callback status to evaluation endpoint.")
    print("=" * 60)


if __name__ == "__main__":
    print("\nStarting test in 3 seconds...")
    print("Make sure the server is running on http://localhost:8000")
    print("Update API_KEY in this script if needed.\n")
    time.sleep(3)
    
    run_test_conversation()
