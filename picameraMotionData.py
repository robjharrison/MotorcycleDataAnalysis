
from __future__ import division

import numpy as np

## Example
##width = 640
##height = 480

# These must match the video/camera resolution settings
width = 1280
height = 720

motionDataFile = 'EXAMPLEmotion.data'

cols = (width + 15) // 16
cols += 1 # there's always an extra column
rows = (height + 15) // 16

motion_data = np.fromfile(
    motionDataFile, dtype=[
        ('x', 'i1'),
        ('y', 'i1'),
        ('sad', 'u2'),
        ])
frames = motion_data.shape[0] // (cols * rows)
motion_data = motion_data.reshape((frames, rows, cols))

# Access the data for the first frame
print(motion_data[0])

# Access just the x-vectors from the fifth frame
print(motion_data[4]['x'])

# Access SAD values for the tenth frame
print(motion_data[9]['sad'])
