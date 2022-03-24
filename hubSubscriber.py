import paho.mqtt.client as mqtt

MQTTBROKER = 'test.mosquitto.org'
PORT = 1883


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('csc1010/falldetection')


def on_disconnect(client, userdata, rc):
    print('Disconnect with result code' + str(rc))

def on_message(client, userdata, msg):
    txt = str(msg.payload.decode("utf-8"))
    print(txt)
    if txt == "Fall Detected":
        print("Run hub functions here")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()