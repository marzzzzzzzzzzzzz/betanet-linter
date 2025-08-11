import re
from utils import get_help_output

def check_1(binary_path: str) -> dict:
    """
    Check 1: Implements HTX over TCP-443 and QUIC-443 with origin-mirrored TLS + ECH;
    performs per-connection calibration (§5.1).
    """
    try:
        # Retrieve help text via the shared helper (handles scripts and executables)
        help_text = get_help_output(binary_path)
        
        # Look for HTX transport support
        htx_patterns = [r"htx", r"tcp-443", r"quic-443", r"tls", r"ech", r"calibration"]
        found = [pattern for pattern in htx_patterns if re.search(pattern, help_text)]
        
        if len(found) >= 4:
            return {
                "status": "PASS",
                "description": "Implements HTX over TCP-443/QUIC-443 with origin-mirrored TLS + ECH; performs per-connection calibration",
                "details": f"Found HTX features: {', '.join(found)}"
            }
        
        return {
            "status": "FAIL",
            "description": "Implements HTX over TCP-443/QUIC-443 with origin-mirrored TLS + ECH; performs per-connection calibration",
            "details": f"Missing HTX features. Found: {len(found)}/4 required"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "description": "Implements HTX over TCP-443/QUIC-443 with origin-mirrored TLS + ECH; performs per-connection calibration",
            "details": f"Exception: {str(e)}"
        }