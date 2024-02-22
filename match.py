import os
from tqdm import tqdm
from lolstats.http import get_account_puuid, get_list_of_match_ids, get_matches
from lolstats.disk import unsaved_matches, save_matches

# Obtain the API key from Riot Developer Portal https://developer.riotgames.com/
# Important: do not share your api key with anyone!
API_KEY = os.environ['RIOT_API_KEY']

# Set the routing value that is used to make the host name for the HTTP request to Riot API servers.
# It depends on your League of Legends region:
#  * `americas` routing value serves NA, BR, LAN and LAS.
#  * `asia` routing value serves KR and JP. The EUROPE routing value serves EUNE, EUW, TR and RU.
#  * `sea` routing value serves OCE, PH2, SG2, TH2, TW2 and VN2.
# Source: https://developer.riotgames.com/apis#match-v5
MATCH_ROUTE = 'sea'


puuid = get_account_puuid(routing='asia', name='Noct', tag='Noob', api_key=API_KEY)

MATCHES_DIR = f"./matches"
total_matches = 40
batch_size = 20
queue = 420 # 420 is "5v5 Ranked Solo games" (https://static.developer.riotgames.com/docs/lol/queues.json)
total_loaded = 0
total_new = 0

for start in tqdm(range(0, total_matches, batch_size), desc="Loading Matches"):
  match_ids = get_list_of_match_ids(route=MATCH_ROUTE, puuid=puuid, api_key=API_KEY, start=start, count=batch_size, queue=queue)
  total_loaded += len(match_ids)
  new_match_ids = unsaved_matches(directory=MATCHES_DIR, ids=match_ids)
  total_new += len(new_match_ids)
  matches = get_matches(route=MATCH_ROUTE, ids=new_match_ids, api_key=API_KEY)
  save_matches(directory=MATCHES_DIR, matches=matches)

print(f"\n\nLoaded {total_loaded} matches, {total_new} new")

