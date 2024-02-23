# League of Legends match downloader

A program written in Python that downloads data for a player's recent matches and stores them locally for analysis. Here is an example of a single match data: [docs/match.json](docs/match.json).

## Setup

### Download the code

```bash
git clone https://github.com/evgenyneu/lolstats.git
```

### Set up Python environment

See [Python setup](docs/python_setup.md).

## Usage

Run `python load.py` to download data for the most recent matches and store them locally. For example:

```bash
python load.py --name=Faker --tag=t1 --region=americas --max=100 --key=your_api_key
```

Where:

  * `--name` and `--tag` are the League of Legends player's name and tag.
  * `--region` is one of `americas`, `asia`, `europe` or `sea`.
  * `--max` is the maximum number of recent matches to download.
  * `--key` is your Riot API key from https://developer.riotgames.com.

Run `python load.py -h` to get the list of all available options.


## Development

See [docs/development.md](docs/development.md).


## Feedback is welcome

If you need help or notice a bug, feel free to create an issue ticket. I will be happy to help. :D


## License

This code is released under the [MIT License](LICENSE).
