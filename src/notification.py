import os
from datetime import datetime
import time
import RPi.GPIO as GPIO
import requests
import json

# Global variables:
number_of_times_button_has_been_pressed = 0

# Emergency button GPIO definition:
gpio_emergency_button = 18


# Function: prepare/setup emergency button GPIO
# Params: none
# Return: none
def setup_emergency_button_gpio():
    # setup emergency button gpio as input (using internal SOC pull-up)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_emergency_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return


# Function: send Pushbullet notification
# Params: number of times emergency button has been pressed
# Return: none
def send_pushbullet_notification(number):
    now = datetime.now()
    StringDataHora = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " em " + str(now.day) + "/" + str(
        now.month) + "/" + str(now.year)

    StringMsg = "Emergency button pressing #" + str(
        number) + ". Last date/time emergency button has been pressed: " + StringDataHora + "."
    data_send = {"type": "note", "title": "Notification - emergency button", "body": StringMsg}

    # Pushbullet access token
    access_token = 'o.iLMdb3vOaI5NQgQlexg0fBxcnLH9d1vS'
    result_notification_send = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                                             headers={'Authorization': 'Bearer ' + access_token,
                                                      'Content-Type': 'application/json'})

    return


# Function: verify if emergency button is pressed (and waits for its release)
# Params: none
# Return: none
def verify_emergency_button_is_pressed():
    global number_of_times_button_has_been_pressed

    # if emergency button is pressed, a Pushbullet notification is sent.
    if GPIO.input(gpio_emergency_button) == 0:
        # Update emergency button pressing counter and send the Pushbullet notification
        number_of_times_button_has_been_pressed = number_of_times_button_has_been_pressed + 1
        send_pushbullet_notification(number_of_times_button_has_been_pressed)

        # debouncing delay (50ms)
        time.sleep(0.050)

        # waits for emergency button release.
        # This ensures no risk of sending multiple notifications in just one button press.
        while GPIO.input(gpio_emergency_button) == 0:
            continue

    return


# ------------------------
#   Main program
# -----------------------
time.sleep(30)
setup_emergency_button_gpio()

# Main loop
while True:
    verify_emergency_button_is_pressed()
