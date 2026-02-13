# Wrapper module for auth functions
# This ensures imports work on Streamlit Cloud

import sys
import os
from pathlib import Path

# Get the directory where this file is located
_this_dir = Path(__file__).parent.resolve()
_lib_dir = _this_dir / "lib"

# Try to import from lib, fallback to inline
try:
    from lib.auth import register, verify
except (ModuleNotFoundError, ImportError):
    # Fallback: read and exec the auth module
    auth_file = _lib_dir / "auth.py"
    if auth_file.exists():
        exec(open(auth_file).read())
    else:
        raise ImportError("Could not find auth module")
