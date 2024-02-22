import os

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

# import sys
# from tqdm import tqdm
# from google.colab import drive
# drive.mount('/content/drive')

# project_path = '/content/drive/MyDrive/Colab Notebooks'
# sys.path.append(project_path)

from http import get_account_puuid

# puuid = get_account_puuid(routing='asia', name='Noct', tag='Noob', api_key=API_KEY)
