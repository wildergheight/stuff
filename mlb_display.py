from __future__ import print_function
import mlbgame
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import *
from os import system, name
import time

game_diction = {}


class Static:
    def __init__(self):
        pass

    teamname = 'Padres'
    end_game = False


def getGames(game_dict):
    current_date = datetime.now()
    # Used until season restarts
    # current_date = date.fromisoformat('2019-05-02')
    # current_date = datetime.combine(current_date, datetime.min.time())
    current_year = current_date.year
    current_month = current_date.month

    next_month_date = current_date + relativedelta(months=+1)
    next_month = next_month_date.month

    # use current year when season comes back
    month = mlbgame.games(current_year, current_month, home=Static.teamname, away=Static.teamname)
    month2 = mlbgame.games(current_year, next_month, home=Static.teamname, away=Static.teamname)

    games_future_month = mlbgame.combine_games(month2)
    games = mlbgame.combine_games(month)
    key = 0

    game_dict.clear()
    for game in games:
        # s = Game_data()

        diff = game.date - current_date
        diff_days = diff.days
        diff_seconds = diff.seconds
        if key == 10:
            break
        elif diff_days > -2 or (diff_days == 0 and diff_seconds > 0):
            # print(game)
            # print(game.date)
            game_dict.update({key: game})
            key += 1
    if key != 10:  # Less than 10 games left in current month
        for game in games_future_month:
            # s = Game_data()

            diff = game.date - current_date
            diff_days = diff.days
            diff_seconds = diff.seconds
            if key == 10:
                break
            elif diff_days > -2 or (diff_days == 0 and diff_seconds > 0):
                # print(game)
                # print(game.date)
                game_dict.update({key: game})
                key += 1
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
        if game_dictionary[game].game_status == 'IN_PROGRESS':
            game_live = True

    for game in game_dictionary:

        diff = game_dictionary[game].date - current_date

        diff_days = diff.days
        if game_dictionary[game].game_status == 'IN_PROGRESS':

            game_link = game_dictionary[game].game_id
            current_game = mlbgame.game_events(game_link)

            current_in = len(current_game)
            current_inning = current_game[current_in - 1]
            try:
                bottom_of_inning = current_inning.bottom[0]
            except Exception:
                top_or_bottom = 'T'  # Top of inning
                current_event_num = len(current_inning.top)
                current_event = current_inning.top[current_event_num - 1]

            else:
                top_or_bottom = 'B'  # Bottom of inning
                current_event_num = len(current_inning.bottom)
                current_event = current_inning.bottom[current_event_num - 1]

            current_outs = current_event.o

            if current_in >= 9:
                if current_outs == 3:
                    if current_event.away_team_runs < current_event.home_team_runs:
                        if top_or_bottom == 'T':
                            Static.end_game = True
                    elif current_event.away_team_runs != current_event.home_team_runs:
                        if top_or_bottom == 'B':
                            Static.end_game = True
                elif top_or_bottom == 'B' and current_event.home_team_runs > current_event.away_team_runs:
                    Static.end_game = True

            if game_dictionary[game].home_team == Static.teamname:
                print('{0:10}{1:2}  {6:10} {2:2} {3:1}{4:2} {5:1} Out/s'.format(game_dictionary[game].away_team,
                                                                                current_event.away_team_runs,
                                                                                current_event.home_team_runs,
                                                                                top_or_bottom, str(current_in),
                                                                                current_outs,
                                                                                game_dictionary[game].home_team))

            else:

                print('{6:10} {0:2}  {1:10} {2:2}  {3:1}{4:2} {5:1} Out/s'.format(current_event.away_team_runs,
                                                                                  game_dictionary[game].home_team,
                                                                                  current_event.home_team_runs,
                                                                                  top_or_bottom, str(current_in),
                                                                                  current_outs,
                                                                                  game_dictionary[game].away_team))
        elif game_dictionary[game].game_status == 'FINAL':
            if not game_live:
                final_score = game_dictionary[game].home_team_runs - game_dictionary[game].away_team_runs
                if final_score > 0:
                    home_won = True
                else:
                    home_won = False

                if game_dictionary[game].home_team == Static.teamname:
                    if home_won:
                        print('{0:10}{1:2}  {3:10} {2:2} W'.format(game_dictionary[game].away_team,
                                                                   game_dictionary[game].away_team_runs,
                                                                   game_dictionary[game].home_team_runs,
                                                                   game_dictionary[game].home_team))
                    else:
                        print('{0:10}{1:2}  {3:10} {2:2}   L'.format(game_dictionary[game].away_team,
                                                                     game_dictionary[game].away_team_runs,
                                                                     game_dictionary[game].home_team_runs,
                                                                     game_dictionary[game].home_team))
                else:
                    if home_won:
                        print('{3:10}{0:2}  {1:10} {2:2}   L'.format(game_dictionary[game].away_team_runs,
                                                                      game_dictionary[game].home_team,
                                                                      game_dictionary[game].home_team_runs,
                                                                      game_dictionary[game].away_team))
                    else:
                        print('{3:10}{0:2}  {1:10} {2:2}   W'.format(game_dictionary[game].away_team_runs,
                                                                     game_dictionary[game].home_team,
                                                                     game_dictionary[game].home_team_runs,
                                                                     game_dictionary[game].away_team))
        elif game_dictionary[game].game_status == 'PRE_GAME':
            time_pre_zone_change = datetime.strptime(game_dictionary[game].game_start_time, "%I:%M %p")
            time_post_zone_change_dt = time_pre_zone_change - timedelta(hours=3)
            time_west_coast = time_post_zone_change_dt.strftime("%I:%M %p %Z")
            if game_dictionary[game].home_team == Static.teamname:
                print('{0:10} P - {1:17} T-{2:2} {3} PDT'.format(game_dictionary[game].away_team,
                                                                 game_dictionary[game].p_pitcher_away, diff_days,
                                                                 time_west_coast))
            else:
                print('@{0:9} P - {1:17} T-{2:2} {3} PDT'.format(game_dictionary[game].home_team,
                                                                 game_dictionary[game].p_pitcher_home, diff_days,
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
    dif = game_diction[0].date - current_date
    if game_diction[0].game_status == "FINAL":
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
