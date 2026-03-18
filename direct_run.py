#!/usr/bin/env python
import subprocess
import sys

# Execute the script
result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\create_ai_trainer.py'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
sys.exit(result.returncode)
