"""
Scam Intent Detection Module
Uses keyword matching and context escalation to detect scam attempts
"""
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ScamClassifier:
    """Detects scam intent from messages using rule-based approach"""
    
    def __init__(self):
        # High-confidence scam keywords
        self.scam_keywords = [
            # Banking/Financial urgency
            r'\baccount\s+(will\s+be\s+)?(blocked|suspended|closed|deactivated)',
            r'\bkyc\s+(update|verification|pending|expired)',
            r'\bverify\s+(your\s+)?(account|identity|details)',
            r'\bupdate\s+(your\s+)?(kyc|pan|details)',
            r'\bimmediate(ly)?\s+action',
            r'\burgent(ly)?\s+(required|needed|update)',
            
            # Prize/Lottery scams
            r'\bcongratulations.*won',
            r'\blottery\s+winner',
            r'\bprize\s+(of|worth)',
            r'\bclaim\s+(your\s+)?(prize|reward|amount)',
            
            # Phishing indicators
            r'\bclick\s+(here|link|below)',
            r'\bdownload\s+(app|application)',
            r'\binstall\s+(app|application)',
            r'\benter\s+(your\s+)?(otp|password|pin)',
            r'\bshare\s+(your\s+)?(otp|password|pin)',
            
            # Payment/Transfer requests
            r'\bsend\s+(money|payment|amount)',
            r'\btransfer\s+(money|amount|funds)',
            r'\bpay\s+(immediately|now|urgent)',
            r'\bupi\s+id',
            r'\bbank\s+account\s+number',
            r'\bifsc\s+code',
            
            # Impersonation
            r'\bbank\s+(official|representative|executive)',
            r'\bcustomer\s+(care|support|service)',
            r'\bgovernment\s+(official|department)',
            
            # Threats
            r'\blegal\s+action',
            r'\bpolice\s+(complaint|case)',
            r'\bpenalty\s+(charges|fee)',
        ]
        
        # Context escalation patterns
        self.escalation_patterns = [
            r'\blink\b',
            r'\burl\b',
            r'http[s]?://',
            r'\bwww\.',
            r'\bdownload\b',
            r'\binstall\b',
            r'\botp\b',
            r'\bpassword\b',
            r'\bpin\b',
            r'\baccount\s+number\b',
            r'\bupi\b',
        ]
    
    def detect_scam(
        self,
        message_text: str,
        conversation_history: List[Dict],
        metadata: Dict
    ) -> bool:
        """
        Detect if the message indicates scam intent
        
        Args:
            message_text: Current message text
            conversation_history: Previous messages in conversation
            metadata: Channel, language, locale info
            
        Returns:
            True if scam detected, False otherwise
        """
        message_lower = message_text.lower()
        
        # Count keyword matches
        keyword_matches = 0
        matched_keywords = []
        for pattern in self.scam_keywords:
            if re.search(pattern, message_lower):
                keyword_matches += 1
                matched_keywords.append(pattern)
                logger.debug(f"Scam keyword matched: {pattern}")
        
        # Aggressive detection - even 1 strong keyword
        if keyword_matches >= 1:
            logger.info(f"Scam detected: {keyword_matches} keyword matches - {matched_keywords[:2]}")
            return True
        
        # Context escalation - check conversation history
        if len(conversation_history) >= 1:
            escalation_score = self._calculate_escalation_score(conversation_history)
            
            # Lower threshold - detect faster
            if escalation_score >= 2:
                logger.info(f"Scam detected: escalation score {escalation_score}")
                return True
        
        # Check for URLs/links - immediate detection
        if self._has_suspicious_link(message_lower):
            logger.info("Scam detected: suspicious link found")
            return True
        
        # Check for UPI/payment mentions
        if any(word in message_lower for word in ["upi", "account number", "ifsc", "transfer"]):
            logger.info("Scam detected: payment/account details requested")
            return True
        
        return False
    
    def _calculate_escalation_score(self, conversation_history: List[Dict]) -> int:
        """
        Calculate escalation score based on conversation progression
        Higher score indicates increasing pressure/urgency
        """
        score = 0
        
        for msg in conversation_history:
            if msg.get("sender") == "scammer":
                text = msg.get("text", "").lower()
                
                # Check for escalation patterns
                for pattern in self.escalation_patterns:
                    if re.search(pattern, text):
                        score += 1
        
        return score
    
    def _has_suspicious_link(self, message_text: str) -> bool:
        """Check if message contains URLs or link indicators"""
        link_patterns = [
            r'http[s]?://[^\s]+',
            r'www\.[^\s]+',
            r'\b[a-z0-9-]+\.(com|in|net|org|co\.in)[^\s]*',
        ]
        
        for pattern in link_patterns:
            if re.search(pattern, message_text):
                return True
        
        return False
