@echo off
cd /d "c:\Users\selds\Documents\ai trainer"
python.exe create_fitness_trainer.py
echo.
echo ================================
echo DIRECTORY TREE
echo ================================
echo.
tree fitness_trainer /f
pause
