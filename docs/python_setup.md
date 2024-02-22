# Setup Python environment

This is how to install python and libraries needed to run the code in this repository.

## Install Python

* Install pyenv by following the [setup instructions from pyenv GitHub page](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

* Run `pyenv install` in the root of this project to install Python version specified in [.python-version](/.python-version).


## Create and active Python environment

* Run `python -m venv .venv` to create local Python environment.

* Activate the environment: `source .venv/bin/activate`.

## Install Python libraries

Run `pip install -r requirements.txt` to install required libraries.
