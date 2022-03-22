import requests
import json
from datetime import datetime
from datetime import timedelta
from termcolor import colored
import time

current_date = datetime.utcnow()
url = 'https://statsapi.web.nhl.com'
game_dict = {}
nyr = 3

team_dict = {1: ['NJD', [200, 16, 46], [0, 0, 0]], 2: ['NYI', [0, 48, 135], [252, 76, 2]],
             3: ['NYR', [0, 57, 166], [204, 9, 47]], 4: ['PHI', [253, 67, 0], [0, 0, 0]],
             5: ['PIT', [255, 200, 12], [4, 7, 7]], 6: ['BOS', [253, 185, 39], [0, 0, 0]],
             7: ['BUF', [0, 45, 98], [253, 187, 48]], 8: ['MTL', [0, 30, 98], [166, 25, 46]],
             9: ['OTT', [228, 23, 62], [214, 159, 15]], 10: ['TOR', [0, 56, 118], [255, 255, 255]],
             12: ['CAR', [225, 58, 62], [35, 31, 32]], 13: ['FLA', [4, 30, 66], [200, 16, 46]],
             14: ['TBL', [0, 62, 126], [255, 255, 255]], 15: ['WSH', [0, 33, 77], [207, 19, 43]],
             16: ['CHI', [97, 170, 0], [209, 0, 27]], 17: ['DET', [200, 16, 46], [255, 255, 255]],
             18: ['NSH', [8, 55, 99], [251, 189, 44]], 19: ['STL', [4, 71, 160], [255, 195, 37]],
             20: ['CGY', [212, 38, 4], [251, 198, 2]], 21: ['COL', [139, 41, 66], [0, 84, 136]],
             22: ['EDM', [0, 32, 91], [207, 69, 32]], 23: ['VAN', [0, 46, 86], [0, 62, 126]],
             24: ['ANA', [252, 76, 2], [133, 113, 77]], 25: ['DAL', [0, 99, 65], [138, 141, 143]],
             26: ['LAK', [177, 181, 182], [0, 0, 0]], 28: ['SJS', [0, 110, 127], [0, 0, 0]],
             29: ['CBJ', [1, 38, 91], [223, 57, 61]], 30: ['MIN', [1, 88, 54], [191, 43, 55]],
             52: ['WPG', [0, 46, 98], [129, 1, 32]], 53: ['ARI', [137, 34, 47], [223, 203, 160]],
             54: ['VGK', [135, 112, 78], [51, 64, 73]]}


class Game_data:
    def __init__(self):
        self.game = 0
        self.gameid = 0
        self.gamedate = 0
        self.awayid = 0
        self.homeid = 0
        self.opp_record = []
        self.games_played = 0
        # self.away_score = 0
        # self.home_score = 0
        self.opponent = 0


current_d = datetime.now()


def getStandings():
    # current_date = datetime.utcnow()
    standings = 'https://statsapi.web.nhl.com/api/v1/standings'
    response = requests.get(standings)
    standings_get = json.loads(response.text)
    for x in range(8):
        print(' ')
    print('                            GP Pts  W L OTL')
    for x in range(8):
        teamname = standings_get['records'][0]['teamRecords'][x]['team']['name']
        teamrecord_wins = standings_get['records'][0]['teamRecords'][x]['leagueRecord']['wins']
        teamrecord_losses = standings_get['records'][0]['teamRecords'][x]['leagueRecord']['losses']
        teamrecord_ot = standings_get['records'][0]['teamRecords'][x]['leagueRecord']['ot']
        teamrecord_points = standings_get['records'][0]['teamRecords'][x]['points']
        teamstreak = standings_get['records'][0]['teamRecords'][x]['streak']['streakCode']
        games_played = teamrecord_ot + teamrecord_losses + teamrecord_wins
        if teamname == "New York Rangers":
            print('  {0:25}          {6:2}  {1:2}, {2:2},{3:2},{4:2}   {5:3}'.format(colored(teamname, 'green'), teamrecord_points,
                                                                            teamrecord_wins,
                                                                            teamrecord_losses, teamrecord_ot,
                                                                            teamstreak, games_played))
        else:
            print('  {0:25} {6:2}  {1:2}, {2:1},{3:1},{4:1}   {5:3}'.format(teamname, teamrecord_points, teamrecord_wins,
                                                                 teamrecord_losses, teamrecord_ot, teamstreak, games_played))


def getSchedule():
    # Things to add:
    # Obviously display stuff
    # Other info per team, maybe current record or place in division/conf
    # Countdown to next game
    # Possibly some info on previous games (if there's space)
    # Rangers current record

    game_dict.clear()
    future_d = current_d + timedelta(days=30)
    current_d_str = datetime.strftime(current_d, '%Y-%m-%d')
    future_d_str = datetime.strftime(future_d, '%Y-%m-%d')
    schedule = '/api/v1/schedule?teamId=3&startDate=' + current_d_str + '&endDate=' + future_d_str
    # schedule = '/api/v1/schedule?teamId=3&startDate=' + '2019-03-1' + '&endDate=' + '2019-03-30'

    # current season (and future dates) once the season comes back

    response = requests.get(url + schedule)

    schedule_get = json.loads(response.text)
    # date = ''
    sports_out = []
    sports = ''
    total_games = schedule_get['totalGames']
    upcoming = 5  # grab next 5 games
    if total_games <= 4:
        upcoming = total_games
    # current_date = datetime.utcnow()  # continue getting current time
    d = ''
    for i in range(0, upcoming):  # Grab upcoming 5 games
        s = Game_data()
        s.game = i
        s.gamelink = schedule_get['dates'][i]['games'][0]['link']
        d = schedule_get['dates'][i]['games'][0]['gameDate']
        date = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
        date = date - timedelta(hours=7)
        s.gamedate = date.strftime('%m/%d %I:%M %p')
        s.awayid = schedule_get['dates'][i]['games'][0]['teams']['away']['team']['id']
        s.homeid = schedule_get['dates'][i]['games'][0]['teams']['home']['team']['id']

        # s.away_score = schedule_get['dates'][i]['games'][0]['teams']['away']['score']
        # s.home_score = schedule_get['dates'][i]['games'][0]['teams']['home']['score']
        if s.awayid == 3:
            # s.opponent = team_dict[s.homeid][0]
            s.opponent = "@" + schedule_get['dates'][i]['games'][0]['teams']['home']['team']['name']
            s.opp_record = [schedule_get['dates'][i]['games'][0]['teams']['home']['leagueRecord']['wins'],
                            schedule_get['dates'][i]['games'][0]['teams']['home']['leagueRecord']['losses'],
                            schedule_get['dates'][i]['games'][0]['teams']['home']['leagueRecord']['ot']]
            s.games_played = sum(s.opp_record)
        else:
            # s.opponent = team_dict[s.awayid][0]
            s.opponent = schedule_get['dates'][i]['games'][0]['teams']['away']['team']['name']
            s.opp_record = [schedule_get['dates'][i]['games'][0]['teams']['away']['leagueRecord']['wins'],
                            schedule_get['dates'][i]['games'][0]['teams']['away']['leagueRecord']['losses'],
                            schedule_get['dates'][i]['games'][0]['teams']['away']['leagueRecord']['ot']]
            s.games_played = sum(s.opp_record)
        game_dict[i] = s

    # difference_in_time = game_dict[0].gamedate - current_date
    # difference_in_days = difference_in_time.days
    # if difference_in_days == 0:
    #     if (abs(difference_in_time.seconds) / 3600) <= 2:
    #         inGame(game_dict[0].gameid, game_dict[0].opponent_id)

    # sports += sports_out[0]
    # sports += ' ' + sports_out[1]
    # sports += ' ' + sports_out[2]
    # sports += ' ' + sports_out[3]
    # sports += ' ' + sports_out[4]

    # print(sports_out)
    # print(sports)
    # print('{0}'.format(team_dict[game_dict[0].opponent][0]))
    # # print(team_dict[game_dict[0].opp_record][0])
    # print('{0}'.format(team_dict[game_dict[1].opponent][0]))
    # print('{0}'.format(team_dict[game_dict[2].opponent][0]))
    # print('{0}'.format(team_dict[game_dict[3].opponent][0]))
    # print('{0}'.format(team_dict[game_dict[4].opponent][0]))


# if next gametime is same as current time (or within say 2 hours post) switch to in game mode function

# def inGame(game_link, opp_id):
#     # Things to add:
#     # Obviously display stuff
#     # Goal celebration (or maybe something negative if opposing, using goalScored function)
#     # PP/PK implementation
#     # Maybe pulled goalie? API has implementation
#     # Track SOG
#     # Intermission info (time remaining)
#
#     prev_goal_h = 0
#     prev_goal_a = 0
#
#     while True:
#         # timer_start = time.perf_counter()
#         game_response = requests.get(url + str(game_link))
#         game_get = json.loads(game_response.text)
#         game_over_check = game_get['gameData']['status']['abstractGameState']
#
#         # if game_over_check == 'Final':  # If the game is over, wait half and hour, then end the function
#         #     # time.sleep(1800)  #inactive for testing, re-enable when using for real
#         #     return
#         opp = opp_id
#         current_period = game_get['liveData']['linescore']['currentPeriod']
#         time_remaining = game_get['liveData']['linescore']['currentPeriodTimeRemaining']
#         home_score = game_get['liveData']['linescore']['teams']['home']['goals']
#         if home_score != prev_goal_h:
#             goalScored(game_get, opp, 1)
#             prev_goal_h = home_score
#         away_score = game_get['liveData']['linescore']['teams']['away']['goals']
#         if away_score != prev_goal_a:
#             goalScored(game_get, opp, 0)
#             prev_goal_a = away_score
#
#         time.sleep(.5)  # delay repeating function half a second to avoid hammering the api too much
#         # timer_finish = time.perf_counter()
#         # print(timer_finish - timer_start) # Check how long the repeating function takes, change sleep time accordingly


# def goalScored(game, opp_id, home_away_scored):
#     # Things to add:
#     # Obviously display stuff
#     # Scorer, assisted by possibly
#
#     if home_away_scored == 1:
#         if game['liveData']['linescore']['teams']['home']['team']['id'] == 3:
#             # do rangers scored thing
#             print(team_dict[nyr][0])
#         else:
#             # do opp_id scored thing
#             print(team_dict[opp_id][0])
#     else:
#         if game['liveData']['linescore']['teams']['away']['team']['id'] == 3:
#             # do rangers scored thing
#             print(team_dict[nyr][0])
#         else:
#             # do opp_id scored thing
#             print(team_dict[opp_id][0])
#             print(team_dict[opp_id][1][0])

getStandings()
print(" ")
print("  Upcoming Schedule")
print(" ")
getSchedule()
print('  {0:25} {4:5} ({1:1},{2:1},{3:1}) '.format(game_dict[0].opponent, game_dict[0].opp_record[0],
                                                 game_dict[0].opp_record[1], game_dict[0].opp_record[2],
                                                 game_dict[0].gamedate))
print('  {0:25} {4:5} ({1:1},{2:1},{3:1}) '.format(game_dict[1].opponent, game_dict[1].opp_record[0],
                                                 game_dict[1].opp_record[1], game_dict[1].opp_record[2],
                                                 game_dict[1].gamedate))
print('  {0:25} {4:5} ({1:1},{2:1},{3:1}) '.format(game_dict[2].opponent, game_dict[2].opp_record[0],
                                                 game_dict[2].opp_record[1], game_dict[2].opp_record[2],
                                                 game_dict[2].gamedate))
print('  {0:25} {4:5} ({1:1},{2:1},{3:1}) '.format(game_dict[3].opponent, game_dict[3].opp_record[0],
                                                 game_dict[3].opp_record[1], game_dict[3].opp_record[2],
                                                 game_dict[3].gamedate))
print('  {0:25} {4:5} ({1:1},{2:1},{3:1}) '.format(game_dict[4].opponent, game_dict[4].opp_record[0],
                                                 game_dict[4].opp_record[1], game_dict[4].opp_record[2],
                                                 game_dict[4].gamedate))

print(" ")
print(" ")

# current_d = datetime(2019, 2, 13)
# getSchedule()
pass
# inGame(game_dict[0].gamelink, game_dict[0].opponent)  # for testing, will be called in the schedule function
