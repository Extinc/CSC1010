import paho.mqtt.client as mqtt

MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'csc1010/falldetection'
MESSAGE = 'Connected to Subscriber'

publisher = mqtt.Client('python_pub')
publisher.connect(MQTTBROKER, PORT)
publisher.publish(TOPIC, MESSAGE)


# On Fall Detected, run these code
MESSAGE = "Fall Detected"
publisher.publish(TOPIC, MESSAGE)
print("Fall Detected message sent")
