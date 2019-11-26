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

"""
Set up gpath as the path to the geo information photos
name.jpg
for the default radius of .1 miles
or 
name@1.5.jpg
for a radius of 1.5 miles

Set up path as the path to the photos to rename
Note, you should run DatetoName.py first to add dates

2019-04-13 Changed to use PIL import for GPS info
2019-04-14 Modified to not use subdirectory files in gpath
and to also remove iPhone and Panasonic photo names
"""

gpath = 'geophoto/'
print 'gpath=',gpath

path = 'photos/'
print 'path=',path

bRemoveShortName = False #skip removing original iPhone names if False

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
        

for (dirname, dirs, files) in os.walk(path):
    print ('DIR:', dirname)
    for file in files:
        if os.path.isdir(path + file):
            continue
        if not file.lower().endswith('jpg'):
            continue
#        exif_data = get_exif_data(path + file)
#        lat, long = get_exif_location(exif_data)
        oldpathname = os.path.join(dirname, file)
        
        try:
            pil_exif = Image.open(oldpathname)._getexif()           
            lat, long = get_gpsinfo_location(pil_exif)
        except IOError:
            print 'Cannot open image for: ' + oldpathname
            continue
        except AttributeError:
            print 'Cannot get GEO info for: ' + oldpathname
            continue            
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
        newpathfile = os.path.join(dirname, newfile)
            
        os.rename(oldpathname, newpathfile)
        
 #### ------ now remove original iPhone or Panasonic photo id 
if bRemoveShortName:	    
    count = 0
    print 'Removing original iPhone IMG_#### text from name'
    for (dirname, dirs, files) in os.walk(path):
        print ('DIR:', dirname)
        for file in files:
            if file.upper().endswith('PNG'):
                continue
    ##        if not file.endswith('jpg'):
    ##            continue
    #        print(file)
    #        found = re.findall('(IMG_\d\d\d\d)', file)
            newstr = None
            found = re.search('(IMG_\d\d\d\d)', file)
            if found == None:
                found = re.search('(P\d+)', file)
            if found != None:
                istart = found.start()
                if file[istart-1]==' ' and file[istart-2]== ' ':
                    istart = istart - 1;
                newstr = file[:istart] + file[found.end():]
            if newstr != None:
                count += 1
     #           print newstr
                oldpathname = os.path.join(dirname, file)
                newpathname = os.path.join(dirname, newstr)
                os.rename(oldpathname, newpathname)
    print str(count)+' Renamed'
else:
    print 'Iphone text IMG_#### not removed from name'