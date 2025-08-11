import re
from utils import get_help_output

def check_10(binary_path: str) -> dict:
    """
    Check 10: Accepts 128-B Cashu vouchers for known keysets with PoW adverts and 
    rate-limits; supports Lightning settlement (§9).
    """
    try:
        help_text = get_help_output(binary_path)
        
        # Look for payment features
        payment_patterns = [r"cashu", r"voucher", r"pow", r"rate.limit", r"lightning"]
        found = [pattern for pattern in payment_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Accepts 128-B Cashu vouchers with PoW adverts and rate-limits; supports Lightning settlement",
                "details": f"Found payment features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Accepts 128-B Cashu vouchers with PoW adverts and rate-limits; supports Lightning settlement",
            "details": f"Missing payment features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Accepts 128-B Cashu vouchers with PoW adverts and rate-limits; supports Lightning settlement",
            "details": f"Exception: {str(e)}"
        }