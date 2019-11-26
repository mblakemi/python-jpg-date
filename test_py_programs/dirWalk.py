#print files not starting with 19 or 20
import os,sys
from PIL import Image
import re
from datetime import date, timedelta, datetime

path = 'temp\\'
count = 0
for (dirname, dirs, files) in os.walk(path):
    print ('DIR:', dirname)
    for file in files:
##        if not file.endswith('jpg'):
##            continue
        print(file)
#        found = re.findall('(IMG_\d\d\d\d)', file)
        found = re.search('(IMG_\d\d\d\d)', file)
        print found
        if found != None:
            newstr = file[:found.start()] + file[found.end():]
            print newstr

 
