@echo off
REM Simple setup script for AI Fitness Trainer
setlocal enabledelayedexpansion

REM Create base directory
mkdir "c:\Users\selds\Documents\ai trainer\fitness_trainer"

REM Create subdirectories
for %%D in (main pose_estimation exercises feedback data api ui tests utils) do (
    mkdir "c:\Users\selds\Documents\ai trainer\fitness_trainer\%%D"
    echo.> "c:\Users\selds\Documents\ai trainer\fitness_trainer\%%D\__init__.py"
)

REM Create requirements.txt
(
echo opencv-python==4.8.1.78
echo mediapipe==0.10.8
echo numpy==1.24.3
echo scipy==1.11.4
echo fastapi==0.104.1
echo uvicorn==0.24.0
echo pydantic==2.5.0
echo sqlalchemy==2.0.23
echo psycopg2-binary==2.9.9
echo pygame==2.5.2
echo pydub==0.25.1
echo requests==2.31.0
echo python-dotenv==1.0.0
echo pytest==7.4.3
echo pytest-cov==4.1.0
) > "c:\Users\selds\Documents\ai trainer\fitness_trainer\requirements.txt"

echo.
echo Project structure created successfully!
echo.
echo Directory listing:
dir /s "c:\Users\selds\Documents\ai trainer\fitness_trainer"

pause
