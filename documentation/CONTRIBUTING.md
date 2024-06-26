# Contributing to the ISM Project

This document was made with guidance from [Contributing.md](https://contributing.md) and [GitHub Guidelines for Contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors). It is a living document and should reflect the opinions and needs of the current ORCA ISM team.

1. Coding language(s)
   - Python
2. IDE
   - VSCode, PyCharm
3. Code Style
   - Linter (Flake8?)
   - Norms
     - NetID as a starting comment so we know who created a given function
     - Folder/directory tree for orfganization
     - Including license in the file helps ensure the license remains with the project
   - Testing it helpful, ask someone else to test what you have written
4. Git

   - Protect main - merging/pull requests required
   - Branches
     - Feature/Issue branches
     - One branch for each person
     - Push/pull frequently

5. Making changes/refactoring

   - What is OK to change as needed?
   - What should need a 5-minute review before changing?
   - Modifying other's code/issues
     - How to handle with git?
     - Distribution of work items

6. Working together

   - Working as a pair can often lead to better results
   - Ask for help often, no one is judged for not knowing something

7. Divide and conquer
   - Are you working on what you want to be working on?
   - Are you getting what you want out of this project so far?

## Running locally

These instructions are designed for MacOS & GNU/Linux users.  
**Windows users:** [Using WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux) is recommended.

### Requirements

Install the following tools using their instructions:

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)- Python version manager
- [nvm](https://github.com/nvm-sh/nvm) - Node version manager

### Running locally

**Setup pyenv & nvm**

```sh
# Python
pyenv install # If the version already exists, no need to re-install
# Node.js
nvm install
```

**Install dependencies**

```sh
# Python
pip install -r requirements.txt
# Node.js
corepack install # Sets up npm
npm install
```

**Run the app**

```sh
python wsgi.py --port=5001 --host=localhost --debug
```

Then visit http://localhost:5001
