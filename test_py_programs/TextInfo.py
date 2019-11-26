# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:09:27 2019

@author: Michael
"""

import exifread
import os
import sys
import re
import datetime
import math

gpath = 'in/temp/'
print 'gpath=',gpath

for (dirname, dirs, files) in os.walk(gpath):
    print ('DIR:', dirname)
    for file in files:
##        if not file.endswith('jpg'):
##            continue
        exif_data = get_exif_data(gpath + file)
        print file + ':'
        print exif_data
        
        
        