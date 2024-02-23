"""Load data from Riot API"""

import time
import requests
from .errors import MyError, HttpError


def send_get_request(url, max_retries=8, retry_delay=10):
    """
    Send a GET request to a specified URL.

    Parameters
    ----------
    url : str
      The URL to which the GET request is sent.

    max_retries : int
      Number of times the HTTP request is retried when Riot server returns
      HTTP error 429 Rate limit exceeded.
      Riot API has request limit of 100 requests per two minutes.

    retry_delay : int
      Delay before the next retried HTTP request in seconds. For
      each subsequent request the delay is doubled.

    Returns
    -------
    dict
      The JSON response from the server if the request is successful.

    Raises
    ------
    Exception
      If the request fails, an exception is raised with the error message.
    """

    attempts = 0

    while attempts < max_retries:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise MyError(
                "401 Unauthorized. Your API key is missing or incorrect. "
                "Regenerate a new key from https://developer.riotgames.com/."
            )
        elif response.status_code == 403:
            raise MyError(
                "403 Forbidden. Your API key has expired. "
                "Regenerate a new key from https://developer.riotgames.com/."
            )
        elif response.status_code == 429:
            time.sleep(retry_delay)
            retry_delay *= 2  # Double the delay for the next retry
            attempts += 1
        else:
            raise HttpError(
                f"{response.status_code} {response.reason}", response.status_code
            )

    # If the loop exits without returning or raising for status 200, it means max retries were reached.
    raise MyError("Max retries exceeded.")


def get_account_puuid(routing, name, tag, api_key):
    """
    Returns player's identified PUUID given their in-game name.

    Parameters
    ----------
    routing : str
      The protion of the HTTP request hostname.
      There are three routing values for account-v1: americas, asia, and europe.
      You can query for any account in any region. We recommend using the nearest cluster.
      Source: https://developer.riotgames.com/apis#account-v1/

    name : str
        Gamer name part from Riot ID: Name#Tag

    tag : str
        Gamer tag line part from Riot ID: Name#Tag

    api_key : str
        Riot API key.

    Returns
    -------
    str
      Player's PUUID
    """

    try:
        url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}"
        data = send_get_request(url)
        return data["puuid"]

    except HttpError as e:
        if e.status_code == 404:
            raise MyError(
                f"Player {name}#{tag} not found. Check if the name and tag are correct."
            ) from e

        raise


def get_list_of_match_ids(
    route, puuid, api_key, start=0, count=20, end_time=None, queue=None
):
    """
    Returns list of match ids.

    Parameters
    ----------
    route : str
      Match region used in HTTP request hostname:
        * `americas` for NA, BR, LAN and LAS.
        * `asia` for KR and JP.
        * `europe` for EUNE, EUW, TR and RU.
        * `sea` for OCE, PH2, SG2, TH2, TW2 and VN2.
      Source: https://developer.riotgames.com/apis#match-v5

    puuid : str
      Player's unique identifier.

    api_key : str

    start: int, optional
      Start index.

    count: int, optional
      Number of match ids to return. Valid values: 0 to 100.

    end_time: int, optional
      The UNIX timestamp in seconds for the end of time range.
      Matched that finish before this time will be included.

    queue: int, optional
      Game queue type. See https://static.developer.riotgames.com/docs/lol/queues.json.
      Example: 420 is "5v5 Ranked Solo games".

    Returns
    -------
    list
      List of match IDs.
    """

    url = (
        f"https://{route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        f"?api_key={api_key}"
        f"&start={start}"
        f"&count={count}"
        f"&endTime={end_time or ''}"
        f"&queue={queue or ''}"
    )

    return send_get_request(url)


def get_match(route, id, api_key):
    """
    Return match data.

    Parameters
    ----------
    route : str
      See get_list_of_match_ids.

    id : str
      Match id.

    api_key : str

    Returns
    -------
    dict
      Match data (see https://developer.riotgames.com/apis#match-v5/GET_getMatch).
    """

    url = (
        f"https://{route}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={api_key}"
    )
    return send_get_request(url)


def get_matches(route, ids, api_key):
    """
    Loads match data from Riot API.

    Parameters
    ----------
    route : str
      See get_list_of_match_ids.

    ids : list
      List of match IDs.

    api_key : str

    Returns
    -------
    list of dict
      List of match data (see https://developer.riotgames.com/apis#match-v5/GET_getMatch).
    """

    return [get_match(route=route, id=id, api_key=api_key) for id in ids]
