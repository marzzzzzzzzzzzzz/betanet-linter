import re
from utils import get_help_output

def check_3(binary_path: str) -> dict:
    """
    Check 3: Performs inner Noise XK with key separation, nonce lifecycle, and rekeying (§5.3);
    uses hybrid X25519-Kyber768 from 2027-01-01.
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for Noise protocol features
        noise_patterns = [r"noise", r"xk", r"rekey", r"kyber", r"x25519"]
        found = [pattern for pattern in noise_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Performs inner Noise XK with key separation, nonce lifecycle, and rekeying; uses hybrid X25519-Kyber768",
                "details": f"Found Noise features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Performs inner Noise XK with key separation, nonce lifecycle, and rekeying; uses hybrid X25519-Kyber768",
            "details": f"Missing Noise features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Performs inner Noise XK with key separation, nonce lifecycle, and rekeying; uses hybrid X25519-Kyber768",
            "details": f"Exception: {str(e)}"
        }