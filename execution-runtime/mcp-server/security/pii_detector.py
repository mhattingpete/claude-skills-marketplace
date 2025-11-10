"""
PII and Secret Detection

Automatically detect and mask sensitive information before it reaches the model context.
"""

import re
from typing import Dict, List, Tuple, Optional


class PIIDetector:
    """
    Detect and mask personally identifiable information and secrets.
    """

    # Patterns for different types of sensitive data
    PATTERNS = {
        'api_key': [
            r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
            r'apikey["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
        ],
        'aws_key': [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
            r'aws[_-]?access[_-]?key[_-]?id["\']?\s*[:=]\s*["\']([A-Z0-9]{20})["\']',
            r'aws[_-]?secret[_-]?access[_-]?key["\']?\s*[:=]\s*["\']([A-Za-z0-9/+=]{40})["\']',
        ],
        'github_token': [
            r'ghp_[a-zA-Z0-9]{36}',  # GitHub Personal Access Token
            r'gho_[a-zA-Z0-9]{36}',  # GitHub OAuth Token
            r'ghu_[a-zA-Z0-9]{36}',  # GitHub User Token
            r'ghs_[a-zA-Z0-9]{36}',  # GitHub Server Token
            r'ghr_[a-zA-Z0-9]{36}',  # GitHub Refresh Token
        ],
        'google_api_key': [
            r'AIza[0-9A-Za-z\-_]{35}',
        ],
        'slack_token': [
            r'xox[pboa]-[0-9]{11,12}-[0-9]{11,12}-[0-9a-zA-Z]{24,32}',
        ],
        'generic_secret': [
            r'secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-/+=]{20,})["\']',
            r'password["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
            r'token["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-/+=]{20,})["\']',
        ],
        'private_key': [
            r'-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----',
            r'-----BEGIN OPENSSH PRIVATE KEY-----',
        ],
        'email': [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        ],
        'phone': [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US phone numbers
            r'\+\d{1,3}[-.]?\d{1,14}\b',  # International
        ],
        'ssn': [
            r'\b\d{3}-\d{2}-\d{4}\b',  # US SSN
        ],
        'credit_card': [
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
        ],
        'ip_address': [
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',  # IPv4
        ],
        'jwt_token': [
            r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
        ],
        'stripe_key': [
            r'sk_live_[0-9a-zA-Z]{24}',
            r'pk_live_[0-9a-zA-Z]{24}',
        ],
        'database_url': [
            r'(?:postgres|mysql|mongodb)://[^:]+:[^@]+@[^/]+/[^\s]+',
        ],
    }

    # Mask formats for different types
    MASK_FORMATS = {
        'api_key': '[REDACTED_API_KEY]',
        'aws_key': '[REDACTED_AWS_KEY]',
        'github_token': '[REDACTED_GITHUB_TOKEN]',
        'google_api_key': '[REDACTED_GOOGLE_API_KEY]',
        'slack_token': '[REDACTED_SLACK_TOKEN]',
        'generic_secret': '[REDACTED_SECRET]',
        'private_key': '[REDACTED_PRIVATE_KEY]',
        'email': '[EMAIL_REDACTED]',
        'phone': '[PHONE_REDACTED]',
        'ssn': '[SSN_REDACTED]',
        'credit_card': '[CARD_REDACTED]',
        'ip_address': '[IP_REDACTED]',
        'jwt_token': '[JWT_REDACTED]',
        'stripe_key': '[REDACTED_STRIPE_KEY]',
        'database_url': '[REDACTED_DATABASE_URL]',
    }

    def __init__(self, enabled_detectors: Optional[List[str]] = None):
        """
        Initialize PII detector.

        Args:
            enabled_detectors: List of detector types to enable (None = all)
        """
        self.enabled_detectors = enabled_detectors or list(self.PATTERNS.keys())

    def detect(self, text: str) -> List[Dict]:
        """
        Detect sensitive information in text.

        Args:
            text: Text to scan

        Returns:
            List of detected items with type, match, and position
        """
        detections = []

        for detector_type in self.enabled_detectors:
            if detector_type not in self.PATTERNS:
                continue

            patterns = self.PATTERNS[detector_type]

            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    detections.append({
                        'type': detector_type,
                        'match': match.group(0),
                        'start': match.start(),
                        'end': match.end(),
                        'line': text[:match.start()].count('\n') + 1
                    })

        return detections

    def mask(self, text: str, detector_types: Optional[List[str]] = None) -> Tuple[str, List[Dict]]:
        """
        Mask sensitive information in text.

        Args:
            text: Text to mask
            detector_types: Specific detector types to use (None = all enabled)

        Returns:
            Tuple of (masked_text, list_of_detections)
        """
        detectors_to_use = detector_types or self.enabled_detectors
        detections = []
        masked_text = text

        # Sort detections by position (reverse) to maintain indices during replacement
        all_detections = self.detect(text)
        all_detections = [d for d in all_detections if d['type'] in detectors_to_use]
        all_detections.sort(key=lambda x: x['start'], reverse=True)

        for detection in all_detections:
            mask_format = self.MASK_FORMATS.get(detection['type'], '[REDACTED]')

            # Replace the match with mask
            masked_text = (
                masked_text[:detection['start']] +
                mask_format +
                masked_text[detection['end']:]
            )

            detections.append(detection)

        return masked_text, detections

    def scan_file(self, file_path: str) -> Dict:
        """
        Scan file for sensitive information.

        Args:
            file_path: Path to file to scan

        Returns:
            Dict with detections and recommendations
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            detections = self.detect(content)

            return {
                'file': file_path,
                'status': 'success',
                'detections': detections,
                'count': len(detections),
                'types': list(set(d['type'] for d in detections))
            }

        except Exception as e:
            return {
                'file': file_path,
                'status': 'error',
                'error': str(e)
            }

    def mask_result(self, result: any, aggressive: bool = False) -> any:
        """
        Mask sensitive information in execution results before returning to model.

        Args:
            result: Result to mask (string, dict, list, etc.)
            aggressive: Use aggressive masking (emails, IPs, etc.)

        Returns:
            Masked result
        """
        if isinstance(result, str):
            # Choose detectors based on aggressiveness
            if aggressive:
                detectors = self.enabled_detectors
            else:
                # Only mask secrets/credentials, not general PII
                detectors = [
                    'api_key', 'aws_key', 'github_token', 'google_api_key',
                    'slack_token', 'generic_secret', 'private_key', 'jwt_token',
                    'stripe_key', 'database_url'
                ]

            masked_text, _ = self.mask(result, detectors)
            return masked_text

        elif isinstance(result, dict):
            return {k: self.mask_result(v, aggressive) for k, v in result.items()}

        elif isinstance(result, list):
            return [self.mask_result(item, aggressive) for item in result]

        else:
            return result


# Global detector instance
_default_detector = PIIDetector()


def mask_secrets(text: str) -> str:
    """
    Quick function to mask secrets in text.

    Args:
        text: Text to mask

    Returns:
        Masked text
    """
    masked, _ = _default_detector.mask(text, detector_types=[
        'api_key', 'aws_key', 'github_token', 'google_api_key',
        'slack_token', 'generic_secret', 'private_key', 'jwt_token',
        'stripe_key', 'database_url'
    ])
    return masked


def detect_secrets(text: str) -> List[Dict]:
    """
    Quick function to detect secrets in text.

    Args:
        text: Text to scan

    Returns:
        List of detections
    """
    return _default_detector.detect(text)
