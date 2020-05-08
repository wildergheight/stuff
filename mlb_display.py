from __future__ import print_function
import mlbgame
from datetime import datetime
from datetime import date
from dateutil.relativedelta import *

game_dict = {}


def getGames():
    current_date = datetime.now()
    # Used until season restarts
    current_date = date.fromisoformat('2019-05-15')
    current_date = datetime.combine(current_date, datetime.min.time())
    current_year = current_date.year
    current_month = current_date.month

    next_month_date = current_date + relativedelta(months=+1)
    next_month = next_month_date.month

    # use current year when season comes back
    month = mlbgame.games(2019, current_month, home='Mets', away='Mets')
    games = mlbgame.combine_games(month)
    key = 0

    game_dict.clear()
    for game in games:
        # s = Game_data()

        diff = game.date - current_date
        diff_days = diff.days
        if diff_days > 0:
            # print(game)
            # print(game.date)
            game_dict.update({key: game})
            key += 1

    # gameid = '2019_05_31_nynmlb_arimlb_1'
    print('Home: {} \nAway: {} \nStatus: {} '.format(game_dict[0].home_team, game_dict[0].away_team,
                                                     game_dict[0].game_status))

    # Eventually do an In-Game check, with game_dict[0] (since that's the closest game to current time

    return game_dict


def writeGames(game_dictionary):
    stuff = game_dictionary
    pass


d = getGames()

pass
