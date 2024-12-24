import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# List of files and directories relative to the current root
list_of_files = [
    "docs/.gitkeep",
    "flowcharts/.gitkeep",
    "notebooks/.gitkeep",
    "src/leaflogic/__init__.py",
    "src/leaflogic/logger/__init__.py",
    "src/leaflogic/exception/__init__.py",
    "src/leaflogic/utils/__init__.py",
    ".gitignore",
    "demo.py",
    "LICENSE",
    "README.md",
    "requirements.txt",
    "scripts.sh",
    "setup.py",
    "template.py"
]


# File and directory creation logic
for filepath in list_of_files:
    filepath = Path(filepath)

    # Split file directory and filename
    filedir, filename = os.path.split(filepath)

    # Create directories if needed
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    # Create file if it doesn't exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath} already exists")