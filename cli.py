import argparse
import sys
import json
import os
from typing import List, Dict
# Import checker and SBOM generator from the local modules.  We avoid
# dotted package names here because the parent directory has a space in its
# name ("betanet LINTER").  Using relative imports makes the code work
# when running the CLI from source and when installed via setup.py.
from checker import run_all_checks
from sbom import generate_sbom

def main():
    parser = argparse.ArgumentParser(
        description="Betanet Spec-Compliance Linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  betanet-linter --binary C:\\path\\to\\binary.exe
  betanet-linter --binary C:\\path\\to\\binary.exe --output report.json
  betanet-linter --binary C:\\path\\to\\binary.exe --sbom --sbom-output sbom.json
        """
    )
    
    parser.add_argument(
        "--binary", 
        "-b",
        required=True,
        help="Path to the candidate binary to check"
    )
    
    parser.add_argument(
        "--output", 
        "-o",
        help="Output file for the compliance report (JSON format)"
    )
    
    parser.add_argument(
        "--sbom",
        action="store_true",
        help="Generate Software Bill of Materials (SBOM)"
    )
    
    parser.add_argument(
        "--sbom-output",
        default="sbom.json",
        help="Output file for the SBOM (default: sbom.json)"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate binary path
    if not os.path.exists(args.binary):
        print(f"Error: Binary file '{args.binary}' not found")
        sys.exit(1)
    
    # Check if file is executable (Windows: check extension)
    if not (args.binary.lower().endswith('.exe') or os.access(args.binary, os.X_OK)):
        print(f"Warning: Binary file '{args.binary}' may not be executable")
    
    # Run all checks
    try:
        results = run_all_checks(args.binary, args.verbose)
        passed = sum(1 for r in results if r["status"] == "PASS")
        total = len(results)
        
        # Generate output
        if args.format == "json":
            output_data = {
                "binary": args.binary,
                "passed": passed,
                "total": total,
                "compliant": passed == total,
                "checks": results
            }
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                print(f"Report saved to {args.output}")
            else:
                print(json.dumps(output_data, indent=2))
        else:
            # Text format
            print(f"Betanet Compliance Report for: {args.binary}")
            print("=" * 60)
            for result in results:
                status = "✓ PASS" if result["status"] == "PASS" else "✗ FAIL"
                print(f"{status} Check {result['id']}: {result['description']}")
                if args.verbose and result["details"]:
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
            with open(args.sbom_output, 'w') as f:
                json.dump(sbom_data, f, indent=2)
            print(f"SBOM generated: {args.sbom_output}")
            
    except Exception as e:
        print(f"Error running compliance checks: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()