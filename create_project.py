import os
base = r'c:\Users\selds\Documents\ai trainer\fitness_trainer'
os.makedirs(base, exist_ok=True)

dirs = ['main', 'pose_estimation', 'exercises', 'feedback', 'data', 'api', 'ui', 'tests', 'utils']
for d in dirs:
    path = os.path.join(base, d)
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, '__init__.py'), 'w').write(f'"""Module: {d}"""\n')

# Create requirements.txt
with open(os.path.join(base, 'requirements.txt'), 'w') as f:
    f.write('opencv-python==4.8.1.78\nmediapipe==0.10.8\nnumpy==1.24.3\nscipy==1.11.4\nfastapi==0.104.1\nuvicorn==0.24.0\npydantic==2.5.0\nsqlalchemy==2.0.23\npsycopg2-binary==2.9.9\npygame==2.5.2\npydub==0.25.1\nrequests==2.31.0\npython-dotenv==1.0.0\npytest==7.4.3\npytest-cov==4.1.0')

with open(os.path.join(base, '.gitignore'), 'w') as f:
    f.write('__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\n.env\n.idea/\n.vscode/')

with open(os.path.join(base, 'config.py'), 'w') as f:
    f.write('"""Configuration module for AI Fitness Trainer"""\n')

with open(os.path.join(base, 'app.py'), 'w') as f:
    f.write('"""Main entry point for AI Fitness Trainer"""\n')

with open(os.path.join(base, '.env.example'), 'w') as f:
    f.write('ENV=development\nDEBUG=true\n')

with open(os.path.join(base, 'README.md'), 'w') as f:
    f.write('# AI Fitness Trainer\n\nProject structure created successfully.')

print('All directories and files created successfully!')

# Now display the directory structure
import subprocess
subprocess.run(['dir', '/s', base], shell=True)
