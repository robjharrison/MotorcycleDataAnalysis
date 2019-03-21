
# how do i integrate the camera (batch/segmented) recording to the below logging....

raspivid --width 640 --height 360 --framerate 24 --bitrate 750000 --qp 15 --timeout $((24*60*60*1000)) --segment $((1*60*60*1000)) --output hour%02d.h264
# from
#https://raspberrypi.stackexchange.com/questions/26714/can-i-record-a-24-hour-video-on-the-raspberry-pi-with-camera-module




##### Libraries #####
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from datetime import datetime
from time import sleep
from threading import Thread

import os

##### Logging Settings #####
WRITE_FREQUENCY = 60
DELAY=0
x=2 #shutdown variable
FILENAME = "DriveLog.csv"


##### Functions #####


def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)
    
def get_sense_data():
    sense_data=[]

    sense_data.append(datetime.now().replace(microsecond=0).isoformat(' '))

    sense_data.append(sense.get_temperature_from_humidity())
    sense_data.append(sense.get_temperature_from_pressure())
    sense_data.append(sense.get_humidity())
    sense_data.append(sense.get_pressure())

    o = sense.get_orientation()
    yaw = o["yaw"]
    pitch = o["pitch"]
    roll = o["roll"]
    sense_data.extend([pitch,roll,yaw])

    mag = sense.get_compass_raw()
    mag_x = mag["x"]
    mag_y = mag["y"]
    mag_z = mag["z"]
    sense_data.extend([mag_x,mag_y,mag_z])

    acc = sense.get_accelerometer_raw()
    x = acc["x"]
    y = acc["y"]
    z = acc["z"]
    sense_data.extend([x,y,z])

    gyro = sense.get_gyroscope_raw()
    gyro_x = gyro["x"]
    gyro_y = gyro["y"]
    gyro_z = gyro["z"]
    sense_data.extend([gyro_x,gyro_y,gyro_z])

    return sense_data


def joystickEventHandling(event):
    global x
    if event.action == ACTION_PRESSED:
        x = 1 # toggle between 0/1 where 0 is shutdown 1 is exit program



# Define some colours
blue = (0, 0, 255)
yellow = (255, 255, 0)


##### Main Program #####
sense = SenseHat()
batch_data= []


while True:
    # Display LED matrix
    sense.show_message("+", text_colour=yellow, back_colour=blue, scroll_speed=0.05)
    sleep(.5)
    sense.clear()
    sleep(.5)
    sense.show_message("+", text_colour=yellow, back_colour=blue, scroll_speed=0.1)

    sense_data = get_sense_data()
    log_data()


        
    if len(batch_data) >= WRITE_FREQUENCY:
        
##        print("Writing to file..")

        sense.show_message("+", text_colour=blue, back_colour=yellow, scroll_speed=0.05)


        with open(FILENAME,"a") as f:
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []

        sense.clear(blue) 


    events = sense.stick.get_events()
    for event in events:
        joystickEventHandling(event)

    if x == 0:
            sense.clear()
            os.system("sudo shutdown now -P")
            sleep(30)
    elif x == 1:
            sense.clear()
            raise SystemExit
            sleep(30)

