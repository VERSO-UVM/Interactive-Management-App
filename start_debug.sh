#!/bin/bash

# FOR MACOS AND LINUX; you can use this shellscript to help setup the development
# environment for the ORCA ism-app project

# FOR WINDOWS; you can also use this shellscript, but you need to use the
# Windows Subsystem for Linux. To install it:
# 1. Open PowerShell or Command Prompt **as an administrator**
# 2. Run this command: wsl --install

# https://learn.microsoft.com/en-us/windows/wsl/install


clear

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.10.12

flask run -h localhost -p 5000 --debug
