"""
GUVI Callback Client
Sends final results to the evaluation endpoint
"""
import httpx
from typing import Dict, List
import logging
from config import settings

logger = logging.getLogger(__name__)


class GuviCallbackClient:
    """Client for sending final results to GUVI evaluation endpoint"""
    
    def __init__(self):
        self.callback_url = settings.GUVI_CALLBACK_URL
        self.timeout = 10.0  # 10 second timeout
    
    async def send_final_result(
        self,
        session_id: str,
        scam_detected: bool,
        total_messages: int,
        intelligence: Dict[str, List[str]],
        conversation_history: List[Dict]
    ) -> bool:
        """
        Send final result to GUVI evaluation endpoint
        
        Args:
            session_id: Session identifier
            scam_detected: Whether scam was detected
            total_messages: Total messages exchanged
            intelligence: Extracted intelligence data
            conversation_history: Full conversation history
            
        Returns:
            True if callback successful, False otherwise
        """
        # Build agent notes summary
        agent_notes = self._build_agent_notes(
            conversation_history,
            intelligence,
            total_messages
        )
        
        # Build payload according to spec
        payload = {
            "sessionId": session_id,
            "scamDetected": scam_detected,
            "totalMessagesExchanged": total_messages,
            "extractedIntelligence": {
                "bankAccounts": intelligence.get("bankAccounts", []),
                "upiIds": intelligence.get("upiIds", []),
                "phishingLinks": intelligence.get("phishingLinks", []),
                "phoneNumbers": intelligence.get("phoneNumbers", []),
                "suspiciousKeywords": intelligence.get("suspiciousKeywords", [])
            },
            "agentNotes": agent_notes
        }
        
        try:
            logger.info(f"Sending callback for session {session_id} to {self.callback_url}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.callback_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Callback successful for session {session_id}")
                    return True
                else:
                    logger.error(
                        f"Callback failed for session {session_id}: "
                        f"Status {response.status_code}, Response: {response.text}"
                    )
                    return False
                    
        except httpx.TimeoutException:
            logger.error(f"Callback timeout for session {session_id}")
            return False
        except Exception as e:
            logger.error(f"Callback error for session {session_id}: {str(e)}")
            return False
    
    def _build_agent_notes(
        self,
        conversation_history: List[Dict],
        intelligence: Dict[str, List[str]],
        total_messages: int
    ) -> str:
        """
        Build summary notes about the scammer behavior
        
        Args:
            conversation_history: Full conversation
            intelligence: Extracted intelligence
            total_messages: Message count
            
        Returns:
            Summary string
        """
        notes_parts = []
        
        # Scam type detection
        keywords = intelligence.get("suspiciousKeywords", [])
        if any(k in keywords for k in ["kyc", "verify", "blocked", "suspended"]):
            notes_parts.append("Banking/KYC scam attempt.")
        if any(k in keywords for k in ["prize", "won", "lottery"]):
            notes_parts.append("Prize/lottery scam.")
        if any(k in keywords for k in ["otp", "password", "pin"]):
            notes_parts.append("Credential phishing attempt.")
        
        # Intelligence summary
        intel_summary = []
        if intelligence.get("bankAccounts"):
            intel_summary.append(f"{len(intelligence['bankAccounts'])} bank account(s)")
        if intelligence.get("upiIds"):
            intel_summary.append(f"{len(intelligence['upiIds'])} UPI ID(s)")
        if intelligence.get("phishingLinks"):
            intel_summary.append(f"{len(intelligence['phishingLinks'])} phishing link(s)")
        if intelligence.get("phoneNumbers"):
            intel_summary.append(f"{len(intelligence['phoneNumbers'])} phone number(s)")
        
        if intel_summary:
            notes_parts.append(f"Extracted: {', '.join(intel_summary)}.")
        
        # Engagement summary
        notes_parts.append(f"Engaged over {total_messages} messages.")
        
        # Scammer behavior
        scammer_messages = [
            msg for msg in conversation_history
            if msg.get("sender") == "scammer"
        ]
        
        if scammer_messages:
            avg_length = sum(len(msg.get("text", "")) for msg in scammer_messages) / len(scammer_messages)
            if avg_length > 100:
                notes_parts.append("Scammer provided detailed instructions.")
            
            # Check for urgency
            urgency_words = ["urgent", "immediate", "now", "quickly", "asap"]
            urgency_count = sum(
                1 for msg in scammer_messages
                if any(word in msg.get("text", "").lower() for word in urgency_words)
            )
            if urgency_count >= 2:
                notes_parts.append("High urgency tactics used.")
        
        return " ".join(notes_parts)
