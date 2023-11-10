#!/bin/bash

# FOR MACOS AND LINUX; you can use this shell script to help set up the development
# environment for the ORCA ism-app project

# FOR WINDOWS; you can also use this shell script, but you need to use the
# Windows Subsystem for Linux. To install it:
# 1. Open PowerShell or Command Prompt **as an administrator**
# 2. Run this command: wsl --install
# https://learn.microsoft.com/en-us/windows/wsl/install

# Clear the terminal screen.
clear

# Check if Homebrew is installed; if not, prompt the user to install Homebrew or quit.
if ! command -v brew &> /dev/null; then
    read -p "Homebrew is not installed. Enter y to install Homebrew, n to cancel. [y/n]: " yn
    case $yn in
        y | yes ) echo "Installing Homebrew"
                  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)";;
        n | no ) echo "Homebrew is required. Exiting..."
                 exit;;
        * ) echo "Invalid response"
            exit 1
    esac
fi

# Check if Python and pip are installed; if not, prompt to install with Homebrew or quit.
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    read -p "Python or pip is not installed. Enter y to install Python and pip with Homebrew, n to cancel. [y/n]: " yn
    case $yn in
        y | yes ) echo "Installing Python and pip"
                  brew install python;;
        n | no ) echo "Python and pip are required. Exiting..."
                 exit;;
        * ) echo "Invalid response"
            exit 1
    esac
fi

# Check if pyenv is installed; if not, prompt to install with Homebrew or quit.
if ! command -v pyenv &> /dev/null; then
    read -p "pyenv is not installed. Enter y to install pyenv with Homebrew, n to cancel. [y/n]: " yn
    case $yn in
        y | yes ) echo "Installing pyenv"
                  brew install pyenv;;
        n | no ) echo "pyenv is required. Exiting..."
                 exit;;
        * ) echo "Invalid response"
            exit 1
    esac
fi

# Install Python 3.10.12 with pyenv if it's not already installed.
if ! pyenv versions | grep -q "3.10.12"; then
    echo "Python 3.10.12 is not installed. Installing..."
    pyenv install 3.10.12
fi

# Check if requirements.txt exists; if yes, install the requirements.
if [ -f requirements.txt ]; then
    echo "Installing project requirements..."
    pip3 install -r requirements.txt -q || { echo "Requirements installation failed. Please try again."; exit 1; }
else
    echo "requirements.txt not found."
    exit 1
fi

# Activate the pyenv shell 3.10.12 and launch wsgi.py.

echo "Initializing pyenv..."
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.10.12
python wsgi.py --port=5001 --host=localhost --debug