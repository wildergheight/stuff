import requests
import json
from datetime import datetime
from datetime import timedelta
import time

current_date = datetime.utcnow()
standings = 'https://statsapi.web.nhl.com/api/v1/standings'
response = requests.get(standings)
standings = json.loads(response.text)
for x in range(8):
    print(' ')
print('                           Pts   W  L  OTL')
for x in range(7):
    teamname = schedule_get['records'][0]['teamRecords'][x]['team']['name']
    teamrecord_wins = schedule_get['records'][0]['teamRecords'][x]['leagueRecord']['wins']
    teamrecord_losses = schedule_get['records'][0]['teamRecords'][x]['leagueRecord']['losses']
    teamrecord_ot = schedule_get['records'][0]['teamRecords'][x]['leagueRecord']['ot']
    teamrecord_points = schedule_get['records'][0]['teamRecords'][x]['points']
    teamstreak = schedule_get['records'][0]['teamRecords'][x]['streak']['streakCode']
    print('  {0:25} {1:2}, {2:2},{3:2},{4:2}   {5:3}'.format(teamname, teamrecord_points, teamrecord_wins, teamrecord_losses, teamrecord_ot, teamstreak))