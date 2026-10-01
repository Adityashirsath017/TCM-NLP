import re
import html
from fastapi import HTTPException, status

# Blacklist of malicious script / injection patterns
DANGEROUS_PATTERNS = [
    re.compile(r'<\s*script[^>]*>', re.IGNORECASE),
    re.compile(r'javascript\s*:', re.IGNORECASE),
    re.compile(r'on\w+\s*=', re.IGNORECASE), # e.g. onerror=, onclick=
    re.compile(r'<\s*iframe[^>]*>', re.IGNORECASE),
    re.compile(r'<\s*embed[^>]*>', re.IGNORECASE),
    re.compile(r'<\s*object[^>]*>', re.IGNORECASE),
    re.compile(r'data\s*:\s*text\/html', re.IGNORECASE),
    re.compile(r'\$\{.*?\}'), # template injection
    re.compile(r'\{\{.*?\}\}'), # SSTI template injection
    re.compile(r'__proto__', re.IGNORECASE), # prototype pollution
    re.compile(r'constructor', re.IGNORECASE)
]

def sanitize_comment(raw_text: str) -> str:
    """
    Strictly sanitize user comments against malicious code, XSS,
    template injection, and database tampering attempts.
    """
    if not isinstance(raw_text, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid comment format."
        )

    # 1. Remove null bytes and non-printable control characters (except common whitespace)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', raw_text)
    cleaned = cleaned.strip()

    # 2. Length validation
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a comment."
        )

    if len(cleaned) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment is too long. Maximum 500 characters."
        )

    # 3. Check for obvious script / malicious injection payloads
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(cleaned):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Malicious input or script tags detected. Please enter safe text only."
            )

    # 4. Escape HTML to prevent any injection in downstream consumers
    safe_text = html.escape(cleaned, quote=True)

    # Re-normalize whitespace
    safe_text = re.sub(r'[ \t]+', ' ', safe_text)

    return safe_text

def sanitize_id(val: any) -> int:
    """Ensure ID is strictly a positive integer to prevent NoSQL/key injection."""
    try:
        val_int = int(val)
        if val_int <= 0:
            raise ValueError()
        return val_int
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid post ID format."
        )
