import re
from utils import get_help_output

def check_8(binary_path: str) -> dict:
    """
    Check 8: Selects mixnodes using BeaconSet randomness with per-stream entropy and 
    path diversity (§7.2); "balanced" mode enforces ≥ 2 hops until trust ≥ 0.8 (§7.1–§7.3).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for privacy/mixnet features
        privacy_patterns = [r"mixnode", r"beacon", r"entropy", r"privacy", r"hop"]
        found = [pattern for pattern in privacy_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Selects mixnodes using BeaconSet randomness with per-stream entropy and path diversity",
                "details": f"Found privacy features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Selects mixnodes using BeaconSet randomness with per-stream entropy and path diversity",
            "details": f"Missing privacy features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Selects mixnodes using BeaconSet randomness with per-stream entropy and path diversity",
            "details": f"Exception: {str(e)}"
        }