"""
Validation utilities
Input validation and sanitization helpers
"""
import re
from typing import Optional


def is_valid_session_id(session_id: str) -> bool:
    """
    Validate session ID format
    Should be alphanumeric with hyphens/underscores
    """
    if not session_id or len(session_id) > 100:
        return False
    
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, session_id))


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """
    Sanitize text input
    Remove potentially harmful characters and limit length
    """
    if not text:
        return ""
    
    # Limit length
    text = text[:max_length]
    
    # Remove null bytes and other control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text.strip()


def is_valid_timestamp(timestamp: int) -> bool:
    """
    Validate timestamp is reasonable
    Should be in milliseconds since epoch
    """
    # Check if timestamp is within reasonable range
    # Between year 2020 and 2030
    min_timestamp = 1577836800000  # 2020-01-01
    max_timestamp = 1893456000000  # 2030-01-01
    
    return min_timestamp <= timestamp <= max_timestamp


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL
    Returns None if invalid
    """
    try:
        pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    except Exception:
        pass
    
    return None
