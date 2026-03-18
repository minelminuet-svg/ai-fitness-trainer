import sys
import io
from pathlib import Path

# Redirect stdout to capture all output
old_stdout = sys.stdout
sys.stdout = captured_output = io.StringIO()

try:
    # Change to the directory and run the script
    sys.path.insert(0, r'c:\Users\selds\Documents\ai trainer')
    exec(open(r'c:\Users\selds\Documents\ai trainer\create_ai_trainer.py').read())
finally:
    # Restore stdout and print the captured output
    sys.stdout = old_stdout
    output = captured_output.getvalue()
    print(output)
    if output:
        # Also write to a file for reference
        with open(r'c:\Users\selds\Documents\ai trainer\script_output.txt', 'w') as f:
            f.write(output)
