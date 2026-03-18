#!/usr/bin/env python3
"""
Direct execution wrapper to run execute_create.py and display all output
"""
import os
import sys
import subprocess

# Change to the correct directory
os.chdir(r'C:\Users\selds\Documents\ai trainer')

# Run the script and capture output
print("=" * 70)
print("EXECUTING: python execute_create.py")
print("=" * 70)

try:
    # Execute the script directly with output streaming
    process = subprocess.Popen(
        [sys.executable, 'execute_create.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Stream output line by line
    for line in process.stdout:
        print(line, end='')
    
    # Wait for process to complete
    return_code = process.wait()
    
    print("\n" + "=" * 70)
    print(f"SCRIPT EXECUTION COMPLETE (Return Code: {return_code})")
    print("=" * 70)
    
    # Try to read the execution output file if it was created
    try:
        output_file = r'C:\Users\selds\Documents\ai trainer\execution_output.txt'
        if os.path.exists(output_file):
            print("\nContents of execution_output.txt:")
            print("-" * 70)
            with open(output_file, 'r') as f:
                print(f.read())
    except Exception as e:
        print(f"Could not read execution_output.txt: {e}")
    
    sys.exit(return_code)
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
