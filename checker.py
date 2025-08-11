import subprocess
import json
import os
import re
from typing import List, Dict, Any

# Import all check modules
# Import the individual check functions from the local checks package.  We use
# relative imports here instead of ``betanet_linter.checks`` because the
# project directory contains a space in its name ("betanet LINTER"), which
# prevents Python from resolving it as a dotted package name.  The ``checks``
# package lives directly under the same directory as this module.
from checks.check_1 import check_1
from checks.check_2 import check_2
from checks.check_3 import check_3
from checks.check_4 import check_4
from checks.check_5 import check_5
from checks.check_6 import check_6
from checks.check_7 import check_7
from checks.check_8 import check_8
from checks.check_9 import check_9
from checks.check_10 import check_10
from checks.check_11 import check_11

def run_all_checks(binary_path: str, verbose: bool = False) -> List[Dict[str, Any]]:
    """
    Run all 11 required checks against the binary.
    Returns a list of check results.
    """
    checks = [
        check_1, check_2, check_3, check_4, check_5,
        check_6, check_7, check_8, check_9, check_10, check_11
    ]
    
    results = []
    
    for i, check_func in enumerate(checks, 1):
        try:
            result = check_func(binary_path)
            results.append({
                "id": i,
                "description": result.get("description", f"Check {i}"),
                "status": result["status"],
                "details": result.get("details", "")
            })
        except Exception as e:
            results.append({
                "id": i,
                "description": f"Check {i}",
                "status": "ERROR",
                "details": f"Check failed with exception: {str(e)}"
            })
    
    return results