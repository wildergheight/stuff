from samplebase import SampleBase
from rgbmatrix import graphics
import time
import requests
import json
import pytemperature
from datetime import datetime
from mqtt import Mqtt


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def drawClear(self, canvas, clr):
        # Clear Icon                              x1 y1  x2 y2  color
        len = graphics.DrawLine(canvas, 11, 12, 11, 12, clr)
        len = graphics.DrawLine(canvas, 20, 12, 20, 12, clr)

        len = graphics.DrawLine(canvas, 12, 13, 12, 13, clr)
        len = graphics.DrawLine(canvas, 15, 13, 16, 13, clr)
        len = graphics.DrawLine(canvas, 19, 13, 19, 13, clr)

        len = graphics.DrawLine(canvas, 14, 14, 17, 14, clr)

        len = graphics.DrawLine(canvas, 9, 15, 11, 15, clr)
        len = graphics.DrawLine(canvas, 13, 15, 18, 15, clr)
        len = graphics.DrawLine(canvas, 20, 15, 22, 15, clr)

        len = graphics.DrawLine(canvas, 13, 16, 18, 16, clr)

        len = graphics.DrawLine(canvas, 14, 17, 17, 17, clr)

        len = graphics.DrawLine(canvas, 12, 18, 12, 18, clr)
        len = graphics.DrawLine(canvas, 15, 18, 16, 18, clr)
        len = graphics.DrawLine(canvas, 19, 18, 19, 18, clr)

        len = graphics.DrawLine(canvas, 11, 19, 11, 19, clr)
        len = graphics.DrawLine(canvas, 20, 19, 20, 19, clr)

    def drawClouds(self, canvas, clr):
        # Clouds Icon                              x1 y1  x2 y2  color
        len = graphics.DrawLine(canvas, 13, 12, 14, 12, clr)

        len = graphics.DrawLine(canvas, 12, 13, 15, 13, clr)
        len = graphics.DrawLine(canvas, 17, 13, 18, 13, clr)

        len = graphics.DrawLine(canvas, 10, 14, 19, 14, clr)

        len = graphics.DrawLine(canvas, 9, 15, 19, 15, clr)

        len = graphics.DrawLine(canvas, 9, 16, 20, 16, clr)

        len = graphics.DrawLine(canvas, 9, 17, 20, 17, clr)

        len = graphics.DrawLine(canvas, 10, 18, 12, 18, clr)
        len = graphics.DrawLine(canvas, 15, 18, 16, 18, clr)
        len = graphics.DrawLine(canvas, 18, 18, 19, 18, clr)

    def drawNight(self, canvas, clr):
        len = graphics.DrawLine(canvas, 13, 12, 16, 12, clr)

        len = graphics.DrawLine(canvas, 14, 13, 17, 13, clr)

        len = graphics.DrawLine(canvas, 15, 14, 18, 14, clr)

        len = graphics.DrawLine(canvas, 15, 15, 18, 15, clr)

        len = graphics.DrawLine(canvas, 15, 16, 15, 16, clr)
        len = graphics.DrawLine(canvas, 17, 16, 18, 16, clr)

        len = graphics.DrawLine(canvas, 15, 17, 18, 17, clr)

        len = graphics.DrawLine(canvas, 14, 18, 17, 18, clr)

        len = graphics.DrawLine(canvas, 13, 19, 16, 19, clr)

    def drawRain(self, canvas, clr1, clr2):
        len = graphics.DrawLine(canvas, 13, 12, 19, 12, clr1)

        len = graphics.DrawLine(canvas, 12, 13, 20, 13, clr1)

        len = graphics.DrawLine(canvas, 12, 14, 20, 14, clr1)

        len = graphics.DrawLine(canvas, 13, 15, 19, 15, clr1)

        len = graphics.DrawLine(canvas, 14, 17, 14, 17, clr2)
        len = graphics.DrawLine(canvas, 16, 17, 16, 17, clr2)
        len = graphics.DrawLine(canvas, 18, 17, 18, 17, clr2)

        len = graphics.DrawLine(canvas, 14, 18, 14, 18, clr2)
        len = graphics.DrawLine(canvas, 16, 18, 16, 18, clr2)
        len = graphics.DrawLine(canvas, 18, 18, 18, 18, clr2)

        len = graphics.DrawLine(canvas, 14, 19, 14, 19, clr2)
        len = graphics.DrawLine(canvas, 16, 19, 16, 19, clr2)
        len = graphics.DrawLine(canvas, 18, 19, 18, 19, clr2)

    def drawDrizzle(self, canvas, clr1, clr2):
        len = graphics.DrawLine(canvas, 13, 12, 19, 12, clr1)

        len = graphics.DrawLine(canvas, 12, 13, 20, 13, clr1)

        len = graphics.DrawLine(canvas, 12, 14, 20, 14, clr1)

        len = graphics.DrawLine(canvas, 13, 15, 19, 15, clr1)

        len = graphics.DrawLine(canvas, 14, 17, 14, 17, clr2)
        len = graphics.DrawLine(canvas, 18, 17, 18, 17, clr2)

    def drawThunderstorm(self, canvas, clr1, clr2):
        len = graphics.DrawLine(canvas, 12, 12, 20, 12, clr1)

        len = graphics.DrawLine(canvas, 13, 13, 15, 13, clr1)
        len = graphics.DrawLine(canvas, 16, 13, 16, 13, clr2)
        len = graphics.DrawLine(canvas, 18, 13, 19, 13, clr1)

        len = graphics.DrawLine(canvas, 17, 14, 17, 14, clr2)

        len = graphics.DrawLine(canvas, 18, 15, 18, 15, clr2)

        len = graphics.DrawLine(canvas, 17, 16, 17, 16, clr2)

        len = graphics.DrawLine(canvas, 16, 17, 16, 17, clr2)

        len = graphics.DrawLine(canvas, 17, 18, 17, 18, clr2)

        len = graphics.DrawLine(canvas, 18, 19, 18, 19, clr2)

    def drawFog(self, canvas, clr):
        len = graphics.DrawLine(canvas, 13, 13, 19, 13, clr)

        len = graphics.DrawLine(canvas, 14, 15, 18, 15, clr)

        len = graphics.DrawLine(canvas, 14, 17, 17, 17, clr)

        len = graphics.DrawLine(canvas, 13, 19, 19, 19, clr)

    def drawWait(self, canvas):
        tColor = graphics.Color(255, 255, 255)
        len = graphics.DrawLine(canvas, 2, 1, 5, 1, tColor)

        len = graphics.DrawLine(canvas, 2, 2, 5, 2, tColor)

        len = graphics.DrawLine(canvas, 2, 3, 5, 3, tColor)

    # def undrawWait(self, canvas):
    #     tColor = graphics.Color(0, 0, 0)
    #     len = graphics.DrawLine(canvas, 2, 1, 5, 1, tColor)
    #
    #     len = graphics.DrawLine(canvas, 2, 2, 5, 2, tColor)
    #
    #     len = graphics.DrawLine(canvas, 2, 3, 5, 3, tColor)

    def getMqttTemp(self, client, my_mqtt):
        # try:
        my_mqtt.subscribe(client)
        client.loop_start()
        mqtt_temp = round(float(my_mqtt.temp))
        client.loop_stop()
        # except:
        #     mqtt_temp = '0'
        # print(mqtt_temp)
        return mqtt_temp

    def getWeather(self, client, my_mqtt):
        mTemp = self.getMqttTemp(client, my_mqtt)
        url = "http://api.openweathermap.org/data/2.5/weather?zip=92122,US&appid=3294e2836901a1399a3c094dc825a1b2"
        response = requests.get(url)
        # url2 = 'https://api.weatherbit.io/v2.0/current?postal_code=92122&units=I&key=721fff29e1ef4aa5b7fcb7b99b284bc4'
        # url2 = 'https://api.weatherbit.io/v2.0/current?station=AS861&units=I&key=721fff29e1ef4aa5b7fcb7b99b284bc4'
        url2 = 'http://api.openweathermap.org/data/2.5/uvi?appid=3294e2836901a1399a3c094dc825a1b2&lat=32.867&lon=-127.2'
        response2 = requests.get(url2)
        weather_get = json.loads(response.text)
        weather_get2 = json.loads(response2.text)

        weather_type = weather_get['weather'][0]['main']
        # temp = int(weather_get2['data'][0]['temp'])

        if (mTemp == 0):
            temp = int(round(pytemperature.k2f(weather_get['main']['temp']), 0))
            print("did not get MQTT temp")
        else:
            print("MQTT temp")
            temp = mTemp

        temp_color = []
        if temp > 89:
            temp_color = [181, 22, 22]
        elif temp > 79:
            temp_color = [255, 255, 0]
        elif temp > 69:
            temp_color = [81, 255, 0]
        elif temp > 59:
            temp_color = [0, 38, 255]
        elif temp > 49:
            temp_color = [0, 225, 255]
        else:
            temp_color = [255, 255, 255]

        current_time = datetime.now()
        sunset = int(weather_get['sys']['sunset'])
        sunrise = int(weather_get['sys']['sunrise'])
        sunset_time = datetime.fromtimestamp(sunset)
        sunrise_time = datetime.fromtimestamp(sunrise)

        diff_sunset = (sunset_time - current_time).days
        diff_sunrise = (sunrise_time - current_time).days

        day_bool = False
        if diff_sunset >= 0 and diff_sunrise < 0:
            day_bool = True

        temperature = str(temp) + "°F"
        # cloud_percentage = str(weather_get['clouds']['all']) + "%"
        # wind_dir = weather_get2['data'][0]['wind_cdir']
        wind_dir = 'NSW'
        wind_int = int(weather_get['wind']['speed'] * 2.23694)
        if wind_int > 9:
            wind_length = 2
        else:
            wind_length = 1
        wind = str(wind_int)
        humidity = str(weather_get['main']['humidity'])
        # uv = str(int(round(weather_get2['data'][0]['uv'],0))) + " " + humidity
        uv = str(int(round(weather_get2['value'], 0))) + " " + humidity
        if int(round(weather_get2['value'], 0)) > 9:
            uv_length = 2
        else:
            uv_length = 1
        weather_stats = [weather_type, temperature, temp_color, day_bool, wind, uv_length, uv, wind_length, wind_dir]
        return weather_stats

    def run(self):
        init_time = time.perf_counter()
        my_mqtt = Mqtt()
        client = my_mqtt.connect_mqtt()
        stats = self.getWeather(client, my_mqtt)
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 255)
        tempColor = graphics.Color(stats[2][0], stats[2][1], stats[2][2])
        uvColor = graphics.Color(255, 130, 130)
        pos = offscreen_canvas.width
        temp = stats[1]
        desc = stats[0]
        wind_speed = stats[4]
        wind_direction = stats[8]
        uv = stats[6]
        backColor = graphics.Color(204, 9, 47)
        clr = 0
        prnt_time_temp = 0

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawLine(offscreen_canvas, 0, 0, 0, 31, tempColor)
            len = graphics.DrawLine(offscreen_canvas, 31, 0, 31, 31, tempColor)
            len = graphics.DrawText(offscreen_canvas, font, 9, 5, tempColor, temp)

            if stats[7] == 1:
                len = graphics.DrawText(offscreen_canvas, font, 8, 26, textColor, wind_speed)
                len = graphics.DrawText(offscreen_canvas, font, 16, 26, textColor, wind_direction)
            else:
                len = graphics.DrawText(offscreen_canvas, font, 6, 26, textColor, wind_speed)
                len = graphics.DrawText(offscreen_canvas, font, 16, 26, textColor, wind_direction)
            if stats[5] == 1:
                len = graphics.DrawText(offscreen_canvas, font, 8, 32, uvColor, uv)
            else:
                len = graphics.DrawText(offscreen_canvas, font, 6, 32, uvColor, uv)

            if stats[0] == 'Clear':
                if not stats[3]:
                    self.drawNight(offscreen_canvas, graphics.Color(255, 253, 158))
                    len = graphics.DrawText(offscreen_canvas, font, 7, 11, textColor, desc)
                else:
                    self.drawClear(offscreen_canvas, graphics.Color(255, 255, 0))  # 255, 255, 0
                    # clr += 1
                    # if clr >= 255:
                    #     clr = 0
                    len = graphics.DrawText(offscreen_canvas, font, 7, 11, textColor, desc)
            elif stats[0] == 'Clouds':
                self.drawClouds(offscreen_canvas, graphics.Color(104, 112, 112))
                len = graphics.DrawText(offscreen_canvas, font, 5, 11, textColor, desc)
            elif stats[0] == 'Thunderstorm':
                self.drawThunderstorm(offscreen_canvas, graphics.Color(0, 0, 255), graphics.Color(255, 255, 0))
                len = graphics.DrawText(offscreen_canvas, font, 5, 11, textColor, "Tstorm")
            elif stats[0] == 'Drizzle':
                self.drawDrizzle(offscreen_canvas, graphics.Color(104, 112, 112), graphics.Color(0, 200, 255))
                len = graphics.DrawText(offscreen_canvas, font, 3, 11, textColor, desc)
            elif stats[0] == 'Rain' or stats[0] == 'Snow':
                self.drawRain(offscreen_canvas, graphics.Color(104, 112, 112), graphics.Color(0, 200, 255))
                len = graphics.DrawText(offscreen_canvas, font, 9, 11, textColor, desc)
            elif stats[0] == 'Mist' or stats[0] == 'Fog':
                self.drawFog(offscreen_canvas, graphics.Color(104, 112, 112))
                len = graphics.DrawText(offscreen_canvas, font, 9, 11, textColor, desc)
            else:
                len = graphics.DrawText(offscreen_canvas, font, 9, 11, textColor, desc)

            # self.drawWait(offscreen_canvas)

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            current_time = time.perf_counter()
            # prnt_time = int(round(500 - (current_time - init_time),0))
            # if prnt_time != prnt_time_temp:
            #     print("Time until next update: " + str(prnt_time))
            #     prnt_time_temp = prnt_time
            if current_time - init_time > 500:
                init_time = current_time
                try:
                    stats = self.getWeather(client, my_mqtt)
                except Exception as exc:
                    self.drawWait(offscreen_canvas)
                    sttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                    error = "ERROR! {}".format(exc)
                    log = r'/home/pi/rpi-rgb-led-matrix/log.txt'
                    # with open(log, 'a') as logfile:
                    #     logfile.write(sttime + error + '\n')
                    print("Error Recorded {}".format(sttime))
                    time_wait_init = time.perf_counter()
                    while 1:
                        self.drawWait(offscreen_canvas)
                        time_wait_current = time.perf_counter()
                        if time_wait_current - time_wait_init > 1800:
                            # self.undrawWait(offscreen_canvas)
                            break
                    # time.sleep(1800)

                temp = stats[1]
                tempColor = graphics.Color(stats[2][0], stats[2][1], stats[2][2])
                desc = stats[0]
                wind_speed = stats[4]
                uv = stats[6]


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
