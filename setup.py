import os

def create_directory_structure():
    """Create the initial directory structure for Posterfy."""
    directories = [
        'src/posterfy/api',
        'src/posterfy/image_processing',
        'src/posterfy/utils',
        'tests',
        'examples/outputs'
    ]
    
    files = {
        'src/posterfy/api': [
            'spotify.py',
            'imgur.py',
            'gelato.py',
            '__init__.py'
        ],
        'src/posterfy/image_processing': [
            'noise.py',
            'transformations.py',
            '__init__.py'
        ],
        'src/posterfy/utils': [
            'color.py',
            'text.py',
            '__init__.py'
        ],
        'src/posterfy': [
            '__init__.py',
            'config.py'
        ],
        'tests': [
            '__init__.py',
            'test_spotify.py',
            'test_image_processing.py',
            'test_utils.py'
        ],
        '': [
            'README.md',
            'requirements.txt',
            '.gitignore',
            'main.py'
        ]
    }
    
    # Create directories and files
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create all specified files
    for directory, filenames in files.items():
        for filename in filenames:
            filepath = os.path.join(directory, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    pass

if __name__ == "__main__":
    create_directory_structure()
    print("Project structure created successfully!")