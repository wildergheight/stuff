#!/usr/bin/env python

from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO  # Allows us to call our GPIO pins and names it just GPIO
import urllib.request
import time

time_init = time.perf_counter()

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 5  # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA$
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input
level_flag = 0


class pushingbox():
    url = ""

    def __init__(self, key, t):
        url = 'http://api.pushingbox.com/pushingbox'
        values = {'devid': key}
        sendrequest = urllib.request.urlopen(
            'http://api.pushingbox.com/pushingbox?devid=vB053531C1B839B1&time_filled=' + t)


while True:
    if GPIO.input(INPUT_PIN) == False and (level_flag == 0):  # Physically read the pin now
        print('sending message now')
        time_out = time.perf_counter()
        t = (time_out - time_init)
        t = str(round(t / 86400, 2))
        pushingbox('vB053531C1B839B1', t)
        level_flag = 1
        sleep(7200)
        time_out = time.perf_counter()
        t = time_out - time_init
        t = str(round(t / 86400, 2))
        pushingbox('vB053531C1B839B1', t)
        break
    else:
        print('0')
    sleep(5)  # Sleep for a full second before restarting our loop
