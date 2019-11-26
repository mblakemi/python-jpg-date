# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 20:56:51 2019

@author: Michael
"""
# note needed to use 'pip install exifread' at Anaconda prompt

from PIL import Image
from PIL import ExifTags
import os
import sys
import re
import datetime
import math
from collections import defaultdict

"""
Set up gpath as the path to the geo information photos
name.jpg
for the default radius of .1 miles
or 
name@1.5.jpg
for a radius of 1.5 miles

"""

gpath = 'geofind/'
print 'gpath=',gpath

path = 'e:/Old Photo/01 Art Museums/DC National Gallery 60 b DC/'
#path = 'e:/Old Photo/01 Art Museums/'
path = 'e:/Old Photo/'
#path = 'e:/Old Photo/65 Old Photo/'
#path = 'e:/Old Photo/61 Old Photos - Kent Carol/'
print 'path=',path

# based on https://gist.github.com/erans/983821

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def pill_convert_to_degress(values):
#    print 'pil value=', values
    d = float(values[0][0])/ float(values[0][1])
    m = float(values[1][0])/ float(values[1][1])
    s = float(values[2][0])/ float(values[2][1])
    return d + (m / 60.0) + (s / 3600.0)

def get_gpsinfo_location(pil_exif):
    lat = None
    lon = None
    
    gpsinfo = {}
    try:
        for key in pil_exif[34853].keys():
            decode = ExifTags.GPSTAGS.get(key,key)
            gpsinfo[decode] = pil_exif[34853][key]
    except:
        return lat, lon

    gps_latitude = _get_if_exist(gpsinfo, 'GPSLatitude')
    gps_latitude_ref = _get_if_exist(gpsinfo, 'GPSLatitudeRef')
    gps_longitude = _get_if_exist(gpsinfo, 'GPSLongitude')
    gps_longitude_ref = _get_if_exist(gpsinfo, 'GPSLongitudeRef')
#    print 'lat ref', gps_latitude_ref
#    print 'long ref', gps_longitude_ref

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = pill_convert_to_degress(gps_latitude)
        if gps_latitude_ref != 'N':
            lat = - lat

        lon = pill_convert_to_degress(gps_longitude)
        if gps_longitude_ref != 'E':
            lon = - lon

    return lat, lon  

def getxyz(lat, long):
    rad_lat = lat * math.pi/180.
    rad_long = long * math.pi/180.
    rxy = math.cos(rad_lat)
    x = rxy * math.cos(rad_long)
    y = rxy * math.sin(rad_long)
    z = math.sin(rad_lat)
    return (x,y,z)


#### create a dictionary of files in gpath (not sub directories)
count = 0
dict = {}

# make sure path exists
if not os.path.exists(path):
    print 'Path does not exist: ' + path

#for (dirname, dirs, files) in os.walk(gpath):
#    print ('DIR:', dirname)
for file in os.listdir(gpath):
    if not file.lower().endswith('jpg'):
        continue
#        exif_data = get_exif_data(gpath + file)
#        lat, long = get_exif_location(exif_data)
    pathfile = gpath + file
    print 'pathfile=',pathfile
    pil_exif = Image.open(pathfile)._getexif()           
    lat, long = get_gpsinfo_location(pil_exif)
    # warn if Panasonic with no GPS data
    if lat > 17056800 and lat == long:
        lat = None
    if lat == None or long == None:
        print 'No Geo info for: ' + pathfile
        print '***** Exiting program ******'
        raise Exception('exit')
        
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


# raise Exception('SkipMainLoop')       
print
print

for (dirname, dirs, files) in os.walk(path):
#    print ('DIR:', dirname)
    icount = 0
    freq = defaultdict(int)
    none_count = 0
    out_count = 0
    for file in files:
        if os.path.isdir(path + file):
            continue
##        if not file.endswith('jpg'):
##            continue
#        exif_data = get_exif_data(path + file)
#        lat, long = get_exif_location(exif_data)
        # skip non .jpg files
        if not file.lower().endswith('jpg'):
            continue
        
        oldpathname = os.path.join(dirname, file)

        try:        
            pil_exif = Image.open(oldpathname)._getexif()           
            lat, long = get_gpsinfo_location(pil_exif)
        except IOError:
            print 'Error opening:' + oldpathname
            lat = None
        gname = 'Unknown'
        dxclose = 1e8
        # sometimes iPhone doesn't add GPS
        if lat == None:
            none_count += 1
        else:
            pxyz = getxyz(lat, long)
            # check dict for closest location within limit
            for key,val in dict.iteritems():
                wdx = worlddist(pxyz, val[0])
                # would be new close
#                if wdx < val[1]:
                if wdx < .5:
                    # update closest value
                    freq[key] += 1
                    icount += 1
#                    print str(wdx) + ' found ' + oldpathname
                else:
                    out_count += 1

    if icount > 0:
        print 'Dir: ' + dirname + ' has ' + str(icount)
        print 'No GPS:' + str(none_count) + '  out count = ' + str(out_count)
        for key,val in freq.iteritems():
            print key + ' has ' + str(val)
        print
        



