import subprocess
import sys

result = subprocess.run([sys.executable, r'c:\Users\selds\Documents\ai trainer\run_project_creator.py'], 
                       capture_output=False, text=True)
sys.exit(result.returncode)
