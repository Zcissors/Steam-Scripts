#!/usr/bin/python
import requests
import json
import time
# -------- change this to who you want
steamid = '76561198023414915'  # St4ck

# ----- dont change this stuff? -----
# -----------------------------------
with open('token.json') as fp:
    token = json.load(fp)
steam_key = token['s-key']

def level(steamid):
    url = requests.get(
        f'https://api.steampowered.com/IPlayerService/GetBadges/v1/',
        params={'key': steam_key, 'steamid': steamid}
    )
    data = url.json()
    data = data['response']
    level = data.get('player_level')
    xp = data.get('player_xp')
    xpup = data.get('player_xp_needed_to_level_up')

    if url.status_code == 500:
        print('smthn broke sorry')
    elif url.status_code == 200:
        print(f'{steamid} |||| Level: {level:,} || Current XP: {xp:,} '
              f'|| Badges left to next level: {xpup // 100}')

print(time.ctime())
while True:
    level(steamid)
