# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 20:56:51 2019

@author: Michael
"""
# note needed to use 'pip install exifread' at Anaconda prompt

import exifread
import os
import sys
import re
import datetime
import math

"""
Set up gpath as the path to the geo information photos
name.jpg
for the default radius of .1 miles
or 
name@1.5.jpg
for a radius of 1.5 miles

Set up path as the path to the photos to rename
Note, you should run DatetoName.py first to add dates
"""

gpath = 'geophoto/'
print 'gpath=',gpath

path = 'photos/'
print 'path=',path

# based on https://gist.github.com/erans/983821

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)
    
def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon

def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags 

def getxyz(lat, long):
    rad_lat = lat * math.pi/180.
    rad_long = long * math.pi/180.
    rxy = math.cos(rad_lat)
    x = rxy * math.cos(rad_long)
    y = rxy * math.sin(rad_long)
    z = math.sin(rad_lat)
    return (x,y,z)


count = 0
dict = {}
for (dirname, dirs, files) in os.walk(gpath):
    print ('DIR:', dirname)
    for file in files:
##        if not file.endswith('jpg'):
##            continue
        exif_data = get_exif_data(gpath + file)
        lat, long = get_exif_location(exif_data) 
        xyz = getxyz(lat, long)
        rad = .1
        iat = file.find('@')
        if iat >= 0:
            rest = file[iat+1:].upper()
            gname = file[:iat]
            ijpg = rest.find('.JPG')
            if (ijpg):
                rad = float(rest[:ijpg])
        else:
            # no extra
            idot = file.find('.')
            if idot >= 0:
                gname = file[:idot]
            else:
                gname = file
        print 'name', gname, ' rad=', rad

        dict.update([(gname, (xyz, rad))])
        
#        dt = str(exif_data['EXIF DateTimeOriginal'])  # might be different
#        print 'dt= ', dt
        print file, lat,long
        
for key,val in dict.iteritems():
    print key, val
    
def worlddist(xyz1, xyz2):
    dcos = xyz1[0] * xyz2[0] + xyz1[1] * xyz2[1] + xyz1[2] * xyz2[2]
    if dcos > 1.0:
        dcos = 1.0
    dx = 3959 * math.acos(dcos)
    return dx
        

for (dirname, dirs, files) in os.walk(path):
    print ('DIR:', dirname)
    for file in files:
##        if not file.endswith('jpg'):
##            continue
        exif_data = get_exif_data(path + file)
        lat, long = get_exif_location(exif_data)
        gname = 'Unknown'
        dxclose = 1e8
        # sometimes iPhone doesn't add GPS
        if lat != None:
            pxyz = getxyz(lat, long)
            # check dict for closest location within limit
            for key,val in dict.iteritems():
                wdx = worlddist(pxyz, val[0])
                if (wdx < dxclose):
                    # would be new close
                    if val[1]< 0.0 or wdx < val[1]:
                        # update closest value
                        gname = key
                        dxclose = wdx
                        #print 'gname, wdx', gname, wdx
        
        # should have name to update this photo
        if gname == 'Unknown':
            print file, ' is in ', gname
        
        oldfile = file
        iplace = oldfile.find('@')
        if (iplace >=0):
            newfile = oldfile[:iplace] + '@' + gname + '.jpg'
        else:
            # just strip off .jpg
            ijpg = oldfile.lower().find('.jpg')
            if ijpg >= 0:
                newfile = oldfile[:ijpg] + '@' + gname + '.jpg'
            else:
                print '*** Not JPG so not changed:' + oldfile
                continue
            
        os.rename(path + oldfile, path + newfile)
        
        
