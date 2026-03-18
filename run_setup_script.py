#!/usr/bin/env python3
"""Execute final_setup.py and display the result"""
import os
import sys

# Change to the working directory
os.chdir(r'c:\Users\selds\Documents\ai trainer')
sys.path.insert(0, os.getcwd())

# Execute the setup file
try:
    with open('final_setup.py', 'r', encoding='utf-8') as f:
        code_to_exec = f.read()
    # Execute the code
    exec(code_to_exec, {'__name__': '__main__', '__file__': 'final_setup.py'})
except Exception as e:
    print(f"Error executing final_setup.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
