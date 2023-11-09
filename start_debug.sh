#!/bin/bash

# FOR MACOS AND LINUX; you can use this shellscript to help setup the development
# environment for the ORCA ism-app project

# FOR WINDOWS; you can also use this shellscript, but you need to use the
# Windows Subsystem for Linux. To install it:
# 1. Open PowerShell or Command Prompt **as an administrator**
# 2. Run this command: wsl --install

# https://learn.microsoft.com/en-us/windows/wsl/install


clear

# If you are using Pyenv, uncomment the below lines to use pyenv.
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.10.12

# If you are using a venv, uncomment the line below.
# source venv/bin/activate

python wsgi.py --port=5001 --host=localhost --debug
