#
# driveData.py
# 23/03/2019
#
# Written to run only on device with senseHat
# Record Sensehat Accelerometer/Gyro/Mag/Humidity/Pressure data
# Filename convention: yymmddhhmmss.h264 / yymmddhhmmss_motion.data

# Reference/guidance at: 

from sense_hat import SenseHat, ACTION_PRESSED
from datetime import datetime
from time import sleep
from threading import Thread

import os


WRITE_FREQUENCY = 60        # how often the batched data is written in secs
FILENAME = "DriveLog.csv"   # resultant datafile to append to



def log_data():
    # create csv ready row format from logged data, get ready to record it
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)
    
def get_sense_data():
    # collect all the sensor data, append to empty array
    sense_data=[]

    # get the full timestamp 
    sense_data.append(datetime.now().replace(microsecond=0).isoformat(' '))

    # get pressure and humidity
    sense_data.append(sense.get_temperature_from_humidity())
    sense_data.append(sense.get_temperature_from_pressure())
    sense_data.append(sense.get_humidity())
    sense_data.append(sense.get_pressure())

    # direction in relation to horizontal plane
    o = sense.get_orientation()
    yaw = o["yaw"]
    pitch = o["pitch"]
    roll = o["roll"]
    sense_data.extend([pitch,roll,yaw])

    # get magnometer data
    mag = sense.get_compass_raw()
    mag_x = mag["x"]
    mag_y = mag["y"]
    mag_z = mag["z"]
    sense_data.extend([mag_x,mag_y,mag_z])

    # get accelerometer data (non-gravitational acceleration)
    acc = sense.get_accelerometer_raw()
    x = acc["x"]
    y = acc["y"]
    z = acc["z"]
    sense_data.extend([x,y,z])

    # get 3 axis gyro rate of change data (degrees per second)
    gyro = sense.get_gyroscope_raw()
    gyro_x = gyro["x"]
    gyro_y = gyro["y"]
    gyro_z = gyro["z"]
    sense_data.extend([gyro_x,gyro_y,gyro_z])

    return sense_data

# used at the moment to assist with basic headless device control
def joystickEventHandling(event):
    if event.action == ACTION_PRESSED:

        # Check which direction
        # directions as follows:
            #   L=towards LED matrix, D=towards hdmi cable
            #   R=towards ethernet port, U=towards GPIO
        if event.direction == "up":
            # run the shutdown sequence
            sense.show_letter("U")      # Up arrow
            sense.clear()       
            os.system("sudo shutdown now -P")
            sleep(20)
            
        elif event.direction == "down":
            # run the stop logging sequence
            sense.show_letter("D")      # Down arrow
            sense.clear()
            raise SystemExit
            sleep(10)

        # left in for now, but redundant/do nothing    
        elif event.direction == "left":
            sense.show_letter("L")      # Left arrow
        elif event.direction == "right":
            sense.show_letter("R")      # Right arrow
        elif event.direction == "middle":
            sense.show_letter("M")      # Enter key
            
        
        # Wait a while and then clear the screen
        sleep(0.5)
        sense.clear()

# Define some colours for led matrix display
blue = (0, 0, 255)
yellow = (255, 255, 0)

# main program prep
sense = SenseHat()
batch_data= [] # used to store collected data pre file write


#
# main program start

while True:
    # display LED matrix so i know the scripts are running when device headless
    sense.show_message("+", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
    sleep(1) # collect data every 1sec

    # get the data and log it formatted
    sense_data = get_sense_data()
    log_data()

    # have we enough data to write it to file?         
    if len(batch_data) >= WRITE_FREQUENCY:

        # show me something different so i know when data is being written
        sense.show_message("+", text_colour=blue, back_colour=yellow, scroll_speed=0.05)

        # write the batched data to file
        with open(FILENAME,"a") as f:
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []

        # let me know when we're done writing
        sense.clear(blue) 


    # event handler from sensehat joystick for basic control of device/e.g shutdown
    events = sense.stick.get_events()
    for event in events:
        joystickEventHandling(event)


