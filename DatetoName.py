#dir directories
import os,sys
from PIL import Image
import re
from datetime import timedelta, datetime

# 2017-10-18 AVI and MTS converted like MOV with last modified date

# **** Notes 2018 *****
# For large Old Photo files, move to E:/Temp/Photos and use this
# as the path, then move back.
# For a few folders (so easy to copy) use photos/in/ and move
# to this folder.
# *** you may also want to delete .aae files if any show up
# *** .png files are NOT renamed, you can do this manually

# path = 'photos\\in\\'
path = 'E:\\Temp\\Photos'
path = 'photos\\'
path = 'in_name'
# path = 'C:\\Archive\\2017'
nPanaOffset = 0 # hour offset for panasonic camera 7 early germany
if nPanaOffset != 0:
    print ('Panasonic hour offset is', nPanaOffset)
    
nNonJpgOffset = 0 # hours offset for non jpg files
if nNonJpgOffset != 0:
    print ('Non Offset hour offset is', nNonJpgOffset)
     
    
bSkipShorten = 0

def nToAA(ival):
# first 26 are ' a' - ' z', then 'aa' to 'zz'
# after 26*26 = 676 then three digits and doesn't sort correctly
    sret = chr(ord('a') + (ival % 26))
    iupper = int(ival / 26)
    sret = chr(ord('a') + (ival % 26))
    if iupper == 0:
        return ' ' + sret
    while (iupper):
        ival = int(iupper % 26)
        iupper = int(iupper / 26)
        sret = chr(ord('a') + (ival % 26) - 1) + sret
    return sret

def getFileDateTime(filename):
    mtime = os.path.getmtime(filename)
    ds = datetime.fromtimestamp(mtime)
    ds += timedelta(0, 60*60*nNonJpgOffset)
    sdate = '%02d-%02d-%02d %02d-%02d-%02d' % \
            (ds.year, ds.month, ds.day, ds.hour, ds.minute, ds.second)
    return sdate

def getFileDateHourMin(filename):
    mtime = os.path.getmtime(filename) 
    ds = datetime.fromtimestamp(mtime)
    ds += timedelta(0, 60*60*nNonJpgOffset)
    
    sdate = '%02d-%02d-%02d %02dh%02dm' % \
            (ds.year, ds.month, ds.day, ds.hour, ds.minute)
    return sdate

def FixPana(d,h,nPanaOffset):
    nh = int(h) + nPanaOffset
    anh = '%02d' % nh
    if (nh >= 0 and nh < 24):
        return (d, anh)
    # need to use more complicated date time calculation
    found = re.findall('^(\d\d\d\d)-(\d\d)-(\d\d )', d)
    if len(found) == 0:
        return (d, anh)
    (yy, mm, dd) = found[0]
    ds = datetime(int(yy), int(mm), int(dd), int(h))
    ds += timedelta(0, nPanaOffset*60*60)
    ad ='%02d-%02d-%02d ' % (ds.year, ds.month, ds.day)
    anh = '%02d' % ds.hour
    return (ad, anh)


count = 0
mcount = 0
oldcount = 0
mskipyear = 0
for (dirname, dirs, files) in os.walk(path):
    print('Checking:', dirname)
    for filename in files:
        #check for old format and change
        found = re.findall('^(\d\d\d\d \d\d \d\d)( .+\....$)', filename)
        if len(found)>0:
            (d,r) = found[0]
            oldpathname = os.path.join(dirname, filename)
            try:
                dtake = Image.open(oldpathname)._getexif()[36867]
            except:
                dtake = getFileDateTime(oldpathname)
            newname = dtake.replace(':','-') + r
            newpathname = os.path.join(dirname, newname)
            os.rename(oldpathname, newpathname)
            oldcount += 1
            continue
             
        # skip if start 19 or 20
        if filename.startswith('19') or filename.startswith('20'):
            mskipyear += 1
            # print ('***skipped:', dirname, filename)
            continue
        
        #handle Movies using modified time
        if filename.endswith('.mov'):
            filename = filename[:-3]+'MOV'
        if filename.endswith('.MOV'):
            oldpathname = os.path.join(dirname, filename)
            # sdate = getFileDateHourMin(oldpathname)
            sdate = getFileDateTime(oldpathname)          
            newname = sdate + ' ' + filename
            newpathname = os.path.join(dirname, newname)
            os.rename(oldpathname, newpathname)
            print (newpathname)
            mcount += 1
            continue
        
          #handle AVI Movies using modified time
        if filename.endswith('.avi'):
            filename = filename[:-3]+'AVI'
        if filename.endswith('.AVI'):
            oldpathname = os.path.join(dirname, filename)
            sdate = getFileDateHourMin(oldpathname)
            newname = sdate + ' ' + filename
            newpathname = os.path.join(dirname, newname)
            os.rename(oldpathname, newpathname)
            print (newpathname)
            mcount += 1
            continue      
 
          #handle MTS Movies using modified time
        if filename.endswith('.mts'):
            filename = filename[:-3]+'MTS'
        if filename.endswith('.MTS'):
            oldpathname = os.path.join(dirname, filename)
            sdate = getFileDateHourMin(oldpathname)
            newname = sdate + ' ' + filename
            newpathname = os.path.join(dirname, newname)
            os.rename(oldpathname, newpathname)
            print (newpathname)
            mcount += 1
            continue     
                
        # now handle jpg or .JPG                            
        if filename.endswith('.jpg'):
            filename = filename[:-3]+'JPG'
        if not filename.endswith('.JPG'):
            print ('not JPG:', filename)
            continue
        oldpathname = os.path.join(dirname, filename)
        try:
            dtake = Image.open(oldpathname)._getexif()[36867]
        except:
            dtake = getFileDateTime(oldpathname)
            print ('Used file date', oldpathname)

        # has date taken, change name
        newname = dtake.replace(':','-') + ' ' + filename
        newpathname = os.path.join(dirname, newname)
        os.rename(oldpathname, newpathname)
        count += 1
print (count, 'JPG files changed.')
if (mcount):
    print(mcount, 'MOV AVI or MTS files changed')
if (mskipyear):
    print(mskipyear, 'Skipped as start with 19 or 20')
if oldcount:
    print(oldcount,' old #### ## ## files redone')
            
# now shorten names to A-X for hour taken then a-z for order per hour
# adjust time for panasonic if necessary
# bSkipShorten = True
if bSkipShorten:
    sys.exit('skip shorten part')

for (dirname, dirs, files) in os.walk(path):
    oldRoot = ''
    ndup = 0
    files.sort()
    for filename in files:
        if filename.endswith('.jpg'):
            filename = filename[:-3]+'JPG'           
        # skip if not start 19 or 20
        if not filename.endswith('.JPG') and not filename.endswith('.MOV'):
            continue
        if not filename.startswith('19') and not filename.startswith('20'):
            continue
        #check for old format and change to new
        found = re.findall('^(\d\d\d\d \d\d \d\d)( .+\....$)', filename)
        if len(found)>0:
            (d,r) = found[0]
            newname = d.replace(' ', '-') + r
            print('- replaced:', newname)
            newpathname = os.path.join(dirname, newname)
            oldpathname = os.path.join(dirname, filename)
            os.rename(oldpathname, newpathname) 
            
        bIsPanasonic = False
        # check that correct ####-##-## ##-##-## format
        found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (.*?) \d\d\d\.(...$)', filename)
        #check for Kent Mission photos
##        if len(found) == 0: 
##            found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (.*?) - \d\d\d\.(...$)', filename)
        if len(found) == 0:
            # check for panasonic
            found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (P\d+)\.(...$)', filename)
            if len(found) > 0:
                bIsPanasonic = True
        #check for Canon
        if len(found) == 0:
            found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (IMG_\d+)\.(...$)', filename)
        if len(found) == 0:
            #all other files
            found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (.+)\.(...$)', filename)
        if len(found) == 0:                  
            continue
        d, h, m, name, ext = found[0]
        if bIsPanasonic and nPanaOffset != 0:
            (d,h) = FixPana(d,h,nPanaOffset)
        root = d + h
        if root == oldRoot:
            root = root + nToAA(ndup)
            ndup += 1
        else:
            oldRoot = root
            ndup = 0
            root = root + ' ' # add space if first so sorts correctly
        newname = root + ' '+ name + '.' + ext
        # print (filename, ' -> ', newname)
        oldpathname = os.path.join(dirname, filename)
        newpathname = os.path.join(dirname, newname)
        os.rename(oldpathname, newpathname)        

print ('Renamed to shorter names')

        
        
        
        


        
    
