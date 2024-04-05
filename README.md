# Silent Installer (Windows Only)

This script silently installs programs from a list (paths.txt) on Windows systems only.

### Pre-built Executable:

If you don't want to build the script yourself, download the pre-compiled executable (.exe file) from the Releases tab! This eliminates the need for Python on your system.

## Building from Source (Python 3 Required):

- Install Python 3.x (https://www.python.org/downloads/)
- Run: python main.py

## Using paths.txt:

Create a text file named paths.txt in the same directory as the script or executable.
In paths.txt, enter the absolute path to each program you want to install silently, one path per line. An absolute path includes the full drive letter, folder structure, and filename (e.g., C:\Program Files\Example\setup.exe).

## Example paths.txt:

    C:\Program Files\Example\setup.exe
    D:\Games\AwesomeGame\Installer.msi

## Features:

- Progress bar with status for each program.
- Summary at the end.
- Handles MSI and executable installers.

### Notes:

Silent installs may bypass prompts. Verify paths in paths.txt are correct and that you have permission to install the programs.
Script may not display progress correctly everywhere.

### Disclaimer:

Use at your own risk. Ensure permissions and program compatibility.
