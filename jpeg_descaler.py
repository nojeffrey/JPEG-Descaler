#!/usr/bin/env python

"""
Descale JPEG images to a maximum of 1000px on longest edge.
Eg if a JPEG is 900x700, it wont be touched, if a JPEG is 3000x1800, it will be resized to 1000x600, etc
Useful for wordpress installs that have GB's of really large images.
Take a backup, then place this script in /wp-content/uploads/ and run.
"""

import os, subprocess
from PIL import Image

before = subprocess.check_output(["du", "-h", ".", "--max-depth=0"]) 
listofjpegs = []

for root, dirs, files in os.walk(".", topdown=True):
    for name in files:
        if name[-3:] == 'jpg' or name[-3:] == 'peg' or name[-3:] == 'JPG' or name[-3:] == 'PEG':
            listofjpegs.append(os.path.join(root, name))

for i in listofjpegs:
    try:
        #incase some file ends with pg, but isn't and jpeg.
        im = Image.open(i)
    except IOError:
        pass
    if im.size[0] > 1000 or im.size[1] > 1000:
        subprocess.call(["mogrify", "-resize", "1000x1000", i])
        print "Resized", i


after = subprocess.check_output(["du", "-h", ".", "--max-depth=0"])                                              
print "Original size: %sAfter resizing: %s" %(before,after)
