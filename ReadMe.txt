
#************** PiBikeBox / DriveLogger **************#

# The logging scripts driveData & driveCam can be run automatically, 
# and are intended to do so, on boot if you:

# Edit the cron file to add link to startUp bash script. 
crontab -e

# Add the following line to the end of the file
@reboot bash /home/pi/DriveLogger/startUp.sh # JOB_ID_1


# 
# Some further useful commands in no specific order 
# To be run at the console e.g. pi@raspberrypi:~ $ 

# In case you need to force/ensure that both logging  
# scripts are still executable. 
sudo chmod +x /home/pi/DriveLogger/driveData.py
sudo chmod +x /home/pi/DriveLogger/driveCam.py


# IF you want to edit the startUp bash script to add further
# independent functionality/scripts at boot. 

sudo nano /home/pi/DriveLogger/startUp.sh

# The startUp.sh script currently contains:

#!/bin/sh
cd /
cd home/pi/DriveLogger/
sudo python3 driveData.py & 
sudo python3 driveCam.py &
exit 0
cd /

# Note: You need the & to make each script run in its own thread
# Without this, nothing else after this point will load.


# If find yourself having booted the Pi with the scripts
# running in the background and wish to force close them. 
# In the console type:

sudo pkill -f driveData.py^C
# To stop the data logging script

sudo pkill -f driveCam.py
# To stop the Camera logging script


# Regarding storage
# The volume of data being logged is quite high, esp with the camera
# So you might find yourself needing to point the scripts to external
# storage. 

# Find out how much space is left locally
df -h

# Find the name of your USB drive (so you can mount it)
ls -l /dev/disk/by-uuid/



# If you dont have VLC installed, you'll have omxplayer accessible also
# from the console. To play a file:
cd /home/pi/DriveLogger/driveCamClips/ # Move to clip folder
omxplayer filenameOfVideo.h264 # play one file

