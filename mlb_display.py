from __future__ import print_function
import statsapi
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import *
from os import system, name
import time
import calendar

game_diction = {}


class Static:
    def __init__(self):
        pass

    teamname = 'San Diego Padres' #135, Mets - 121
    end_game = False


def getGames(game_dict):
    current_date = datetime.now()
    # Used until season restarts
    # current_date = date.fromisoformat('2019-05-02')
    # current_date = datetime.combine(current_date, datetime.min.time())
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    yesterday = (current_date + relativedelta(days=-1)).day

    start_date = str(current_month) + '/' + str(yesterday) + '/' + str(current_year)
    next_month_date = current_date + relativedelta(months=+1)
    next_month = next_month_date.month
    days_in_next_month = calendar.monthrange(current_year, next_month)[1]
    end_date = str(next_month) + '/' + str(days_in_next_month) + '/' + str(current_year)
    # use current year when season comes back
    month = statsapi.schedule(start_date=start_date, end_date=end_date, team=135)
    # month2 = statsapi.schedule(current_year, next_month, team=Static.teamname, opponent=Static.teamname)

    # games_future_month = mlbgame.combine_games(month2)
    games = month
    key = 0

    game_dict.clear()
    for game in games:
        # s = Game_data()
        game_date = game['game_datetime']
        game_date_datetime = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ" )
        diff = game_date_datetime - current_date
        diff_days = diff.days
        diff_seconds = diff.seconds
        if key == 10:
            break
        elif diff_days > -2 or (diff_days == 0 and diff_seconds > 0):
            # print(game)
            # print(game.date)
            game_dict.update({key: game})
            key += 1
    # if key != 10:  # Less than 10 games left in current month
    #     for game in games_future_month:
    #         # s = Game_data()
    #
    #         diff = game.date - current_date
    #         diff_days = diff.days
    #         diff_seconds = diff.seconds
    #         if key == 10:
    #             break
    #         elif diff_days > -2 or (diff_days == 0 and diff_seconds > 0):
    #             # print(game)
    #             # print(game.date)
    #             game_dict.update({key: game})
    #             key += 1
    # gameid = '2019_05_31_nynmlb_arimlb_1'

    # Eventually do an In-Game check, with game_dict[0] (since that's the closest game to current time

    return game_dict


def writeGames(game_dictionary):
    game_live = False
    current_date = datetime.now()
    current_date = current_date + timedelta(hours=3)
    # current_date = date.fromisoformat('2019-05-02')
    # current_date = datetime.combine(current_date, datetime.min.time())
    for game in game_dictionary:
        if game_dictionary[game]['status'] == 'In Progress':
            game_live = True

    for game in game_dictionary:
        game_date_datetime = datetime.strptime(game_dictionary[game]['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
        diff = game_date_datetime - current_date

        diff_days = diff.days
        if game_dictionary[game]['status'] == 'In Progress':

            game_link = game_dictionary[game]['game_id']
            current_game = statsapi.get('game', {'gamePk':game_link})
            current_in = current_game['liveData']['linescore']['currentInning']
            if current_game['liveData']['linescore']['isTopInning']:
                top_or_bottom = 'T'  # Top of inning


            else:
                top_or_bottom = 'B'  # Bottom of inning


            current_outs = current_game['liveData']['linescore']['outs']
            current_balls = current_game['liveData']['linescore']['balls']
            current_strikes = current_game['liveData']['linescore']['strikes']
            if current_game['gameData']['status']['detailedState'] != "In Progress" or current_game['gameData']['status']['detailedState'] != "Pre-Game":
                Static.end_game = True
            # if current_in >= 9:
            #     if current_outs == 3:
            #         if current_event.away_team_runs < current_event.home_team_runs:
            #             if top_or_bottom == 'T':
            #                 Static.end_game = True
            #         elif current_event.away_team_runs != current_event.home_team_runs:
            #             if top_or_bottom == 'B':
            #                 Static.end_game = True
            #     elif top_or_bottom == 'B' and current_event.home_team_runs > current_event.away_team_runs:
            #         Static.end_game = True

            if game_dictionary[game]['home_name'] == Static.teamname:
                print('{0:10}{1:2}  {6:10} {2:2} {3:1}{4:2} {5:1} Out/s'.format(game_dictionary[game]['away_name'],
                                                                                current_game['liveData']['linescore']['teams']['away']['runs'],
                                                                                current_game['liveData']['linescore']['teams']['home']['runs'],
                                                                                top_or_bottom, str(current_in),
                                                                                current_outs,
                                                                                game_dictionary[game]['home_name']))

            else:

                print('{6:10} {0:2}  {1:10} {2:2}  {3:1}{4:2} {5:1} Out/s'.format(current_game['liveData']['linescore']['teams']['away']['runs'],
                                                                                  game_dictionary[game]['home_name'],
                                                                                  current_game['liveData']['linescore']['teams']['home']['runs'],
                                                                                  top_or_bottom, str(current_in),
                                                                                  current_outs,
                                                                                  game_dictionary[game]['away_name']))
        elif game_dictionary[game]['status'] == 'Final':
            if not game_live:
                final_score = game_dictionary[game]['home_score'] - game_dictionary[game]['away_score']
                if final_score > 0:
                    home_won = True
                else:
                    home_won = False

                if game_dictionary[game]['home_name'] == Static.teamname:
                    if home_won:
                        print('{0:10}{1:2}  {3:10} {2:2} W'.format(game_dictionary[game]['away_name'],
                                                                   game_dictionary[game]['away_score'],
                                                                   game_dictionary[game]['home_score'],
                                                                   game_dictionary[game]['home_name']))
                    else:
                        print('{0:10}{1:2}  {3:10} {2:2}   L'.format(game_dictionary[game]['away_name'],
                                                                   game_dictionary[game]['away_score'],
                                                                   game_dictionary[game]['home_score'],
                                                                   game_dictionary[game]['home_name']))
                else:
                    if home_won:
                        print('{3:10}{0:2}  {1:10} {2:2}   L'.format(game_dictionary[game]['away_score'],
                                                                      game_dictionary[game]['home_name'],
                                                                      game_dictionary[game]['home_score'],
                                                                      game_dictionary[game]['away_name']))
                    else:
                        print('{3:10}{0:2}  {1:10} {2:2}   W'.format(game_dictionary[game]['away_score'],
                                                                      game_dictionary[game]['home_name'],
                                                                      game_dictionary[game]['home_score'],
                                                                      game_dictionary[game]['away_name']))
        elif game_dictionary[game]['status'] == 'Pre-Game' or game_dictionary[game]['status'] == 'Scheduled':
            time_pre_zone_change = datetime.strptime(game_dictionary[game]['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
            time_post_zone_change_dt = time_pre_zone_change - timedelta(hours=7)
            time_west_coast = time_post_zone_change_dt.strftime("%I:%M %p %Z")
            if game_dictionary[game]['home_name'] == Static.teamname:
                print('{0:22} P - {1:17} T-{2:2} {3} PDT'.format(game_dictionary[game]['away_name'],
                                                                 game_dictionary[game]['home_probable_pitcher'], diff_days,
                                                                 time_west_coast))
            else:
                print('@{0:21} P - {1:17} T-{2:2} {3} PDT'.format(game_dictionary[game]['home_name'],
                                                                 game_dictionary[game]['away_probable_pitcher'], diff_days,
                                                                 time_west_coast))

    return game_live


init_time = time.perf_counter()
in_game_timer = 0
update_time = 3600
d = getGames(game_diction)
# print(time.perf_counter() - init_time)
live = writeGames(d)

if live:
    update_time = 20
else:
    update_time = 50
for i in range(7):
    print(' ')
flag = False

while True:

    current_date = datetime.now()
    current_date = current_date + timedelta(hours=3)

    if Static.end_game:
        range(10000)  # some payload code
        #print("Me again")  # some console logging
        time.sleep(60)  # sane sleep time of 0.1 seconds
        d = getGames(game_diction)
        Static.end_game = False
        flag = False
    game_date_datetime1 = datetime.strptime(game_diction[0]['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
    dif = game_date_datetime1 - current_date
    if game_diction[0]['status'] == "FINAL":
        dif = game_diction[1].date - current_date
    dif_days = dif.days
    dif_seconds = dif.seconds
    if dif_days == 0 or dif_days == -1:
        if 360 > dif_seconds > -1000:
            if not flag:
                range(10000)  # some payload code
                # print("Me again")  # some console logging
                time.sleep(60)  # sane sleep time of 0.1 seconds
                d = getGames(game_diction)
                live = writeGames(d)
                if live:
                    flag = True
                    in_game_timer = time.perf_counter()
            update_time = 20
    current_time = time.perf_counter()
    if current_time - init_time > update_time:

        init_time = current_time
        try:
            if update_time is not 20:
                range(10000)  # some payload code
                # print("Me again")  # some console logging
                time.sleep(60)  # sane sleep time of 0.1 seconds
                d = getGames(game_diction)
            # d = getGames(game_diction)
            init_time2 = time.perf_counter()
            live = writeGames(d)
            now = datetime.now()
            print("{0}    Time Updated: {1}".format(update_time, now))

            # print(time.perf_counter() - init_time2)

            if live:
                update_time = 20
                if time.perf_counter() - in_game_timer > 14400:
                    range(10000)  # some payload code
                    # print("Me again")  # some console logging
                    time.sleep(60)  # sane sleep time of 0.1 seconds
                    d = getGames(game_diction)
                    live = writeGames(d)
                    in_game_timer = 0
            else:
                update_time = 3600
                flag = False

            for i in range(7):
                print(' ')
        except Exception as exc:
            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            error = "ERROR! {}".format(exc)
            log = 'log.txt'
            with open(log, 'a') as logfile:
                logfile.write(sttime + error + '\n')
            print("error recorded")

            time.sleep(900)
            print("error recorded")
            range(10000)  # some payload code
            # print("Me again")  # some console logging
            time.sleep(60)  # sane sleep time of 0.1 seconds
            d = getGames(game_diction)
            live = writeGames(d)
print('If this shows up, you done fucked up')
