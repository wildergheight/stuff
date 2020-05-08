import requests
import json
from datetime import datetime
from datetime import timedelta
import time
from samplebase import SampleBase
from rgbmatrix import graphics

current_date = datetime.utcnow()
url = 'https://statsapi.web.nhl.com'
game_dict = {}
nyr = 3
game_st = False
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

current_d = datetime(2019, 1, 13)

class Game_data:
    def __init__(self):
        self.game = 0
        self.gameid = 0
        self.gamedate = 0
        self.awayid = 0
        self.homeid = 0
        self.opp_record = []
        # self.away_score = 0
        # self.home_score = 0
        self.opponent = 0



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def getSchedule(self, offscreen_canvas):
        # Things to add:
        # Obviously display stuff
        # Other info per team, maybe current record or place in division/conf
        # Countdown to next game
        # Possibly some info on previous games (if there's space)
        # Rangers current record
        # current_d = datetime.utcnow()
        # Will remove when season restarts
        print(current_d)
        game_dict.clear()
        future_d = current_d + timedelta(days=30)
        current_d_str = datetime.strftime(current_d, '%Y-%m-%d')
        future_d_str = datetime.strftime(future_d, '%Y-%m-%d')
        schedule = '/api/v1/schedule?teamId=3&startDate=' + current_d_str + '&endDate=' + future_d_str  # will need to be updated with
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
        current_date = datetime.utcnow()  # continue getting current time
        d = ''
        for i in range(0, upcoming):  # Grab upcoming 5 games
            s = Game_data()
            s.game = i
            s.gamelink = schedule_get['dates'][i]['games'][0]['link']
            d = schedule_get['dates'][i]['games'][0]['gameDate']
            s.gamedate = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
            s.awayid = schedule_get['dates'][i]['games'][0]['teams']['away']['team']['id']
            s.homeid = schedule_get['dates'][i]['games'][0]['teams']['home']['team']['id']
            # s.away_score = schedule_get['dates'][i]['games'][0]['teams']['away']['score']
            # s.home_score = schedule_get['dates'][i]['games'][0]['teams']['home']['score']
            if s.awayid == 3:
                s.opponent = '@' + team_dict[s.homeid][0]
                s.opponent = s.homeid
                s.opp_record = [schedule_get['dates'][i]['games'][0]['teams']['home']['leagueRecord']['wins'],
                                schedule_get['dates'][i]['games'][0]['teams']['home']['leagueRecord']['losses']]
            else:
                s.opponent = team_dict[s.awayid]
                s.opponent = s.awayid
                s.opp_record = [schedule_get['dates'][i]['games'][0]['teams']['away']['leagueRecord']['wins'],
                                schedule_get['dates'][i]['games'][0]['teams']['away']['leagueRecord']['losses']]
            game_dict[i] = s
            sports_out.append(game_dict[i].opponent)
        difference_in_time = game_dict[0].gamedate - current_date
        difference_in_days = difference_in_time.days

        if difference_in_days == 0:
            if (abs(difference_in_time.seconds) / 3600) <= 2:
                game_st = True
                return game_st
                # inGame(game_dict[0].gameid, game_dict[0].opponent_id)

        self.writeSchedule(offscreen_canvas)

        # print(sports_out)
        # print(sports)
        # print(team_dict[game_dict[0].opponent][0])
        # print(team_dict[game_dict[1].opponent][0])
        # print(team_dict[game_dict[2].opponent][0])
        # print(team_dict[game_dict[3].opponent][0])
        # print(team_dict[game_dict[4].opponent][0])

    # if next gametime is same as current time (or within say 2 hours post) switch to in game mode function

    def writeSchedule(self, offscreen_canvas):

        offscreen_canvas.Clear()
        font = graphics.Font()
        font.LoadFont("fonts/4x6.bdf")
        team0_Color = graphics.Color(team_dict[game_dict[0].opponent][1][0], team_dict[game_dict[0].opponent][1][1],
                                     team_dict[game_dict[0].opponent][1][2])
        team1_Color = graphics.Color(team_dict[game_dict[1].opponent][1][0], team_dict[game_dict[1].opponent][1][1],
                                     team_dict[game_dict[1].opponent][1][2])
        team2_Color = graphics.Color(team_dict[game_dict[2].opponent][1][0], team_dict[game_dict[2].opponent][1][1],
                                     team_dict[game_dict[2].opponent][1][2])
        team3_Color = graphics.Color(team_dict[game_dict[3].opponent][1][0], team_dict[game_dict[3].opponent][1][1],
                                     team_dict[game_dict[3].opponent][1][2])
        team4_Color = graphics.Color(team_dict[game_dict[4].opponent][1][0], team_dict[game_dict[4].opponent][1][1],
                                     team_dict[game_dict[4].opponent][1][2])

        team_color = [team0_Color, team1_Color, team2_Color, team3_Color, team4_Color]

        for i in range(5):
            opp = team_dict[game_dict[i].opponent][0]
            # print(team_dict[game_dict[i].awayid])
            if game_dict[i].awayid == 3:
                # opp = "at " + opp
                len = graphics.DrawText(offscreen_canvas, font, 1, (i + 1) * 6, team_color[i], "at")
                len = graphics.DrawText(offscreen_canvas, font, 10, (i + 1) * 6, team_color[i], opp)
            else:
                # opp = "vs " + opp
                len = graphics.DrawText(offscreen_canvas, font, 1, (i + 1) * 6, team_color[i], "vs")
                len = graphics.DrawText(offscreen_canvas, font, 10, (i + 1) * 6, team_color[i], opp)

            difference_in_time = game_dict[i].gamedate - current_d
            difference_in_days = difference_in_time.days
            if difference_in_days <= 9:
                len = graphics.DrawText(offscreen_canvas, font, 24, (i + 1) * 6, team_color[i], "-")
                len = graphics.DrawText(offscreen_canvas, font, 28, (i + 1) * 6, team_color[i], str(difference_in_days))

        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def inGame(self, offscreen_canvas, game_link, opp_id):
        # Things to add:
        # Obviously display stuff
        # Goal celebration (or maybe something negative if opposing, using goalScored function)
        # PP/PK implementation
        # Maybe pulled goalie? API has implementation
        # Track SOG
        # Intermission info (time remaining)

        prev_goal_h = 0
        prev_goal_a = 0

        while True:
            # timer_start = time.perf_counter()
            game_response = requests.get(url + str(game_link))
            game_get = json.loads(game_response.text)
            game_over_check = game_get['gameData']['status']['abstractGameState']

            # if game_over_check == 'Final':  # If the game is over, wait half and hour, then end the function
            #     # time.sleep(1800)  #inactive for testing, re-enable when using for real
            #     return
            opp = opp_id
            current_period = game_get['liveData']['linescore']['currentPeriod']
            time_remaining = game_get['liveData']['linescore']['currentPeriodTimeRemaining']
            home_score = game_get['liveData']['linescore']['teams']['home']['goals']
            if home_score != prev_goal_h:
                goalScored(game_get, opp_id, 1)
                prev_goal_h = home_score
            away_score = game_get['liveData']['linescore']['teams']['away']['goals']
            if away_score != prev_goal_a:
                goalScored(game_get, opp_id, 0)
                prev_goal_a = away_score

            time.sleep(.5)  # delay repeating function half a second to avoid hammering the api too much
            # timer_finish = time.perf_counter()
            # print(timer_finish - timer_start) # Check how long the repeating function takes, change sleep time accordingly

    def goalScored(self, offscreen_canvas, game, opp_id, home_away_scored):
        # Things to add:
        # Obviously display stuff
        # Scorer, assisted by possibly

        if home_away_scored == 1:
            if game['liveData']['linescore']['teams']['home']['team']['id'] == 3:
                # do rangers scored thing
                print(team_dict[nyr][0])
            else:
                # do opp_id scored thing
                print(team_dict[opp_id][0])
        else:
            if game['liveData']['linescore']['teams']['away']['team']['id'] == 3:
                # do rangers scored thing
                print(team_dict[nyr][0])
            else:
                # do opp_id scored thing
                print(team_dict[opp_id][0])
                print(team_dict[opp_id][1][0])


    def run(self):

        offscreen_canvas = self.matrix.CreateFrameCanvas()

        while True:
            offscreen_canvas.Clear()
            game_st = self.getSchedule(offscreen_canvas)
            if game_st:
                self.inGame(offscreen_canvas, game_dict[0].gameid, game_dict[0].opponent_id)
            time.sleep(5)

            global current_d
            current_d = datetime(2019, 2, 13)       #When season returns, should be current datetime.now()

            game_st = self.getSchedule(offscreen_canvas)
            if game_st:
                self.inGame(offscreen_canvas, game_dict[0].gameid, game_dict[0].opponent_id)
            time.sleep(5)

            current_d = datetime(2019, 1, 13)       #Testing multiple values




        # offscreen_canvas = self.matrix.CreateFrameCanvas()
        # font = graphics.Font()
        # font.LoadFont("fonts/4x6.bdf")
        # textColor = graphics.Color(team_dict[24][1][0], team_dict[24][1][1], team_dict[24][1][2])
        # tempColor = graphics.Color(team_dict[24][2][0], team_dict[24][2][1], team_dict[24][2][2])
        #
        # textColor2 = graphics.Color(team_dict[3][1][0], team_dict[3][1][1], team_dict[3][1][2])
        # tempColor2 = graphics.Color(team_dict[3][2][0], team_dict[3][2][1], team_dict[3][2][2])
        # scoreColor = graphics.Color(255, 255, 255)
        # pos = offscreen_canvas.width
        # time_remaining = 60
        #
        #
        # while True:
        #     offscreen_canvas.Clear()
        #     #Below is for writing in the team names in the corners of the screen
        #     #...                                      x1 y1 x2 y2
        #     len = graphics.DrawLine(offscreen_canvas, 0, 0, 12, 0, textColor)
        #     len = graphics.DrawLine(offscreen_canvas, 0, 0, 0, 6, textColor)
        #     len = graphics.DrawLine(offscreen_canvas, 12, 0, 12, 6, textColor)
        #     len = graphics.DrawLine(offscreen_canvas, 0, 6, 12, 6, textColor)
        #
        #     len = graphics.DrawText(offscreen_canvas, font, 1, 6, tempColor, 'ANA')
        #
        #     len = graphics.DrawLine(offscreen_canvas, 19, 0, 31, 0, tempColor2)
        #     len = graphics.DrawLine(offscreen_canvas, 19, 0, 19, 6, tempColor2)
        #     len = graphics.DrawLine(offscreen_canvas, 31, 0, 31, 6, tempColor2)
        #     len = graphics.DrawLine(offscreen_canvas, 19, 6, 31, 6, tempColor2)
        #
        #     len = graphics.DrawText(offscreen_canvas, font, 20, 6, textColor2, 'NYR')
        #
        #     current_period = 1
        #
        #     len = graphics.DrawText(offscreen_canvas, font, 14, 6, scoreColor, str(current_period))
        #
        #     home_score = 0
        #     away_score = 0
        #
        #     len = graphics.DrawText(offscreen_canvas, font, 1, 13, scoreColor, str(home_score))
        #     len = graphics.DrawText(offscreen_canvas, font, 28, 13, scoreColor, str(home_score))
        #
        #
        #     clk = str(timedelta(seconds=time_remaining))
        #     minutes = clk.split(':',2)[1]
        #     seconds = clk.split(':',2)[2]
        #
        #     len = graphics.DrawText(offscreen_canvas, font, 7, 13, scoreColor, minutes)
        #     len = graphics.DrawText(offscreen_canvas, font, 17, 13, scoreColor, seconds)
        #     len = graphics.DrawText(offscreen_canvas, font, 14, 13, scoreColor, ":")
        #
        #     if time_remaining != 0:
        #         time_remaining = time_remaining - 1
        #
        #     offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        #     time.sleep(1)



# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()