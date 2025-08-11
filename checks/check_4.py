import re
from utils import get_help_output

def check_4(binary_path: str) -> dict:
    """
    Check 4: Emulates HTTP/2/3 with adaptive cadences and origin-mirrored parameters (§5.5).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for HTTP/2/3 emulation features
        http_patterns = [r"http.2", r"http.3", r"adaptive", r"ping", r"settings"]
        found = [pattern for pattern in http_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 3:
            return {
                "status": "PASS",
                "description": "Emulates HTTP/2/3 with adaptive cadences and origin-mirrored parameters",
                "details": f"Found HTTP features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Emulates HTTP/2/3 with adaptive cadences and origin-mirrored parameters",
            "details": f"Missing HTTP features. Found: {len(found)}/3 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Emulates HTTP/2/3 with adaptive cadences and origin-mirrored parameters",
            "details": f"Exception: {str(e)}"
        }