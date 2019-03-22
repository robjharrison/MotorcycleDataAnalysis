#
# driveCam.py
# 23/03/2019
#
# Record timestamped video clips in 5min segments
# Motion data array simultaneously recorded
# Filename convention: yymmddhhmmss.h264 / yymmddhhmmss_motion.data

# Reference/guidance at: https://picamera.readthedocs.io/en/release-1.13/

import picamera
import datetime as dt

# set default locations for resultant files
camClipsLocation = "/home/pi/DriveLogger/driveCamClips/"
motionClipsLocation = "/home/pi/DriveLogger/driveMotionClips/"

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 30
    # set up the in-footage timestamps
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    while True:
        start = dt.datetime.now()
        # following ca =n also be achieved with picamera {timestamp:%H-%M-%S-%f}   
        timestamp = start.strftime("%y%m%d_%H_%M_%S")
        # Tell picam where to put camera/motionData clips and filenaming
        camera.start_recording(camClipsLocation + timestamp+'.h264', motion_output=motionClipsLocation+timestamp+'motion.data')
        while (dt.datetime.now() - start).seconds < 60*5: # 5 min segments
            # Add the in-footage timestamp heading
            camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
            
        # stop once 5min limit+keyframe reached
        camera.stop_recording()


## Playback commandline reference
## omxplayer videoFilename.h264

