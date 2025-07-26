#HEIC to JPEG Converter (with GUI)
---------------------------------

A simple Python tool to batch convert HEIC images into JPEGs.
Includes a graphical interface, progress bar, estimated time remaining, and automatic module installation.

FEATURES
--------
- Converts all .HEIC images in a selected folder (including subfolders) to .JPG format
- Multithreaded for faster performance
- Maintains high image quality (JPEG quality 95, no subsampling)
- Automatically installs required modules (pillow and pillow-heif)
- Progress bar shows total progress based on file size
- Displays estimated time and remaining image count
- Easy-to-use GUI — no command line knowledge needed

REQUIREMENTS
------------
- Python 3.11 or later
- Windows OS (recommended for GUI compatibility)

HOW TO USE
----------
1. Run the Python script:
   python heic_to_jpg_converter.py

2. Select the folder containing your .HEIC images when prompted.

3. Select the folder where you want the converted .JPG images saved.

4. Wait until all files are processed. Progress and estimated time will be shown in the interface.

RECOMMENDED .gitignore ENTRIES
------------------------------
__pycache__/
*.pyc
*.pyo
*.exe
*.spec
build/
dist/

AUTHOR
------
Created by Andyandebb (GitHub)
