import os
import sys
import subprocess

# First, run the original create_project.py
exec(open(r'c:\Users\selds\Documents\ai trainer\create_project.py').read())

# Then display a nicely formatted directory tree
def show_tree(path, prefix="", is_last=True):
    """Display directory tree structure"""
    if os.path.isdir(path):
        items = sorted(os.listdir(path))
        # Filter out hidden files except important ones
        items = [item for item in items if not item.startswith('.') or item in ['.gitignore', '.env.example']]
        
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last_item = i == len(items) - 1
            
            current_prefix = "└── " if is_last_item else "├── "
            print(prefix + current_prefix + item)
            
            if os.path.isdir(item_path) and item not in ['__pycache__', '.git', '.venv', 'venv']:
                extension = "    " if is_last_item else "│   "
                show_tree(item_path, prefix + extension, is_last_item)

print("\n" + "="*60)
print("FINAL PROJECT DIRECTORY STRUCTURE")
print("="*60 + "\n")
show_tree(r'c:\Users\selds\Documents\ai trainer\fitness_trainer')
print("\n" + "="*60)
