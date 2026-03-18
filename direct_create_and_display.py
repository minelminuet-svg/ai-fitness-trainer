#!/usr/bin/env python3
"""
Direct project creation and display script
"""
import os
import sys

def main():
    # Define base path
    base = r'c:\Users\selds\Documents\ai trainer\fitness_trainer'
    
    # Create base directory
    print(f"Creating base directory: {base}")
    os.makedirs(base, exist_ok=True)
    
    # Create subdirectories
    dirs = ['main', 'pose_estimation', 'exercises', 'feedback', 'data', 'api', 'ui', 'tests', 'utils']
    print(f"\nCreating {len(dirs)} subdirectories...")
    for d in dirs:
        path = os.path.join(base, d)
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, '__init__.py')
        with open(init_file, 'w') as f:
            f.write(f'"""Module: {d}"""\n')
        print(f"  ✓ Created: {d}/")
    
    # Create requirements.txt
    print(f"\nCreating configuration files...")
    requirements_content = """opencv-python==4.8.1.78
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
pytest-cov==4.1.0"""
    
    with open(os.path.join(base, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)
    print("  ✓ Created: requirements.txt")
    
    # Create .gitignore
    gitignore_content = """__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.env
.idea/
.vscode/"""
    
    with open(os.path.join(base, '.gitignore'), 'w') as f:
        f.write(gitignore_content)
    print("  ✓ Created: .gitignore")
    
    # Create config.py
    with open(os.path.join(base, 'config.py'), 'w') as f:
        f.write('"""Configuration module for AI Fitness Trainer"""\n')
    print("  ✓ Created: config.py")
    
    # Create app.py
    with open(os.path.join(base, 'app.py'), 'w') as f:
        f.write('"""Main entry point for AI Fitness Trainer"""\n')
    print("  ✓ Created: app.py")
    
    # Create .env.example
    with open(os.path.join(base, '.env.example'), 'w') as f:
        f.write('ENV=development\nDEBUG=true\n')
    print("  ✓ Created: .env.example")
    
    # Create README.md
    with open(os.path.join(base, 'README.md'), 'w') as f:
        f.write('# AI Fitness Trainer\n\nProject structure created successfully.')
    print("  ✓ Created: README.md")
    
    print(f"\n{'='*70}")
    print("ALL DIRECTORIES AND FILES CREATED SUCCESSFULLY!")
    print(f"{'='*70}\n")
    
    # Display directory structure
    print("FINAL PROJECT DIRECTORY STRUCTURE:")
    print(f"{'='*70}\n")
    show_tree(base)
    print(f"\n{'='*70}")
    print(f"Project location: {base}")
    print(f"{'='*70}\n")

def show_tree(path, prefix="", is_last=True, max_depth=3, current_depth=0):
    """Display directory tree structure"""
    if current_depth >= max_depth:
        return
    
    if not os.path.isdir(path):
        return
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return
    
    # Filter out hidden files except important ones
    items = [item for item in items if not item.startswith('.') or item in ['.gitignore', '.env.example']]
    
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last_item = i == len(items) - 1
        
        # Determine the prefix characters
        current_prefix = "└── " if is_last_item else "├── "
        print(prefix + current_prefix + item)
        
        # Recursively show subdirectories
        if os.path.isdir(item_path) and item not in ['__pycache__', '.git', '.venv', 'venv']:
            extension = "    " if is_last_item else "│   "
            show_tree(item_path, prefix + extension, is_last_item, max_depth, current_depth + 1)

if __name__ == '__main__':
    main()
