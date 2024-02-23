"""Load League of Legends match data for the player from Riot API and store it into disk."""

import argparse
import sys
from lolstats.matches import load_matches
from lolstats.errors import MyError


def parse_args():
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description="Load League of Legends match data for the player from Riot API and store it into disk."
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help=("Player name portion in Name#Tag"),
        required=True,
    )
    parser.add_argument(
        "-t",
        "--tag",
        type=str,
        help=("Player tag portion in Name#Tag"),
        required=True,
    )

    parser.add_argument("-k", "--key", type=str, help=("Riot API key"), required=True)

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to directory where matches are stored",
        default="data",
    )

    parser.add_argument(
        "-m", "--max", type=int, help="Maximum number of matches to load", default=40
    )

    parser.add_argument(
        "-q",
        "--queue",
        type=int,
        help="Game queue type. Example: 420 for Ranked solo queue: https://static.developer.riotgames.com/docs/lol/queues.json",
        default=None,
    )

    parser.add_argument(
        "-r",
        "--region",
        type=str,
        help=(
            "Region: "
            " 'americas' for NA, BR, LAN and LAS,"
            " 'asia' for KR and JP, "
            " 'europe' for EUNE, EUW, TR and RU,"
            " 'sea' for OCE, PH2, SG2, TH2, TW2 and VN2."
        ),
    )

    return parser.parse_args()


def main():
    """Parse command line arguments and load matches."""

    try:
        args = parse_args()

        result = load_matches(
            directory=args.output,
            total_matches=args.max,
            route=args.region,
            name=args.name,
            tag=args.tag,
            queue=args.queue,
            api_key=args.key,
        )

        print(
            (
                f"\n\nSuccessfully loaded match data into '{args.output}' directory.\n"
                f"{result['total']} total matches, {result['new']} new."
            )
        )
    except MyError as e:
        print("\n\nError:\n")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
