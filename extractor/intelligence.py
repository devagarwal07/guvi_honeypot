"""
Intelligence Extraction Engine
Extracts actionable scam intelligence using regex patterns
"""
import re
from typing import Dict, List, Set
import logging

logger = logging.getLogger(__name__)


class IntelligenceExtractor:
    """Extracts scam intelligence from messages"""
    
    def __init__(self):
        # Regex patterns for intelligence extraction
        self.patterns = {
            "bank_accounts": [
                r'\b\d{9,18}\b',  # Bank account numbers (9-18 digits)
                r'\baccount\s*(?:number|no\.?|#)?\s*:?\s*(\d{9,18})\b',
            ],
            "upi_ids": [
                r'\b[\w\.-]+@[\w]+\b',  # UPI format: username@bank
                r'\bupi\s*(?:id)?\s*:?\s*([\w\.-]+@[\w]+)\b',
            ],
            "phone_numbers": [
                r'\b(?:\+91|0)?[6-9]\d{9}\b',  # Indian phone numbers
                r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Formatted phone numbers
            ],
            "urls": [
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),])+',
                r'\b[a-z0-9-]+\.(?:com|in|net|org|co\.in|xyz|info|biz)(?:/[^\s]*)?\b',
            ],
            "ifsc_codes": [
                r'\b[A-Z]{4}0[A-Z0-9]{6}\b',  # IFSC code format
            ],
        }
        
        # Suspicious keywords to track
        self.suspicious_keywords = [
            "kyc", "verify", "update", "blocked", "suspended",
            "urgent", "immediate", "action required", "expire",
            "confirm", "validate", "authenticate", "otp",
            "password", "pin", "cvv", "card number",
            "prize", "won", "lottery", "claim", "reward",
            "refund", "cashback", "offer", "limited time",
            "click here", "download", "install", "link",
            "customer care", "helpline", "support",
            "legal action", "police", "penalty", "fine",
        ]
    
    def extract_from_message(self, message_text: str) -> Dict[str, List[str]]:
        """
        Extract all intelligence from a single message
        
        Args:
            message_text: Message text to analyze
            
        Returns:
            Dictionary with extracted intelligence
        """
        extracted = {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        }
        
        message_lower = message_text.lower()
        
        # Extract bank accounts
        for pattern in self.patterns["bank_accounts"]:
            matches = re.findall(pattern, message_text, re.IGNORECASE)
            for match in matches:
                account = match if isinstance(match, str) else match
                # Filter out timestamps and other non-account numbers
                if len(account) >= 9 and len(account) <= 18:
                    extracted["bankAccounts"].append(account)
        
        # Extract UPI IDs with normalization
        for pattern in self.patterns["upi_ids"]:
            matches = re.findall(pattern, message_text, re.IGNORECASE)
            for match in matches:
                upi = match if isinstance(match, str) else match
                upi = upi.strip().lower()  # Normalize to lowercase
                # Validate UPI format
                if "@" in upi and len(upi) > 5 and upi not in extracted["upiIds"]:
                    extracted["upiIds"].append(upi)
        
        # Extract phone numbers with normalization
        for pattern in self.patterns["phone_numbers"]:
            matches = re.findall(pattern, message_text)
            for match in matches:
                phone = re.sub(r'[-.\s]', '', match)  # Clean formatting
                phone = phone.strip()
                # Normalize to +91 format
                if len(phone) == 10 and phone[0] in '6789':
                    phone = f"+91{phone}"
                elif len(phone) == 11 and phone.startswith('0'):
                    phone = f"+91{phone[1:]}"
                elif not phone.startswith('+') and len(phone) >= 10:
                    phone = f"+91{phone[-10:]}"
                
                if phone not in extracted["phoneNumbers"]:
                    extracted["phoneNumbers"].append(phone)
        
        # Extract URLs with normalization
        for pattern in self.patterns["urls"]:
            matches = re.findall(pattern, message_text, re.IGNORECASE)
            for match in matches:
                url = match.strip().lower()
                # Ensure http:// prefix
                if not url.startswith(('http://', 'https://')):
                    url = f"http://{url}"
                if url not in extracted["phishingLinks"]:
                    extracted["phishingLinks"].append(url)
        
        # Extract suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword in message_lower:
                if keyword not in extracted["suspiciousKeywords"]:
                    extracted["suspiciousKeywords"].append(keyword)
        
        # Remove duplicates
        extracted["bankAccounts"] = list(set(extracted["bankAccounts"]))
        extracted["upiIds"] = list(set(extracted["upiIds"]))
        extracted["phishingLinks"] = list(set(extracted["phishingLinks"]))
        extracted["phoneNumbers"] = list(set(extracted["phoneNumbers"]))
        
        # Log extracted intelligence
        if any(extracted.values()):
            logger.info(f"Extracted intelligence: {extracted}")
        
        return extracted
    
    def merge_intelligence(
        self,
        existing: Dict[str, List[str]],
        new: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Merge new intelligence with existing, removing duplicates
        
        Args:
            existing: Current intelligence data
            new: Newly extracted intelligence
            
        Returns:
            Merged intelligence dictionary
        """
        merged = {
            "bankAccounts": list(set(existing.get("bankAccounts", []) + new.get("bankAccounts", []))),
            "upiIds": list(set(existing.get("upiIds", []) + new.get("upiIds", []))),
            "phishingLinks": list(set(existing.get("phishingLinks", []) + new.get("phishingLinks", []))),
            "phoneNumbers": list(set(existing.get("phoneNumbers", []) + new.get("phoneNumbers", []))),
            "suspiciousKeywords": list(set(existing.get("suspiciousKeywords", []) + new.get("suspiciousKeywords", [])))
        }
        
        return merged
