from ohmysportsfeedspy import MySportsFeeds

msf = MySportsFeeds(version="2.0")

msf.authenticate("a13e361c-0c35-4934-b4e4-527214", "MYSPORTSFEEDS")

output = msf.msf_get_data(league='nba', season='2016-2017-regular', feed='seasonal_player_gamelogs', format='json',
                          player='stephen-curry')
print(output)
