# Nitrobyte Auto Installer
This script automates the installation of multiple programs from a provided list.

Features

- Installs programs sequentially or concurrently based on arguments.
- Provides visual feedback during installation with loading animations.
- Handles MSI and non-MSI installers.
- Detects installation errors and provides exit codes.
- Optionally prompts for a system restart after installation.

## Usage

### Paths file:

This script reads a text file containing a list of installer paths, allowing you to manage installers in a separate location.

- Create a text file named paths.txt (or use a different name with the --path_file argument) in the same directory as the script (or a specified location).
- List each installer path on a separate line in the paths.txt file.

### Using the Python script directly:
- Create paths file (See above).
- Run the script: Open a terminal or command prompt and navigate to the directory containing the script and installers. Run the script with the following command:

    python script.py [arguments]

### Using a compiled executable:
- Create paths file (See above)
- Double-click the executable file to run the installer. You may be prompted for administrator privileges.
- Arguments: The executable functions identically to the script and accepts the same command-line arguments described below.

## Arguments:

    --loading_type: Specify the loading animation type (options defined in loading_types.json). Defaults to "spinning_bar".
    --seq: Force sequential installation (each program waits for the previous to finish).
    --path_file: Specify a custom path file containing installer paths (defaults to "paths.txt").

## Example: 
Install programs sequentially with a custom loading animation:

    python main.py --loading_type=straight_bar --seq
    executable.exe --loading_type=straight_bar --seq

Note: Script requires administrator privileges to run installers.

## Dependencies

    Python 3

## Exit Codes

    0: Successful installation of all programs.
    1: Error during script execution.
    Non-zero (returned by installer): Installation failure of a specific program.
