"""
Session Memory Store
Manages session state, conversation history, and intelligence data
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class SessionState:
    """Represents the state of a conversation session"""
    session_id: str
    scam_detected: bool = False
    total_messages: int = 0
    intelligence: Dict[str, List[str]] = field(default_factory=lambda: {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    })
    conversation_turns: List[Dict] = field(default_factory=list)
    callback_sent: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


class SessionMemoryStore:
    """In-memory store for session data"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}
    
    def get_or_create_session(self, session_id: str) -> SessionState:
        """
        Get existing session or create new one
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            SessionState object
        """
        if session_id not in self.sessions:
            logger.info(f"Creating new session: {session_id}")
            self.sessions[session_id] = SessionState(session_id=session_id)
        
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Get session by ID, returns None if not found"""
        return self.sessions.get(session_id)
    
    def mark_scam_detected(self, session_id: str) -> None:
        """Mark session as scam detected"""
        if session_id in self.sessions:
            self.sessions[session_id].scam_detected = True
            self.sessions[session_id].last_updated = datetime.now()
            logger.info(f"Session {session_id} marked as scam")
    
    def increment_message_count(self, session_id: str) -> int:
        """
        Increment message counter for session
        
        Returns:
            New message count
        """
        if session_id in self.sessions:
            self.sessions[session_id].total_messages += 1
            self.sessions[session_id].last_updated = datetime.now()
            return self.sessions[session_id].total_messages
        return 0
    
    def add_intelligence(self, session_id: str, new_intelligence: Dict[str, List[str]]) -> None:
        """
        Add extracted intelligence to session
        Merges with existing intelligence, removing duplicates
        
        Args:
            session_id: Session identifier
            new_intelligence: Newly extracted intelligence
        """
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        
        # Merge each intelligence type
        for key in ["bankAccounts", "upiIds", "phishingLinks", "phoneNumbers", "suspiciousKeywords"]:
            existing = set(session.intelligence.get(key, []))
            new_items = set(new_intelligence.get(key, []))
            session.intelligence[key] = list(existing.union(new_items))
        
        session.last_updated = datetime.now()
        
        logger.debug(f"Updated intelligence for session {session_id}")
    
    def add_conversation_turn(
        self,
        session_id: str,
        incoming_message,
        reply: str
    ) -> None:
        """
        Store a conversation turn (incoming message + reply)
        
        Args:
            session_id: Session identifier
            incoming_message: The incoming message object (Pydantic model)
            reply: The generated reply
        """
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        
        # Store the turn - access Pydantic model attributes directly
        turn = {
            "incoming": {
                "sender": incoming_message.sender,
                "text": incoming_message.text,
                "timestamp": incoming_message.timestamp
            },
            "reply": reply,
            "timestamp": datetime.now().isoformat()
        }
        
        session.conversation_turns.append(turn)
        session.last_updated = datetime.now()
    
    def mark_callback_sent(self, session_id: str) -> None:
        """Mark that final callback has been sent for this session"""
        if session_id in self.sessions:
            self.sessions[session_id].callback_sent = True
            self.sessions[session_id].last_updated = datetime.now()
            logger.info(f"Callback marked as sent for session {session_id}")
    
    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """
        Get summary of session for callback
        
        Returns:
            Dictionary with session summary or None
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "sessionId": session_id,
            "scamDetected": session.scam_detected,
            "totalMessages": session.total_messages,
            "intelligence": session.intelligence,
            "conversationTurns": len(session.conversation_turns),
            "callbackSent": session.callback_sent
        }
