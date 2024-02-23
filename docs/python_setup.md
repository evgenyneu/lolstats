# Setup Python environment

Here's how to install Python and the necessary libraries to run the code in this repository.

## Install Python

### Windows

Install Python from the Microsoft Store, using the version specified in [.python-version](/.python-version) (or the closest available version).

### macOS/Linux

* Install `pyenv` by following [these setup instructions](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

* At the root directory of this project, run `pyenv install` to install the Python version specified in the  [.python-version](/.python-version).


## Activate Python environment

Execute the following commands from the root directory of the project.

### Windows

* In PowerShell, run `python -m venv .venv` to create a local Python environment.
* Allow scripts to run: `Set-ExecutionPolicy Unrestricted -Scope Process`
* Activate the environment: `.venv\Scripts\activate`.

### macOS/Linux

* Run `python -m venv .venv` to create a local Python environment.
* Activate the environment: `source .venv/bin/activate`.

## Install libraries

Run `pip install -r requirements.txt` to install the required Python libraries.
