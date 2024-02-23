# Setup Python environment

Here's how to install Python and the necessary libraries to run the code in this repository.

## Install Python

### Windows

Install Python from Microsoft Store, version closer to [.python-version](/.python-version).

### MacOS/Linux

* Install pyenv by following [these setup instructions](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

* Run `pyenv install` at the root of this project to install the Python version specified in the  [.python-version](/.python-version).


## Activate Python environment

### Windows

* Open PowerShell.
* Run `python -m venv .venv` to create a local Python environment.
* Allow scripts to run: `Set-ExecutionPolicy Unrestricted -Scope Process`
* Activate the environment: `.venv\Scripts\activate`.

### MacOS/Linux

* Run `python -m venv .venv` to create a local Python environment.
* Activate the environment: `source .venv/bin/activate`.

## Install libraries

Run `pip install -r requirements.txt` to install the required Python libraries.
