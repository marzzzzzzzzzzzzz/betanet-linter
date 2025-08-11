import re
from utils import get_help_output

def check_2(binary_path: str) -> dict:
    """
    Check 2: Uses negotiated-carrier, replay-bound access tickets (§5.2) with 
    variable lengths and rate-limits.
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for access ticket features
        ticket_patterns = [r"ticket", r"carrier", r"replay", r"rate.limit", r"padding"]
        found = [pattern for pattern in ticket_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 3:
            return {
                "status": "PASS",
                "description": "Uses negotiated-carrier, replay-bound access tickets with variable lengths and rate-limits",
                "details": f"Found ticket features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Uses negotiated-carrier, replay-bound access tickets with variable lengths and rate-limits",
            "details": f"Missing ticket features. Found: {len(found)}/3 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Uses negotiated-carrier, replay-bound access tickets with variable lengths and rate-limits",
            "details": f"Exception: {str(e)}"
        }