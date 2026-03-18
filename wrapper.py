import subprocess
import sys

result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\direct_create_and_display.py'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("ERRORS:", result.stderr)
sys.exit(result.returncode)
