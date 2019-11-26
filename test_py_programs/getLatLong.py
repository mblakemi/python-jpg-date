# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 20:56:51 2019

@author: Michael
"""
# note needed to use 'pip install exifread' at Anaconda prompt

import exifread
import os
from PIL import Image
from PIL import ExifTags

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
#    print 'convert value=', value
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
    print 'image file =', image_file
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags 


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
    for key in pil_exif[34853].keys():
        decode = ExifTags.GPSTAGS.get(key,key)
        gpsinfo[decode] = pil_exif[34853][key]

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

#image_file = 'geophoto/IMG_4646.JPG'
#lat, long = get_exif_location(get_exif_data(image_file))
#print 'lat,long = ', lat, long

path = 'geophoto/'
count = 0
for (dirname, dirs, files) in os.walk(path):
    print ('DIR:', dirname)
    for file in files:
##        if not file.endswith('jpg'):
##            contin
        sfilename = path + file
        lat, lon = get_exif_location(get_exif_data(sfilename))        
        print file, lat,lon
        
        pil_exif = Image.open(sfilename)._getexif()           
        plat, plon = get_gpsinfo_location(pil_exif)
        
        print 'Pil: Lat,Lon', lat, lon
        print '***** delta lat, lon', plat-lat, plon-lon
        
#        value = gpsinfo['GPSLongitude']
#        print value
#        print pill_convert_to_degress(value)
#        print gpsinfo['GPSLatitude']
#        print pill_convert_to_degress(gpsinfo['GPSLatitude']) 
        count += 1
        if (count > 18):
            break
        
        


