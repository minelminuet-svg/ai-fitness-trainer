"""Direct execution of final_setup.py logic"""
import os
import sys

# Ensure we're in the right directory
os.chdir(r'c:\Users\selds\Documents\ai trainer')

# Create all necessary directories and files
base = r'c:\Users\selds\Documents\ai trainer\fitness_trainer'

# Create main directory
os.makedirs(base, exist_ok=True)

# Create subdirectories
dirs = ['main', 'pose_estimation', 'exercises', 'feedback', 'data', 'api', 'ui', 'tests', 'utils']

for d in dirs:
    path = os.path.join(base, d)
    os.makedirs(path, exist_ok=True)
    init_file = os.path.join(path, '__init__.py')
    with open(init_file, 'w') as f:
        f.write(f'"""Module: {d}"""\n')
    print(f'Created: {d}')

# requirements.txt
req_content = '''opencv-python==4.8.1.78
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
pytest-cov==4.1.0'''

with open(os.path.join(base, 'requirements.txt'), 'w') as f:
    f.write(req_content)
print('Created: requirements.txt')

# .gitignore
gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so
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
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
instance/
.webassets-cache
.scrapy
docs/_build/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.python-version
Pipfile.lock
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
data/models/
data/logs/
output/
temp/'''

with open(os.path.join(base, '.gitignore'), 'w') as f:
    f.write(gitignore_content)
print('Created: .gitignore')

# config.py
config_content = '''"""Configuration module for AI Fitness Trainer"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
LOGS_DIR = DATA_DIR / "logs"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Environment
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "fitness_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "fitness_trainer")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Pose Estimation Configuration
MIN_DETECTION_CONFIDENCE = float(os.getenv("MIN_DETECTION_CONFIDENCE", "0.5"))
MIN_TRACKING_CONFIDENCE = float(os.getenv("MIN_TRACKING_CONFIDENCE", "0.5"))

# Exercise Configuration
TARGET_REPS = int(os.getenv("TARGET_REPS", "10"))
TARGET_SETS = int(os.getenv("TARGET_SETS", "3"))

# UI Configuration
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1280"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "720"))
FPS = int(os.getenv("FPS", "30"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
'''

with open(os.path.join(base, 'config.py'), 'w') as f:
    f.write(config_content)
print('Created: config.py')

# app.py
app_content = '''"""Main entry point for AI Fitness Trainer application"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import LOG_LEVEL, LOG_FORMAT, DEBUG

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    logger.info("Starting AI Fitness Trainer...")
    logger.info(f"Debug mode: {DEBUG}")
    
    try:
        # Import main module
        from main import app as main_app
        
        # Start the application
        main_app.run()
        
    except ImportError as e:
        logger.error(f"Failed to import main module: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

with open(os.path.join(base, 'app.py'), 'w') as f:
    f.write(app_content)
print('Created: app.py')

# .env.example
env_content = '''# Environment
ENV=development
DEBUG=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=fitness_user
DB_PASSWORD=password
DB_NAME=fitness_trainer

# Pose Estimation Configuration
MIN_DETECTION_CONFIDENCE=0.5
MIN_TRACKING_CONFIDENCE=0.5

# Exercise Configuration
TARGET_REPS=10
TARGET_SETS=3

# UI Configuration
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
FPS=30

# Logging Configuration
LOG_LEVEL=INFO
'''

with open(os.path.join(base, '.env.example'), 'w') as f:
    f.write(env_content)
print('Created: .env.example')

# README.md
readme_content = '''# AI Fitness Trainer

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

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Running the Application

```bash
python app.py
```

## Testing

```bash
pytest
pytest --cov=.  # with coverage
```

## Features

- Real-time pose estimation using MediaPipe
- Exercise tracking and form correction
- Performance feedback and analytics
- Interactive UI for exercise guidance
- RESTful API for integration

## Requirements

- Python 3.8+
- See requirements.txt for dependencies

## License

MIT License
'''

with open(os.path.join(base, 'README.md'), 'w') as f:
    f.write(readme_content)
print('Created: README.md')

print('\n' + '='*50)
print('Project structure created successfully!')
print('='*50)
print(f'Project location: {base}')

# Show directory listing
print('\n\nDirectory listing:\n')
os.system(f'dir /s "{base}"')
