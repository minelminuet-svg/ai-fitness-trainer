#!/usr/bin/env python3
if __name__ == "__main__":
    import os
    base = r'c:\Users\selds\Documents\ai trainer\fitness_trainer'
    os.makedirs(base, exist_ok=True)
    
    dirs = ['main', 'pose_estimation', 'exercises', 'feedback', 'data', 'api', 'ui', 'tests', 'utils']
    for d in dirs:
        path = os.path.join(base, d)
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, '__init__.py')
        with open(init_file, 'w') as f:
            f.write(f'"""Module: {d}"""\n')
        print(f'✓ Created: {d}')
    
    req_file = os.path.join(base, 'requirements.txt')
    with open(req_file, 'w') as f:
        f.write('''opencv-python==4.8.1.78
mediapipe==0.10.8
numpy==1.24.3
scipy==1.11.4
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pygame==2.5.2
pydub==0.25.1
requests==2.31.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0''')
    print('✓ Created: requirements.txt')
    
    gitignore_file = os.path.join(base, '.gitignore')
    with open(gitignore_file, 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*$py.class
*.so
build/
dist/
.venv/
venv/
.env
.idea/
.vscode/
*.log
.coverage
htmlcov/
.pytest_cache/
data/models/
data/logs/''')
    print('✓ Created: .gitignore')
    
    config_file = os.path.join(base, 'config.py')
    with open(config_file, 'w') as f:
        f.write('''"""Configuration module for AI Fitness Trainer"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
LOGS_DIR = DATA_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DB_HOST = os.getenv("DB_HOST", "localhost")
MIN_DETECTION_CONFIDENCE = float(os.getenv("MIN_DETECTION_CONFIDENCE", "0.5"))
''')
    print('✓ Created: config.py')
    
    app_file = os.path.join(base, 'app.py')
    with open(app_file, 'w') as f:
        f.write('''"""Main entry point for AI Fitness Trainer application"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import DEBUG

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    logger.info("Starting AI Fitness Trainer...")
    logger.info(f"Debug mode: {DEBUG}")

if __name__ == "__main__":
    main()
''')
    print('✓ Created: app.py')
    
    env_file = os.path.join(base, '.env.example')
    with open(env_file, 'w') as f:
        f.write('''ENV=development
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
DB_HOST=localhost
DB_PORT=5432
MIN_DETECTION_CONFIDENCE=0.5
''')
    print('✓ Created: .env.example')
    
    readme_file = os.path.join(base, 'README.md')
    with open(readme_file, 'w') as f:
        f.write('''# AI Fitness Trainer

A comprehensive AI-powered fitness training application that uses computer vision and pose estimation to guide users through exercises and provide real-time feedback.

## Project Structure

```
fitness_trainer/
├── main/                    # Main application entry point
├── pose_estimation/         # Pose detection and tracking modules
├── exercises/              # Exercise definitions and logic
├── feedback/               # User feedback generation
├── data/                   # Data storage (models, logs, etc.)
├── api/                    # FastAPI application and routes
├── ui/                     # User interface components
├── utils/                  # Utility functions
├── tests/                  # Unit and integration tests
├── config.py              # Configuration management
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

## Running the Application

```bash
python app.py
```

## Features

- Real-time pose estimation using MediaPipe
- Exercise tracking and form correction
- Performance feedback and analytics
- Interactive UI for exercise guidance
- RESTful API for integration
''')
    print('✓ Created: README.md')
    
    print('\n' + '='*60)
    print('✓ Project structure created successfully!')
    print('='*60)
    print(f'Project location: {base}')
    
    print('\nDirectory listing:')
    os.system(f'dir /s "{base}"')
