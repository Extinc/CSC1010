import time
from datetime import datetime
from time import sleep
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(True, True, True)

# MQTT
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'csc1010/falldetection'
MESSAGE = 'Connected to Subscriber'

publisher = mqtt.Client('python_pub')
# To Connect to MQTT CLient
publisher.connect(MQTTBROKER, PORT)
publisher.publish(TOPIC, MESSAGE)

yellow = (255, 255, 0)
# Turna all LED OFF
sense.clear()
fieldnames = ["pitch", "roll", "yaw", "gyrox", "gyroy", "gyroz", "accelx", "accely", "accelz", "Motion"]


class Motion:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STATIONARY = 5
    OFF = 0


def showLED(value):
    if value is Motion.DOWN:
        sense.clear(yellow)
    else:
        sense.clear()


class SenseData:
    def __init__(self, compass_value, orient_val, gyro_val, accel_val):
        self.comx, self.comy, self.comz = compass_value
        self.pitch, self.roll, self.yaw = orient_val
        self.gyrox, self.gyroy, self.gyroz = gyro_val
        self.accelx, self.accely, self.accelz = accel_val
        self.timestamp = datetime.now().isoformat
        self.motion = None

    def set_motion(self, motion):
        self.motion = motion

    def pr_compass(self):
        msg = {"comx": self.comx, "comy": self.comy, "comz": self.comz}
        print(msg)
        return msg

    def pr_orientation(self):
        msg = {"pitch": self.pitch, "roll": self.roll, "yaw": self.yaw}
        print(msg)
        return msg

    def pr_gyro(self):
        msg = {"gyrox": self.gyrox, "gyroy": self.gyroy, "gyroz": self.gyroz}
        print(msg)
        return msg

    def pr_accel(self):
        msg = {"accelx": self.accelx, "accely": self.accely, "accelz": self.accelz}
        print(msg)
        return msg

    def data_list(self):
        msg = {"pitch": self.pitch, "roll": self.roll, "yaw": self.yaw, "gyrox": self.gyrox, "gyroy": self.gyroy,
               "gyroz": self.gyroz, "accelx": self.accelx, "accely": self.accely, "accelz": self.accelz,
               "Motion": self.motion}
        return msg


prev_x = 0
prev_y = 0
prev_z = 0
flag = True
flag_start = False

testcount = 0
datalist = []

prev_res = 0
lastcomz = 0
lastmovement_x = 0
lastmovement_y = 0
lastmovement_z = 0
while (flag):
    data = SenseData(sense.get_compass_raw().values(), sense.get_orientation().values(),
                     sense.get_gyroscope_raw().values(), sense.get_accelerometer_raw().values())
    accelx = round(data.accelx, 4) * 10
    accely = round(data.accely, 4) * 10
    accelz = round(data.accelz, 4) * 10

    if not flag_start:
        flag_start = True
        prev_x = round(data.accelx, 2)
        prev_y = round(data.accely, 2)
        prev_z = round(data.accelz, 2)

    diff_accel_x = abs((round(data.accelx, 4) * 10) - (prev_x * 10))
    diff_accell_y = abs((round(data.accely, 4) * 10) - (prev_y * 10))
    diff_accel_z = abs((round(data.accelz, 4) * 10) - (prev_z * 10))
    if diff_accel_x < 1 and diff_accell_y < 1 and diff_accel_z < 1:

        # If the device is not moving
        showLED(Motion.STATIONARY)
        data.set_motion(Motion.STATIONARY)

    else:
        diff_gyro = (round(data.gyrox, 1)) < -0.5 or round(data.gyroy, 1) < -0.5 or round(data.gyroz, 1) < -0.5

        prev_x = round(data.accelx, 2)
        prev_y = round(data.accely, 2)
        prev_z = round(data.accelz, 2)

        if (diff_accel_x >= 2 or diff_accell_y >= 2 or diff_accel_z >= 2) and diff_gyro:
            data.set_motion(Motion.DOWN)

            showLED(Motion.DOWN)

            # When fall detected 

            # CHeck if any movement

            sleep(2)
            isbuttonpressed = False
            print("Waiting for button input")
            timestart = time.time()
            while not isbuttonpressed:

                eventlist = sense.stick.get_events()

                time2 = time.time()
                if time2 - timestart >= 5:
                    break
                for event in eventlist:
                    if event.direction == 'middle' and event.action == 'pressed':
                        isbuttonpressed = True
                        print("Button has been pressed")
                        event = sense.stick.wait_for_event(emptybuffer=True)
                        showLED(None)
                        break

            if not isbuttonpressed:
                sleep(1)
                MESSAGE = "Fall Detected"
                publisher.publish(TOPIC, MESSAGE)
                print("Fall Detected message sent")
            else:
                isbuttonpressed = False
        else:
            data.set_motion(Motion.UP)
            showLED(Motion.UP)

        lastmovement_x = data.gyrox
        lastmovement_y = data.gyroy
        lastmovement_z = data.gyroz

    sleep(0.7)
