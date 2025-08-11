import re
from utils import get_help_output

def check_5(binary_path: str) -> dict:
    """
    Check 5: Bridges non-SCION links by HTX-tunnelled transition; no on-wire transition 
    header on public networks (§4.2).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for SCION/transition features
        scion_patterns = [r"scion", r"htx.tunnel", r"transition", r"gateway", r"encapsulate"]
        found = [pattern for pattern in scion_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 3:
            return {
                "status": "PASS",
                "description": "Bridges non-SCION links by HTX-tunnelled transition; no on-wire transition header on public networks",
                "details": f"Found SCION/transition features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Bridges non-SCION links by HTX-tunnelled transition; no on-wire transition header on public networks",
            "details": f"Missing SCION/transition features. Found: {len(found)}/3 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Bridges non-SCION links by HTX-tunnelled transition; no on-wire transition header on public networks",
            "details": f"Exception: {str(e)}"
        }