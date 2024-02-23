# Setup Python environment

Here's how to install Python and the necessary libraries to run the code in this repository.


## Install Python

* Install pyenv by following [these setup instructions](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

* Run `pyenv install` at the root of this project to install the Python version specified in the  [.python-version](/.python-version).


## Activate Python environment

* Run `python -m venv .venv` to create a local Python environment.

* Activate the environment: `source .venv/bin/activate`.


## Install libraries

Run `pip install -r requirements.txt` to install the required Python libraries.
