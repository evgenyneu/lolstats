"""Loads match data from Riot API and saves them to disk."""

from tqdm import tqdm
import os
from lolstats.lol_http import get_account_puuid, get_list_of_match_ids, get_matches
from lolstats.disk import unsaved_matches, save_matches, save_player


def load_matches(directory, total_matches, route, name, tag, api_key, queue=None):
    """
    Load multiple matches and save them to directory as JSON files.

    Parameters
    ----------
    directory : str
        Path to directory where the matches are saved.

    total_matches : int
        Maximum number of matches to load, starting from the most recent match.

    route : str
        Match region used in HTTP request hostname:
            * `americas` for NA, BR, LAN and LAS.
            * `asia` for KR and JP.
            * `europe` for EUNE, EUW, TR and RU.
            * `sea` for OCE, PH2, SG2, TH2, TW2 and VN2.
        Source: https://developer.riotgames.com/apis#match-v5

    name : str
        Gamer name from Riot ID: Name#Tag

    tag : str
        Gamer tag line from Riot ID: Name#Tag

    queue: int, optional
        Game queue type. See https://static.developer.riotgames.com/docs/lol/queues.json.
        Example: 420 is "5v5 Ranked Solo games".
        When None, games from all queues are included.

    api_key : str
        Riot API key.
    """
    puuid = get_account_puuid(routing="asia", name=name, tag=tag, api_key=api_key)
    save_player(name=name, tag=tag, puuid=puuid, directory=directory)
    batch_size = 20
    total_loaded = 0
    total_new = 0

    for start in tqdm(range(0, total_matches, batch_size), desc="Loading matches"):
        count = min(batch_size, total_matches - start)

        if count <= 0:
            break

        match_ids = get_list_of_match_ids(
            route=route,
            puuid=puuid,
            api_key=api_key,
            start=start,
            count=count,
            queue=queue,
        )

        total_loaded += len(match_ids)
        match_dir = os.path.join(directory, "matches")
        new_match_ids = unsaved_matches(directory=match_dir, ids=match_ids)
        total_new += len(new_match_ids)
        matches = get_matches(route=route, ids=new_match_ids, api_key=api_key)
        save_matches(directory=match_dir, matches=matches)

    return {"total": total_loaded, "new": total_new}
