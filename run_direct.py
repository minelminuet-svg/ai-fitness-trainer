import os
import sys
from pathlib import Path

# Ensure we're in the right directory for execution
os.chdir(r'c:\Users\selds\Documents\ai trainer')

# Now execute the create_ai_trainer.py script
with open('create_ai_trainer.py', 'r') as f:
    script_code = f.read()

# Execute in the current namespace to capture all output
exec(script_code)
