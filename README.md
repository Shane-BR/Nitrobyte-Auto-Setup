# Automated Installer

This project is an automated installer script written in Python. It uses the `pyautogui` and `win32api` libraries to interact with the operating system and automate the installation of multiple programs.

## Features

- Changes the OS resolution to fit the given screenshots.
- Launches each program listed in a text file.
- Navigates through each installer by clicking buttons identified by screenshots.
- Waits until the current program is finished installing before closing it.
- Changes the resolution back to the original after all installations are complete.

## Requirements

- Python 3
- `pyautogui`
- `win32api`
- `win32con`
- `pywintypes`

## Usage

You can run the script with optional command line arguments to specify the button search time and the output width and height. If not specified, the button search time defaults to 5 seconds, and the output width and height default to 1280x1024.

```bash
./main.exe [button_search_time] [op_width] [op_height]

## The paths.txt File

The `paths.txt` file is a crucial part of this project. It contains the file paths to the installers that the script will automate. Each path should be on a new line. Here's an example of what the `paths.txt` file might look like:

```plaintext
C:/Users/user/Downloads/installer1.exe
C:/Users/user/Downloads/installer2.exe
C:/Users/user/Downloads/installer3.exe
