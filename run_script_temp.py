#!/usr/bin/env python
import subprocess
import sys

result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\execute_create.py'], capture_output=False)
sys.exit(result.returncode)
