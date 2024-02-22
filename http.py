"""Load data from Riot API"""

import requests
import time

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
    response = requests.get(url)

    if response.status_code == 200:
      return response.json()
    elif response.status_code == 403:
      raise Exception(
        '403 - Forbidden. Your API key is incorrect or expired. '
        'Visit https://developer.riotgames.com/, regenerate your API key and '
        'assign it to API_KEY variable.'
      )
    elif response.status_code == 429:
      print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
      time.sleep(retry_delay)
      retry_delay *= 2  # Double the delay for the next retry
      attempts += 1
    else:
      error_message = f"Request error {response.status_code} - {response.reason}"
      raise Exception(error_message)

  # If the loop exits without returning or raising for status 200, it means max retries were reached.
  raise Exception("Max retries exceeded.")


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

  tag : str
    In-game Name#Tag

  api_key : str

  Returns
  -------
  str
    Player's PUUID
  """

  url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}"
  data = send_get_request(url)
  return data['puuid'];


def get_list_of_match_ids(route, puuid, api_key, start=0, count=20, end_time=None, queue=None):
  """
  Returns list of match ids.

  Parameters
  ----------
  route : str
    The protion of the HTTP request hostname:
      * `americas` routing value serves NA, BR, LAN and LAS.
      * `asia` routing value serves KR and JP. The EUROPE routing value serves EUNE, EUW, TR and RU.
      * `sea` routing value serves OCE, PH2, SG2, TH2, TW2 and VN2.
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
    Queue types (draft, raked etc.). See https://static.developer.riotgames.com/docs/lol/queues.json. Example, 420 is "5v5 Ranked Solo games".

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
    See get_list_of_matche_ids.

  id : str
    Match id.

  api_key : str

  Returns
  -------
  dict
    Match data (see https://developer.riotgames.com/apis#match-v5/GET_getMatch).
  """

  url = f"https://{route}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={api_key}"
  return send_get_request(url)


def get_matches(route, ids, api_key):
  """
  Loads match data from Riot API.

  Parameters
  ----------
  route : str
    See get_list_of_matche_ids.

  ids : list
    List of match IDs.

  api_key : str

  Returns
  -------
  list of dict
    List of match data (see https://developer.riotgames.com/apis#match-v5/GET_getMatch).
  """

  return [
      get_match(route=route, id=id, api_key=api_key)
      for id in ids
    ]