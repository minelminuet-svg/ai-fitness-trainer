import subprocess
import sys

result = subprocess.run(
    [sys.executable, r'c:\Users\selds\Documents\ai trainer\full_execution.py'],
    capture_output=False,
    text=True
)
sys.exit(result.returncode)
