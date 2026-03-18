#!/usr/bin/env python
"""Wrapper to execute full_execution.py"""
import sys
import subprocess

# Execute the script
result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\full_execution.py'], 
                       capture_output=False, text=True)
sys.exit(result.returncode)
