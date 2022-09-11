import paho.mqtt.client as mqtt
from datetime import datetime
import requests
import json

MQTTBROKER = 'test.mosquitto.org'
PORT = 1883

# Function: send Pushbullet notification
# Return: none
def send_pushbullet_notification():
    now = datetime.now()
    StringDataHora = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " em " + str(now.day) + "/" + str(
        now.month) + "/" + str(now.year)

    StringMsg = "Fall Detected. Date and Time detected: " + StringDataHora + "."
    data_send = {"type": "note", "title": "Notification - Fall Detected", "body": StringMsg}

    # Pushbullet access token
    access_token = 'o.jRw09nOWyyAhHhZKfx0J9i1ZOfKHRO9w'
    result_notification_send = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                                             headers={'Authorization': 'Bearer ' + access_token,
                                                      'Content-Type': 'application/json'})
    return


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('csc1010/falldetection')


def on_disconnect(client, userdata, rc):
    print('Disconnect with result code' + str(rc))

def on_message(client, userdata, msg):
    txt = str(msg.payload.decode("utf-8"))
    print(txt)
    if txt == "Fall Detected":
        send_pushbullet_notification()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()