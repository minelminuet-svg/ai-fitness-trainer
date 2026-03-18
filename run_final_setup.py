#!/usr/bin/env python3
"""Wrapper to execute final_setup.py and show directory structure"""
import os
import sys
import subprocess
from pathlib import Path

# Set working directory
work_dir = Path(r'c:\Users\selds\Documents\ai trainer')
os.chdir(work_dir)

print("Executing final_setup.py...")
print("=" * 50)

# Execute the setup script
exec(open('final_setup.py').read())
