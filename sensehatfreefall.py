from ast import Or
from asyncore import write
from cgitb import reset
from re import L
from sense_hat import SenseHat
from time import sleep 
from datetime import datetime
import math
import csv


sense = SenseHat()
sense.set_imu_config(True, True, True)

# Turna all LED OFF
sense.clear()
fieldnames = ["pitch", "roll", "yaw","gyrox", "gyroy", "gyroz" ,"accelx", "accely" , "accelz" , "Motion" ]
class Motion:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STATIONARY = 5
    OFF = 0

def showLED(value):
    if value is Motion.UP:
        sense.show_letter("U")
    elif value is Motion.DOWN:
        sense.show_letter("D")
    elif value is Motion.LEFT:
        sense.show_letter("L")  
    elif value is Motion.RIGHT:
        sense.show_letter("R")  
    elif value is Motion.STATIONARY:
        sense.show_letter("S")
    else:
        sense.clear()

class SenseData:
    def __init__(self, compass_value, orient_val,gyro_val, accel_val):
        self.comx, self.comy, self.comz =compass_value
        self.pitch, self.roll, self.yaw = orient_val
        self.gyrox, self.gyroy, self.gyroz = gyro_val
        self.accelx, self.accely, self.accelz =accel_val
        self.timestamp = datetime.now().isoformat
        self.motion = None
    
    def set_motion(self, motion):
        self.motion = motion

    def pr_compass(self):
        msg = {"comx" : self.comx, "comy" : self.comy, "comz" :self.comz}
        print(msg)
        return msg
    
    def pr_orientation(self):
        msg = {"pitch" : self.pitch, "roll" : self.roll, "yaw" :self.yaw}
        print(msg)
        return msg

    def pr_gyro(self):
        msg = {"gyrox" : self.gyrox, "gyroy" : self.gyroy, "gyroz" :self.gyroz}
        print(msg)
        return msg
    
    def pr_accel(self):
        msg = {"accelx" : self.accelx, "accely" : self.accely, "accelz" :self.accelz}
        print(msg)
        return msg

    def data_list(self):
        msg = {"pitch" : self.pitch, "roll" : self.roll, "yaw" :self.yaw,"gyrox" : self.gyrox, "gyroy" : self.gyroy, "gyroz" :self.gyroz,"accelx" : self.accelx, "accely" : self.accely, "accelz" :self.accelz, "Motion" : self.motion}
        return msg

prev_x = 0
prev_y =0
prev_z=0
flag = True
flag_start = False
testcount = 0
datalist = []
while(flag):
    data = SenseData(sense.get_compass_raw().values(), sense.get_orientation().values(), sense.get_gyroscope_raw().values(), sense.get_accelerometer_raw().values())

    if not flag_start:
        flag_start = True
        prev_x = round(data.accelx,2)
        prev_y = round(data.accely,2)
        prev_z = round(data.accelz,2)

    res = math.sqrt((data.accelx ** 2)+(data.accely ** 2)+(data.accelz ** 2))
    print("TOTAL ACCELERATION  : " + str(res))
    if round(data.accelx,2) == prev_x and round(data.accely,2) == prev_y and round(data.accelz,2) == prev_z:
        # If the device is not moving
        showLED(Motion.STATIONARY)
        data.set_motion(Motion.STATIONARY)
        data.pr_orientation()
        data.pr_gyro()
        data.pr_accel()
    else:
        prev_x = round(data.accelx,2)
        prev_y = round(data.accely,2)
        prev_z = round(data.accelz,2)

        
        if data.accely < 0:
            data.set_motion(Motion.DOWN)
            showLED(Motion.DOWN)
        else:
            if abs(res) >= 1.0:
                data.set_motion(Motion.UP)
                showLED(Motion.UP)
            else:
                showLED(Motion.OFF)
        data.pr_orientation()
        data.pr_gyro()
        data.pr_accel()
    
    datalist.append(data.data_list())
    testcount += 1
    sleep(0.5)
    if (testcount == 30):
        flag = False


# open the file in the write mode
with open('testdata.csv', 'w', newline ='') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    writer.writerows(datalist)