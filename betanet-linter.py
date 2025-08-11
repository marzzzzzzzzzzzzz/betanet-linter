#!/usr/bin/env python3
"""
Betanet Spec-Compliance Linter CLI
Checks a candidate binary against all 11 required features and generates an SBOM.
"""

import sys
import os
import argparse
import json

# Import the canonical checker and SBOM generator from the package.  This avoids
# duplicating the check logic in this top‑level script.  See
# betanet_linter/checker.py and betanet_linter/sbom.py for details.
# Import the checker, SBOM generator and utils from the local directory.
# We avoid using a dotted package name here because the project folder has a
# space in its name ("betanet LINTER"), which prevents a conventional
# ``betanet_linter`` package import.  Relative imports work correctly when
# running this script directly and when installed via setup.py.
from checker import run_all_checks
from sbom import generate_sbom
from utils import is_executable

def get_binary_help_text(_binary_path: str) -> str:  # pragma: no cover
    """
    Deprecated helper retained for backward compatibility.  The new
    implementation delegates to betanet_linter.checker.run_all_checks,
    which internally invokes the candidate binary and interprets its
    ``--help`` output.

    This function now simply returns an empty string to avoid
    accidental use.  Please use run_all_checks() instead.
    """
    return ""

def run_check(_binary_path: str, check_num: int, _help_text: str) -> dict:  # pragma: no cover
    """
    Deprecated.  Use ``betanet_linter.checker.run_all_checks`` instead of calling
    this helper directly.  This stub is retained to preserve backward
    compatibility for third‑party scripts that may have imported it from
    earlier versions.
    """
    return {
        "status": "FAIL",
        "description": f"Check {check_num}",
        "details": "This legacy function is deprecated; use run_all_checks().",
    }

def _generate_sbom_deprecated(_binary_path: str):  # pragma: no cover
    """
    Deprecated.  Please import and use :func:`sbom.generate_sbom` instead of
    relying on this stub.  It remains only to preserve backwards
    compatibility for scripts that may have imported ``generate_sbom`` from
    earlier versions of this file.
    """
    raise NotImplementedError(
        "This function is deprecated.  Please import generate_sbom from sbom"
    )

def main():
    parser = argparse.ArgumentParser(
        description="Betanet Spec-Compliance Linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python betanet-linter.py --binary C:\\path\\to\\binary.exe
  python betanet-linter.py --binary C:\\path\\to\\binary.exe --output report.json
  python betanet-linter.py --binary C:\\path\\to\\binary.exe --sbom --sbom-output sbom.json
        """
    )
    
    parser.add_argument("--binary", "-b", required=True, help="Path to the candidate binary to check")
    parser.add_argument("--output", "-o", help="Output file for the compliance report (JSON format)")
    parser.add_argument("--sbom", action="store_true", help="Generate Software Bill of Materials (SBOM)")
    parser.add_argument("--sbom-output", default="sbom.json", help="Output file for the SBOM (default: sbom.json)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Validate binary path
    if not os.path.exists(args.binary):
        print(f"Error: Binary file '{args.binary}' not found")
        sys.exit(1)

    # Warn if the candidate binary may not be executable.  We still proceed
    # because run_all_checks will attempt to invoke scripts via the
    # interpreter when appropriate.
    if not (args.binary.lower().endswith(".exe") or is_executable(args.binary)):
        print(f"Warning: Binary file '{args.binary}' may not be executable")

    try:
        # Delegate to the checker to run all 11 checks.
        results = run_all_checks(args.binary, args.verbose)
        passed = sum(1 for r in results if r["status"] == "PASS")
        total = len(results)

        if args.format == "json":
            output_data = {
                "binary": args.binary,
                "passed": passed,
                "total": total,
                "compliant": passed == total,
                "checks": results,
            }
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(output_data, f, indent=2)
                print(f"Report saved to {args.output}")
            else:
                print(json.dumps(output_data, indent=2))
        else:
            # Human‑readable format
            print(f"Betanet Compliance Report for: {args.binary}")
            print("=" * 60)
            for result in results:
                status = "✓ PASS" if result["status"] == "PASS" else "✗ FAIL"
                print(f"{status} Check {result['id']}: {result['description']}")
                if args.verbose and result.get("details"):
                    print(f"    Details: {result['details']}")
            print("=" * 60)
            print(f"Overall: {passed}/{total} checks passed")
            if passed == total:
                print("✅ BINARY IS BETANET COMPLIANT")
            else:
                print("❌ BINARY IS NOT BETANET COMPLIANT")

        # Generate SBOM if requested
        if args.sbom:
            sbom_data = generate_sbom(args.binary)
            with open(args.sbom_output, "w") as f:
                json.dump(sbom_data, f, indent=2)
            print(f"SBOM generated: {args.sbom_output}")

    except Exception as e:
        print(f"Error running compliance checks: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()