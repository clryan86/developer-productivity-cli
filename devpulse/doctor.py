from __future__ import annotations
import platform
import shutil
import subprocess
import sys

def version(command):
    path = shutil.which(command)
    if not path:
        return {"installed": False, "path": None, "version": None}
    try:
        completed = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=3)
        text = (completed.stdout or completed.stderr).strip().splitlines()[0]
    except Exception:
        text = "unknown"
    return {"installed": True, "path": path, "version": text}

def doctor():
    return {
        "python": {"version": sys.version.split()[0], "executable": sys.executable},
        "platform": platform.platform(),
        "tools": {name: version(name) for name in ("git", "docker", "node", "npm", "ruff", "pytest")},
    }
