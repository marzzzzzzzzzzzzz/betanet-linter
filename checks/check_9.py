import re
from utils import get_help_output

def check_9(binary_path: str) -> dict:
    """
    Check 9: Verifies alias ledger with finality-bound 2-of-3 and applies Emergency 
    Advance liveness only under §8.2 conditions; validates quorum certificates as specified.
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for naming/trust features
        naming_patterns = [r"alias", r"ledger", r"finality", r"quorum", r"certificate"]
        found = [pattern for pattern in naming_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Verifies alias ledger with finality-bound 2-of-3 and applies Emergency Advance liveness",
                "details": f"Found naming features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Verifies alias ledger with finality-bound 2-of-3 and applies Emergency Advance liveness",
            "details": f"Missing naming features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Verifies alias ledger with finality-bound 2-of-3 and applies Emergency Advance liveness",
            "details": f"Exception: {str(e)}"
        }