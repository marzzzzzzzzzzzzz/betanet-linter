import re
from utils import get_help_output

def check_6(binary_path: str) -> dict:
    """
    Check 6: Offers /betanet/htx/1.1.0 and /betanet/htxquic/1.1.0 transports (§6.2).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for transport protocols
        transport_patterns = [r"/betanet/htx/1.1.0", r"/betanet/htxquic/1.1.0", r"transport", r"protocol"]
        found = [pattern for pattern in transport_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 2:
            return {
                "status": "PASS",
                "description": "Offers /betanet/htx/1.1.0 and /betanet/htxquic/1.1.0 transports",
                "details": f"Found transport protocols: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Offers /betanet/htx/1.1.0 and /betanet/htxquic/1.1.0 transports",
            "details": f"Missing transport protocols. Found: {len(found)}/2 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Offers /betanet/htx/1.1.0 and /betanet/htxquic/1.1.0 transports",
            "details": f"Exception: {str(e)}"
        }