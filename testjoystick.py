from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()
while True:
#   for event in sense.stick.get_events():
    # Check if the joystick was pressed
    print(sense.stick.get_events())
      # Wait a while and then clear the screen
    sleep(0.5)
    sense.clear()