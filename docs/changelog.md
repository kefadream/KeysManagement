# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Functionality to create empty keys automatically.
- Logging setup for better error tracking and debugging.

### Changed
- Improved error handling and logging throughout the application.
- Updated user interface for better usability.

### Fixed
- Fixed issues with file reading in `FileTreeWindow`.

## [1.0.0] - 2024-08-01

### Added
- Initial release of the application.
- Functionality to create, modify, and delete groups and keys.
- Support for managing keys with file content.
- Theme selector for the graphical interface.
Script to Create Documentation Files
To automate the creation of these documentation files, you can use the following script:

python
Copier le code
import os

def create_docs():
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)

    documentation_files = {
        "README.md": """
# Project Documentation

This is the main documentation for the project.

## Overview

This project is designed to manage groups and keys with various functionalities such as creating, modifying, and deleting groups and keys. The application uses a graphical user interface built with Tkinter and supports operations with JSON storage.

## Features

- Create, modify, and delete groups and keys.
- Automatically generate unique keys.
- Manage keys with file contents.
- Use themes for the graphical interface.

## Getting Started

To get started with the project, follow the setup instructions in `setup.md`.

## Documentation

- [Setup Instructions](setup.md)
- [Usage Guide](usage.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)
""",
        "setup.md": """
# Setup Instructions

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Tkinter (usually comes with Python installations)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/yourproject.git
Navigate to the project directory:

sh
Copier le code
cd yourproject
Install required packages:

sh
Copier le code
pip install -r requirements.txt
Create example files (optional):

sh
Copier le code
python create_example_files.py
Run the application:

sh
Copier le code
python app.py
Configuration
The application uses a data.json file for storage. This file will be created automatically in the project root if it does not exist.
""",
"usage.md": """

Usage Guide
Running the Application
To run the application, navigate to the project directory and execute the following command:

sh
Copier le code
python app.py
User Interface
Theme Selector
Choose a theme from the dropdown menu to change the appearance of the application.
Creating a Group
Enter the group name in the provided entry field.
Click the "Créer le groupe" button to create the group.
Creating a Key
Select a group from the list.
Enter the key name and value in the provided entry fields.
Click the "Créer la clé" button to create the key.
Creating a Key with File Content
Click the "Créer la clé avec fichier" button.
In the new window, select a file from the file tree.
Right-click on the file and choose to add its content to an existing key or create a new key.
Automatically Creating an Empty Key
Select a group from the list.
Click the "Créer une clé vide automatiquement" button to create an empty key with a unique name.
Managing Groups and Keys
Select a group to view its keys.
Use the provided buttons to delete or modify groups and keys.
""",
"contributing.md": """
Contributing
We welcome contributions to this project. To contribute, follow these steps:

Fork the Repository
Fork the repository on GitHub.
Clone your forked repository:
sh
Copier le code
git clone https://github.com/yourusername/yourproject.git
Navigate to the project directory:
sh
Copier le code
cd yourproject
Make Changes
Create a new branch for your changes:
sh
Copier le code
git checkout -b my-feature-branch
Make your changes in the codebase.
Commit your changes with a descriptive commit message:
sh
Copier le code
git commit -am 'Add new feature'
Submit a Pull Request
Push your changes to your forked repository:
sh
Copier le code
git push origin my-feature-branch
Open a pull request on the original repository.
Guidelines
Ensure your code follows the project's coding style.
Write descriptive commit messages.
Update the documentation if necessary.
Test your changes before submitting a pull request.
""",
"changelog.md": """
Changelog
All notable changes to this project will be documented in this file.

[Unreleased]
Added
Functionality to create empty keys automatically.
Logging setup for better error tracking and debugging.
Changed
Improved error handling and logging throughout the application.
Updated user interface for better usability.
Fixed
Fixed issues with file reading in FileTreeWindow.
[1.0.0] - 2024-08-01
Added
Initial release of the application.

Functionality to create, modify, and delete groups and keys.

Support for managing keys with file content.

Theme selector for the graphical interface.
"""
}

for filename, content in documentation_files.items():
file_path = os.path.join(docs_dir, filename)
with open(file_path, 'w', encoding='utf-8') as file:
file.write(content.strip())

print(f"Documentation files created in '{docs_dir}' directory.")

if name == "main":
create_docs()