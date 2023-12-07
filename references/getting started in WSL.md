# Getting started in WSL #

1. Open PowerShell
2. `wsl` to login to WSL
3. `cd ~/` to go to the home directory
4. `cd` to the project folder (same one with app.py inside of it)
5. `code .` to open in VSCode (you must have the WSL extension installed)
6. `./start_debug.sh` to start the application
    1. If you get an error: "bad interpreter...", fix using:
        `sed -i -e 's/\r$//' scriptname.sh`
