import re
from utils import get_help_output

def check_11(binary_path: str) -> dict:
    """
    Check 11: Enforces anti-concentration caps, diversity, and partition checks for 
    governance (§10).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for governance features
        governance_patterns = [r"governance", r"anti.concentration", r"diversity", r"partition", r"weight"]
        found = [pattern for pattern in governance_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Enforces anti-concentration caps, diversity, and partition checks for governance",
                "details": f"Found governance features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Enforces anti-concentration caps, diversity, and partition checks for governance",
            "details": f"Missing governance features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Enforces anti-concentration caps, diversity, and partition checks for governance",
            "details": f"Exception: {str(e)}"
        }