import subprocess
import sys

# Run the full_execution.py script
result = subprocess.run(
    [sys.executable, r'c:\Users\selds\Documents\ai trainer\full_execution.py'],
    capture_output=True,
    text=True,
    cwd=r'c:\Users\selds\Documents\ai trainer'
)

# Print all output
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Return code:", result.returncode)
