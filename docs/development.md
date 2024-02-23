# Development

## Run unit tests

From PowerShell (Windows) or Terminal (macOS/Linux), run from the root directory of the project:

```bash
pytest
```

## Adding new Python libraries

1. Add the library name to the `requirements.in` file.

1. Run `pip-compile requirements.in` to update the `requirements.txt` file.

1. Run `pip install -r requirements.txt` to install the new dependencies.

## VS Code extensions

This project uses the following VS Code extensions to maintain consistent code style and formatting:

* [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)

* [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
