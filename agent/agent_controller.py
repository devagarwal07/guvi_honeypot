"""
Agent Controller - Autonomous AI Agent
Manages agent decision-making and reply generation
OPTIMIZED FOR SPEED - Rule-based fast path with LLM fallback
"""
import random
from typing import List, Dict
import logging
from config import settings
from agent.persona import (
    AGENT_SYSTEM_PROMPT,
    build_conversation_prompt,
    build_normal_conversation_prompt,
    get_contextual_reply,
    FIRST_TURN_REPLIES,
    FOLLOWUP_REPLIES,
    EXTRACTION_REPLIES,
    COOPERATIVE_REPLIES,
    TECHNICAL_ISSUE_REPLIES
)

logger = logging.getLogger(__name__)

# Try to import Gemini, but don't fail if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed, using rule-based replies only")


class AgentController:
    """Controls the autonomous AI agent behavior - OPTIMIZED FOR SPEED"""
    
    def __init__(self):
        """Initialize - Gemini is optional, rule-based is primary"""
        self.gemini_available = False
        
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(
                    model_name=settings.LLM_MODEL,
                    generation_config={
                        "temperature": settings.LLM_TEMPERATURE,
                        "max_output_tokens": 50,  # Reduced for speed
                    }
                )
                self.gemini_available = True
            except Exception as e:
                logger.warning(f"Gemini init failed: {e}")
    
    def generate_fast_reply(
        self,
        message_text: str,
        conversation_history: List[Dict],
        session_id: str
    ) -> str:
        """
        FAST rule-based reply - primary path for low latency
        Returns immediately without API calls
        """
        turn_number = len(conversation_history) // 2 + 1
        msg_lower = message_text.lower()
        
        # First message - show initial concern
        if turn_number == 1:
            if any(word in msg_lower for word in ["block", "suspend", "frozen", "deactivat"]):
                return random.choice([
                    "Why is my account being blocked?",
                    "What happened to my account?",
                    "Which bank is this from?"
                ])
            elif any(word in msg_lower for word in ["verify", "kyc", "update"]):
                return random.choice([
                    "What verification is needed?",
                    "Which bank is this?",
                    "Is this really from the bank?"
                ])
            elif any(word in msg_lower for word in ["prize", "winner", "lottery", "won"]):
                return random.choice([
                    "What did I win?",
                    "I don't remember entering any contest",
                    "Which company is this from?"
                ])
            else:
                return random.choice(FIRST_TURN_REPLIES)
        
        # Check for specific content to extract intelligence
        if any(word in msg_lower for word in ["link", "click", "http", "url", "www"]):
            return random.choice([
                "The link is not opening",
                "Can you send the link again?",
                "It shows error when I click",
                "Which link should I open?"
            ])
        
        if any(word in msg_lower for word in ["upi", "@", "gpay", "phonepe", "paytm"]):
            return random.choice([
                "Which UPI ID exactly?",
                "Can you send the UPI ID again?",
                "What amount should I send?",
                "Is there another UPI ID?"
            ])
        
        if any(word in msg_lower for word in ["account", "number", "bank"]):
            return random.choice([
                "Which account number?",
                "Which bank is this for?",
                "I have multiple accounts, which one?",
                "What details do you need?"
            ])
        
        if any(word in msg_lower for word in ["otp", "code", "password", "pin"]):
            return random.choice([
                "Which OTP do you need?",
                "I haven't received any code yet",
                "Should I share the OTP?",
                "Where do I find this code?"
            ])
        
        if any(word in msg_lower for word in ["call", "phone", "contact", "number"]):
            return random.choice([
                "What's the phone number?",
                "Can you call me instead?",
                "Give me the customer care number"
            ])
        
        if any(word in msg_lower for word in ["pay", "send", "transfer", "amount", "fee", "charge"]):
            return random.choice([
                "How much do I need to pay?",
                "Where should I send the money?",
                "What's the account for payment?",
                "Why do I need to pay?"
            ])
        
        # Stage-based responses for later turns
        if turn_number <= 4:
            return random.choice(FOLLOWUP_REPLIES)
        elif turn_number <= 8:
            return random.choice(EXTRACTION_REPLIES)
        elif turn_number <= 12:
            return random.choice(COOPERATIVE_REPLIES)
        else:
            return random.choice(TECHNICAL_ISSUE_REPLIES + COOPERATIVE_REPLIES)
    
    def generate_reply(
        self,
        message_text: str,
        conversation_history: List[Dict],
        session_id: str,
        metadata: Dict
    ) -> str:
        """
        Generate human-like reply using AI agent
        Used when scam is detected
        
        Args:
            message_text: Current message from scammer
            conversation_history: Previous messages
            session_id: Session identifier
            metadata: Channel, language info
            
        Returns:
            Human-like reply text
        """
        # Calculate turn number and intelligence count for context
        turn_number = len(conversation_history) // 2 + 1
        intelligence_count = self._count_intelligence_in_history(conversation_history)
        
        # If Gemini not available, use contextual replies immediately
        if not self.gemini_available:
            logger.warning("Gemini not available, using contextual reply")
            return get_contextual_reply(message_text, turn_number, intelligence_count)
        
        try:
            # Build conversation prompt
            user_prompt = build_conversation_prompt(message_text, conversation_history)
            
            # Combine system prompt and user prompt for Gemini
            full_prompt = f"{AGENT_SYSTEM_PROMPT}\n\n{user_prompt}"
            
            # Call Gemini API with timeout handling
            import asyncio
            from concurrent.futures import TimeoutError
            
            try:
                response = self.model.generate_content(
                    full_prompt,
                    request_options={"timeout": 5}  # 5 second timeout
                )
                reply = response.text.strip()
                logger.info(f"Agent generated reply for session {session_id}: {reply}")
                return reply
            except TimeoutError:
                logger.warning(f"Gemini timeout for session {session_id}, using fallback")
                return get_contextual_reply(message_text, turn_number, intelligence_count)
            
        except Exception as e:
            logger.error(f"Error generating agent reply: {str(e)}")
            # Fallback to contextual reply instead of generic
            return get_contextual_reply(message_text, turn_number, intelligence_count)
    
    def generate_normal_reply(
        self,
        message_text: str,
        conversation_history: List[Dict],
        metadata: Dict
    ) -> str:
        """
        Generate reply for non-scam conversations
        Responds politely without engaging deeply
        """
        # If Gemini not available, return simple response
        if not self.gemini_available:
            return "Thank you for your message."
        
        try:
            user_prompt = build_normal_conversation_prompt(message_text, conversation_history)
            
            # Create a simple model for normal responses
            normal_model = genai.GenerativeModel(
                model_name=settings.LLM_MODEL,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 50,
                }
            )
            
            full_prompt = "You are a polite person responding to messages briefly.\n\n" + user_prompt
            response = normal_model.generate_content(
                full_prompt,
                request_options={"timeout": 3}  # 3 second timeout
            )
            
            reply = response.text.strip()
            return reply
            
        except Exception as e:
            logger.error(f"Error generating normal reply: {str(e)}")
            return "Thank you for your message."
    
    def should_end_engagement(
        self,
        total_messages: int,
        intelligence: Dict,
        conversation_history: List[Dict]
    ) -> bool:
        """
        Decide if engagement should end and callback should be sent
        
        Criteria:
        - Minimum message threshold reached
        - Sufficient intelligence extracted
        - Maximum message limit not exceeded
        
        Args:
            total_messages: Total messages exchanged
            intelligence: Extracted intelligence data
            conversation_history: Full conversation
            
        Returns:
            True if engagement should end
        """
        # Don't end too early
        if total_messages < settings.MIN_MESSAGES_BEFORE_END:
            return False
        
        # Force end if max messages reached
        if total_messages >= settings.MAX_MESSAGES_PER_SESSION:
            logger.info(f"Max messages reached: {total_messages}")
            return True
        
        # Count extracted intelligence items
        intel_count = (
            len(intelligence.get("bankAccounts", [])) +
            len(intelligence.get("upiIds", [])) +
            len(intelligence.get("phishingLinks", [])) +
            len(intelligence.get("phoneNumbers", [])) +
            len(intelligence.get("suspiciousKeywords", []))
        )
        
        # End if we have good intelligence and reasonable conversation length
        if intel_count >= settings.MIN_INTELLIGENCE_ITEMS and total_messages >= 10:
            logger.info(f"Sufficient intelligence gathered: {intel_count} items")
            return True
        
        # Check if conversation is stalling (scammer stopped responding meaningfully)
        if total_messages >= 15 and intel_count >= 1:
            # If last 2 scammer messages are very short, might be stalling
            recent_scammer_msgs = [
                msg for msg in conversation_history[-4:]
                if msg.get("sender") == "scammer"
            ]
            
            if len(recent_scammer_msgs) >= 2:
                avg_length = sum(len(msg.get("text", "")) for msg in recent_scammer_msgs) / len(recent_scammer_msgs)
                if avg_length < 20:  # Very short messages
                    logger.info("Conversation appears to be stalling")
                    return True
        
        return False
    
    def _get_fallback_reply(self, message_text: str) -> str:
        """
        Provide fallback reply if AI generation fails
        Returns contextually appropriate response
        """
        message_lower = message_text.lower()
        
        if any(word in message_lower for word in ["link", "url", "click"]):
            return "The link is not opening. Can you send it again?"
        elif any(word in message_lower for word in ["account", "bank"]):
            return "Which bank is this? I have multiple accounts."
        elif any(word in message_lower for word in ["urgent", "immediate"]):
            return "Why is this so urgent? What happens if I don't do it now?"
        elif any(word in message_lower for word in ["verify", "update", "kyc"]):
            return "How do I verify this is really from the bank?"
        else:
            return "I'm not sure I understand. Can you explain more clearly?"
    
    def _count_intelligence_in_history(self, conversation_history: List[Dict]) -> int:
        """
        Count intelligence items mentioned in conversation history
        
        Args:
            conversation_history: Full conversation
            
        Returns:
            Count of intelligence items found
        """
        count = 0
        full_text = " ".join([msg.get("text", "") for msg in conversation_history])
        full_text_lower = full_text.lower()
        
        # Check for various intelligence indicators
        if "upi" in full_text_lower or "@" in full_text:
            count += 1
        if "http" in full_text_lower or "www" in full_text_lower:
            count += 1
        if any(word in full_text_lower for word in ["account", "bank"]):
            count += 1
        if any(char.isdigit() for char in full_text):
            count += 1
            
        return count
