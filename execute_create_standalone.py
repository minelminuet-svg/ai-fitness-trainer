import os
from pathlib import Path
import sys
import io

# Redirect output to capture it
output_capture = io.StringIO()

def log(message):
    print(message)
    output_capture.write(message + '\n')

# Create main directory
base_dir = Path(r'c:\Users\selds\Documents\ai trainer\fitness_trainer')
base_dir.mkdir(parents=True, exist_ok=True)
log(f'✓ Created main directory: {base_dir}')

# Create subdirectories
subdirs = ['main', 'pose_estimation', 'exercises', 'feedback', 'data', 'api', 'ui', 'tests', 'utils']
for subdir in subdirs:
    subdir_path = base_dir / subdir
    subdir_path.mkdir(exist_ok=True)
    init_file = subdir_path / '__init__.py'
    init_file.touch()
    log(f'✓ Created {subdir}/')

# Create requirements.txt
requirements_content = """opencv-python==4.8.1.78
mediapipe==0.10.3
numpy==1.24.3
Flask==3.0.0
python-dotenv==1.0.0
Pillow==10.0.1
scipy==1.11.3
tensorflow==2.13.0
scikit-learn==1.3.1
matplotlib==3.8.1
"""
(base_dir / 'requirements.txt').write_text(requirements_content)
log('✓ Created requirements.txt')

# Create .gitignore
gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Data and logs
*.log
data/
models/
outputs/
*.mp4
*.avi
*.png
*.jpg

# OS
.DS_Store
Thumbs.db
"""
(base_dir / '.gitignore').write_text(gitignore_content)
log('✓ Created .gitignore')

# Create config.py
config_content = '''"""Configuration settings for AI Fitness Trainer"""
import os
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Model settings
POSE_MODEL = 'pose_landmarker_lite.task'
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Video settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# API settings
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')
'''
(base_dir / 'config.py').write_text(config_content)
log('✓ Created config.py')

# Create app.py
app_content = '''"""Main entry point for AI Fitness Trainer"""
from flask import Flask
from config import DEBUG, PORT, HOST

app = Flask(__name__)

@app.route('/')
def index():
    return {'message': 'AI Fitness Trainer API'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
'''
(base_dir / 'app.py').write_text(app_content)
log('✓ Created app.py')

# Create .env.example
env_example_content = """# Environment Configuration
DEBUG=True
PORT=5000
HOST=0.0.0.0
MODEL_PATH=./models
DATA_PATH=./data
"""
(base_dir / '.env.example').write_text(env_example_content)
log('✓ Created .env.example')

# Create README.md
readme_content = """# AI Fitness Trainer

An AI-powered fitness training application using pose estimation and exercise tracking.

## Features
- Real-time pose estimation using MediaPipe
- Exercise recognition and form analysis
- Real-time feedback on exercise execution
- Web UI for interactive training sessions
- REST API for integration

## Project Structure
- **main/**: Core application logic
- **pose_estimation/**: Pose detection and processing
- **exercises/**: Exercise definitions and validation
- **feedback/**: Real-time feedback engine
- **data/**: Data storage and management
- **api/**: Flask REST API endpoints
- **ui/**: Web user interface
- **tests/**: Unit and integration tests
- **utils/**: Utility functions and helpers

## Installation
1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Copy .env.example to .env and configure settings
4. Run the application: python app.py

## Usage
```python
from main import FitnessTrainer
trainer = FitnessTrainer()
trainer.start()
```

## License
MIT
"""
(base_dir / 'README.md').write_text(readme_content)
log('✓ Created README.md')

log('\n' + '='*60)
log('All files created successfully!')
log('='*60)
log(f'\nBase directory: {base_dir}')
log('\n' + '='*60)
log('FINAL DIRECTORY STRUCTURE')
log('='*60)

# Display tree structure
def print_tree(directory, prefix="", is_last=True, max_depth=5, current_depth=0):
    if current_depth >= max_depth:
        return
    
    path = Path(directory)
    try:
        items = sorted(path.iterdir())
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        current_prefix = "└── " if is_last_item else "├── "
        msg = f"{prefix}{current_prefix}{item.name}"
        log(msg)
        
        if item.is_dir() and current_depth < max_depth - 1:
            next_prefix = prefix + ("    " if is_last_item else "│   ")
            print_tree(item, next_prefix, is_last_item, max_depth, current_depth + 1)

log(f"\nfitness_trainer/")
print_tree(base_dir)

log("\n" + "="*60)
log("SCRIPT EXECUTION COMPLETE")
log("="*60)

# Save output to file
output_file = base_dir.parent / 'execution_output.txt'
with open(output_file, 'w') as f:
    f.write(output_capture.getvalue())

log(f"\nOutput saved to: {output_file}")

sys.exit(0)
