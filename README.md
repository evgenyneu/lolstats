# League of Legends match data analysis tools

A program written in Python that loads player's match data and stores it locally for analysis.

## Download this repository

```bash
git clone https://github.com/evgenyneu/lolstats.git
```

## Setup Python environment

See [Python setup](docs/python_setup.md).

## Usage

Run `python load.py` to download player's match data and store it locally. For example:

```bash
python load.py --name=Faker --tag=t1 --region=americas --max=100 --key=your_api_key
```

Where
  * `--name` and `--tag` are the League of Legends player's name and tag,
  * `--max` is the maximum number of matches to download,
  * `--region` is the region,
  * `--key` is your Riot API key from https://developer.riotgames.com/.

Run `python load.py -h` to get the list of all available options.


## Development

VSCode extensions:

* [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
* [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)


## Feedback is welcome

If you need help or notice a bug feel free to create an issue ticket. I will be happy to help you.


## License

Keychain Swift is released under the [MIT License](LICENSE).
