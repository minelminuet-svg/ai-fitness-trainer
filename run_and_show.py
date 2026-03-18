#!/usr/bin/env python3
import subprocess
import sys

try:
    result = subprocess.run([sys.executable, 'execute_create.py'], 
                          capture_output=False, 
                          text=True,
                          cwd=r'C:\Users\selds\Documents\ai trainer')
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
