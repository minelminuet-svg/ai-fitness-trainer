# AI Fitness Trainer

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
