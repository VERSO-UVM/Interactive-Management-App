#!/bin/bash

# FOR MACOS AND LINUX; you can use this shellscript to help setup the development
# environment for the ORCA ism-app project

# FOR WINDOWS; you can also use this shellscript, but you need to use the
# Windows Subsystem for Linux. To install it:
# 1. Open PowerShell or Command Prompt **as an administrator**
# 2. Run this command: wsl --install

# https://learn.microsoft.com/en-us/windows/wsl/install


# You should only need to run this script once, when you are first using your workspace.
# You might need to run it again if new packages are added to requirements.txt


clear

# First, cleanup the previous setup
echo 'Removing old setup...'
echo 'Removing Python venv...'
rm -rf venv

# Then, create a new Python virtual environment
echo 'Setting up Python venv...'
python3 -m venv venv

# Now we run commands from within the venv
source venv/bin/activate

# And finally recursively install pip packages from project requirements
echo 'Installing pip packages...'
pip install -r requirements.txt

clear

# Finished - instructions below are to setup (currently optional) Flake8 linter w/ longer line limit
echo 'Finished setting up the Python virtual environment'
echo 'OPTIONALLY setup the Flake8 Linter (VSCode only):'
echo '1. Search for and install the extension: "Flake8"'
echo '2. Open the Flake8 Extension settings'
echo '3. For the first option, "Flake8: Args", increase the line length limit by adding this item:'
echo "    --max-line-length=160"
