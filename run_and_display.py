#!/usr/bin/env python
import subprocess
import sys

# Execute the create_ai_trainer.py script
result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\create_ai_trainer.py'], 
                       capture_output=False, text=True)
sys.exit(result.returncode)
