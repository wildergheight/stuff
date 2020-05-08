from __future__ import print_function
import mlbgame
from datetime import datetime
from datetime import date
from dateutil.relativedelta import *
from os import system, name
import time

game_dict = {}


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def getGames():
    current_date = datetime.now()
    # Used until season restarts
    # current_date = date.fromisoformat('2019-05-02')
    # current_date = datetime.combine(current_date, datetime.min.time())
    current_year = current_date.year
    current_month = current_date.month

    next_month_date = current_date + relativedelta(months=+1)
    next_month = next_month_date.month

    # use current year when season comes back
    month = mlbgame.games(2020, current_month, home='Mets', away='Mets')
    games = mlbgame.combine_games(month)
    key = 0

    game_dict.clear()
    for game in games:
        # s = Game_data()

        diff = game.date - current_date
        diff_days = diff.days
        if key == 10:
            break
        elif diff_days > 0:
            # print(game)
            # print(game.date)
            game_dict.update({key: game})
            key += 1

    # gameid = '2019_05_31_nynmlb_arimlb_1'

    # Eventually do an In-Game check, with game_dict[0] (since that's the closest game to current time

    return game_dict


def writeGames(game_dictionary):
    current_date = datetime.now()
    # current_date = date.fromisoformat('2019-05-02')
    # current_date = datetime.combine(current_date, datetime.min.time())
    for game in game_dictionary:

        diff = game_dictionary[game].date - current_date

        diff_days = diff.days

        if game_dictionary[game].home_team == 'Mets':
            print('{0:10} P - {1:9} T-{2:2} {3}'.format(game_dictionary[game].away_team,
                                                        game_dictionary[game].p_pitcher_home, diff_days,
                                                        game_dictionary[game].game_start_time))
        else:
            print('{0:10} P - {1:9} T-{2:2} {3}'.format(game_dictionary[game].home_team,
                                                        game_dictionary[game].p_pitcher_away, diff_days,
                                                        game_dictionary[game].game_start_time))


init_time = time.perf_counter()
d = getGames()
while True:

    clear()
    writeGames(d)
    current_time = time.perf_counter()
    if current_time - init_time > 3600:
        d = getGames()
