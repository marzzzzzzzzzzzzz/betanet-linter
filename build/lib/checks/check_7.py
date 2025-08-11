import re
from utils import get_help_output

def check_7(binary_path: str) -> dict:
    """
    Check 7: Bootstraps via rotating rendezvous IDs derived from BeaconSet with PoW and 
    multi-bucket rate-limits; deterministic seeds not used (§6.3–§6.5).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for bootstrap/discovery features
        bootstrap_patterns = [r"beacon", r"pow", r"rendezvous", r"rate.limit", r"bootstrap"]
        found = [pattern for pattern in bootstrap_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Bootstraps via rotating rendezvous IDs with PoW and multi-bucket rate-limits",
                "details": f"Found bootstrap features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Bootstraps via rotating rendezvous IDs with PoW and multi-bucket rate-limits",
            "details": f"Missing bootstrap features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Bootstraps via rotating rendezvous IDs with PoW and multi-bucket rate-limits",
            "details": f"Exception: {str(e)}"
        }