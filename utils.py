import os
import subprocess
import json
from typing import Optional

def is_executable(path: str) -> bool:
    """Check if a file is executable."""
    return os.path.isfile(path) and os.access(path, os.X_OK)

def get_binary_info(binary_path: str) -> dict:
    """Get basic information about the binary."""
    try:
        stat_info = os.stat(binary_path)
        return {
            "path": binary_path,
            "size": stat_info.st_size,
            "modified": stat_info.st_mtime,
            "executable": is_executable(binary_path)
        }
    except Exception as e:
        return {
            "path": binary_path,
            "error": str(e)
        }

def run_command(command: list, timeout: int = 30) -> dict:
    """Run a command and return result."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "error": "timeout"
        }
    except Exception as e:
        return {
            "returncode": -1,
            "error": str(e)
        }

def get_help_output(binary_path: str, timeout: int = 10) -> str:
    """
    Retrieve the lower‑cased help text from a binary or script.  If the
    candidate is a Python script or lacks executable permission, this helper
    will attempt to invoke it via ``sys.executable``.  It falls back to
    executing the file directly if that fails.

    Returns an empty string on failure.
    """
    import subprocess
    import sys
    import os
    # Determine whether to call via Python interpreter
    try_python = binary_path.lower().endswith('.py') or not os.access(binary_path, os.X_OK)
    commands = []
    if try_python:
        commands.append([sys.executable, binary_path, '--help'])
    # Always attempt to run the binary directly as a fallback
    commands.append([binary_path, '--help'])
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0 and result.stdout:
                return result.stdout.lower()
        except Exception:
            continue
    return ''