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

prev_res = 0
lastcomz = 0 
lastmovement_x = 0
lastmovement_y = 0
lastmovement_z = 0
while(flag):
    data = SenseData(sense.get_compass_raw().values(), sense.get_orientation().values(), sense.get_gyroscope_raw().values(), sense.get_accelerometer_raw().values())
    accelx = round(data.accelx,4) * 10
    accely = round(data.accely,4) * 10
    accelz = round(data.accelz,4) * 10

    if not flag_start:
        flag_start = True
        prev_x = round(data.accelx,2)
        prev_y = round(data.accely,2)
        prev_z = round(data.accelz,2)

    # res = math.sqrt((accelx ** 2)+(accely ** 2)+(accelz ** 2))
    
    # print("TOTAL ACCELERATION  : " + str(res))
    diff_accel_x = abs((round(data.accelx,4) * 10) - (prev_x*10)) 
    diff_accell_y = abs((round(data.accely,4) * 10) - (prev_y*10)) 
    diff_accel_z = abs((round(data.accelz,4) * 10) - (prev_z*10))
    if diff_accel_x < 1 and diff_accell_y < 1 and  diff_accel_z < 1:

        # If the device is not moving
        showLED(Motion.STATIONARY)
        data.set_motion(Motion.STATIONARY)
        # prev_res = res

        # region FOr Testing
        # data.pr_compass()
        # data.pr_orientation()
        # data.pr_gyro()
        # data.pr_accel()
        # print("X: " + str(round(data.accelx,2) * 10) + " Y: " + str(round(data.accely,2) *10) +  " Z : " + str(round(data.accelz,2) * 10))
        # print("X: " + str(round(data.gyrox,1)) + " Y: " + str(round(data.gyroy, 1)) + " Z :"+ str(round(data.gyroz,1)))
        # endregion

    else:

        diff_gyro = (round(data.gyrox,1))< -0.5 or round(data.gyroy,1) < -0.5 or round(data.gyroz,1) < -0.5
        # region FOr Testing
        # print("X: " + str(abs((round(data.accelx,4) * 10) - (prev_x*10))) + " Y: " + str(abs((round(data.accely,4) * 10) - (prev_y*10))) +  " Z : " + str(abs((round(data.accelz,4) * 10) - (prev_z*10))))
        # data.pr_compass()
        # data.pr_gyro()
        # print("X: " + str(round(data.accelx,2)  * 10) + " Y: " + str(round(data.accely,2) * 10) +  " Z : " + str(round(data.accelz,2) * 10))

        # print("RES: " + str(res))
        # endregion
        prev_x = round(data.accelx,2)
        prev_y = round(data.accely,2)
        prev_z = round(data.accelz,2) 

        print("X: " + str(round(data.gyrox,1)) + " Y: " + str(round(data.gyroy, 1)) + " Z :"+ str(round(data.gyroz,1)))
    
        if (diff_accel_x >= 2 or diff_accell_y >= 2 or diff_accel_z >= 2) and diff_gyro:
            data.set_motion(Motion.DOWN)

            showLED(Motion.DOWN)

            # When fall detected 

            # CHeck if any movement

            sleep(1)
            if(abs(data.gyrox - lastmovement_x) > 0.5 or abs(data.gyrox - lastmovement_x) > 0.5 or abs(data.gyrox - lastmovement_x) > 0.5):
                print("STILL ABLED")

            

        else:
            data.set_motion(Motion.UP)
            showLED(Motion.UP)

        lastmovement_x = data.gyrox
        lastmovement_y = data.gyroy
        lastmovement_z = data.gyroz
    
    datalist.append(data.data_list())
    testcount += 1
    sleep(0.7)
    if (testcount == 100):
        flag = False


# open the file in the write mode
with open('testdata.csv', 'w', newline ='') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    writer.writerows(datalist)