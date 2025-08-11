import hashlib
import os
import json
import subprocess
import datetime
from typing import Dict, Any

def generate_sbom(binary_path: str) -> Dict[str, Any]:
    """
    Generate a Software Bill of Materials (SBOM) for the binary.
    """
    # Get binary metadata
    stat_info = os.stat(binary_path)
    
    # Calculate hashes
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()
    
    with open(binary_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            hash_sha1.update(chunk)
            hash_sha256.update(chunk)
    
    # Get file info
    file_name = os.path.basename(binary_path)
    file_size = stat_info.st_size
    modification_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).isoformat()
    
    # Try to get version info
    version_info = "Unknown"
    try:
        result = subprocess.run(
            [binary_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_info = result.stdout.strip()
    except:
        pass
    
    # Create SBOM structure
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "Betanet",
                    "name": "Spec-Compliance Linter",
                    "version": "1.0.0"
                }
            ],
            "component": {
                "type": "application",
                "name": file_name,
                "version": version_info,
                "hashes": [
                    {
                        "alg": "MD5",
                        "content": hash_md5.hexdigest()
                    },
                    {
                        "alg": "SHA-1",
                        "content": hash_sha1.hexdigest()
                    },
                    {
                        "alg": "SHA-256",
                        "content": hash_sha256.hexdigest()
                    }
                ]
            }
        },
        "components": [
            {
                "type": "file",
                "name": file_name,
                "version": version_info,
                "hashes": [
                    {
                        "alg": "MD5",
                        "content": hash_md5.hexdigest()
                    },
                    {
                        "alg": "SHA-1",
                        "content": hash_sha1.hexdigest()
                    },
                    {
                        "alg": "SHA-256",
                        "content": hash_sha256.hexdigest()
                    }
                ],
                "size": file_size,
                "modified": modification_time
            }
        ]
    }
    
    return sbom