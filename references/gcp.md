# setup and configure the google cloud  host #

## Configuring the VM ##

I used the cheapest settings possible. Make sure to enable spot VM.

### setting up ssh login via remote machine/openSSH terminal ###
TODO

Steps:
1. `sudo apt update && apt upgrade`
2. Python build essentials
    `
    sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm 
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    `
3. git `curl https://pyenv.run | bash`
4. pyenv ` sudo curl https://pyenv.run | bash`
    1. `export PATH="$HOME/.pyenv/bin:$PATH" &&
        eval "$(pyenv init --path)" &&
        eval "$(pyenv virtualenv-init -)"`
    2. `exec $SHELL`

5. Install the python version for the project. At time of writing it is 3.10.0
    1. `pyenv install 3.10.0`