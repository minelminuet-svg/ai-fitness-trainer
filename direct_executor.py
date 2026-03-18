import os
import sys
from pathlib import Path

# Execute final_setup.py directly
os.chdir(r'c:\Users\selds\Documents\ai trainer')

# Import and execute the setup
with open('final_setup.py', 'r') as f:
    code = f.read()
    exec(code)
