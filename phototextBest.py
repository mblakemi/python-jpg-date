#dir directories
#Python 3.5 version
#17-04-13 move name down for Blake Kitchen frame, only use date
#17-04-13 Single color (255,0,255)
#17-04-13 Recursive process from sIndir to sOutDir
#19-04-12 Added Rotate option based on EXIF info

import os,sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
bDebugReport = False

# Note either use 'out' as sOutDir and the parent directories to
# be converted or use sFolder as the folder to be converted and
# explicitly create this directory in out

sFolder = '0temp' # '2018'
# Recursive in directory (no not use trailing \\'
#sIndir = 'e:\\temp\\in'
sIndir = 'e:\\Archive\\Best Photo\\Best Photo 5\\' + sFolder
sIndir = 'E:\\Temp\\Photos'
#sIndir = 'e:\\Archive\\Best Photo\\Best Photo 1\\Selected HiRes'
#sIndir = 'Rotate'
sIndir = 'in'


sOutDir = 'out\\' + sFolder
sOutDir = 'out'

ivalR = 255
ivalG = 0
ivalB = 255
colLightRGB = (255,255,255) #was (200,200,255)
colDarkRGB = (0,0,200)
colMiddleRGB = (0,255,0) #(255,80,0)
colMinBlue = (0,0,255)
colMinGreen = (0, 255, 0)
colMinRed = (255, 0, 0)

bOnlyAddDate = True
def avg_pix(img, fline):
  imax = 200
  #don't check more than 1/4 way
  width, height = img.size
  if imax > width/4:
    imax = int(width/4)
    
  rsum = 0
  gsum = 0
  bsum = 0
  ntot = 0
  iline = int(fline)
  try:
    for iy in range(iline-1, iline+2):
      for ix in range(0,imax):
        r,g,b = img.getpixel((ix, iy))
        ntot += 1
        rsum += r
        gsum += g
        bsum += b
        
    avg = int((rsum + gsum + bsum)/(3 * ntot))
  except:
    return (200, 200,200,200)
  
  return (avg, int(rsum/ntot), int(gsum/ntot), int(bsum/ntot))

def imageRotation(fname):
    image_info = Image.open(fname)._getexif()
    if image_info == None:
        return 1
    key = 0x0112
    if key in image_info:
        return image_info[key]
    return 1

def add_photo_text(in_dir_name, out_dir_name, in_name):
  sInFileName = in_dir_name + in_name
  try:
    img = Image.open(sInFileName)
  except:
    print('Not photo: [' + sInFileName+ ']')
    return
  # Use EXIF info to rotate image if necessary
  iRotate = imageRotation(sInFileName)
  if iRotate == 6:
    transposed  = img.transpose(Image.ROTATE_270)
    print 'Rotated 270'
    img = transposed
  elif iRotate == 3:
    transposed  = img.transpose(Image.ROTATE_180)
    print 'Rotated 180'
    img = transposed
  elif iRotate == 8:
    transposed  = img.transpose(Image.ROTATE_90)
    print 'Rotated 90'
    img = transposed
  elif iRotate != 1:
    print '***** NOT RECOGNIZED ROTATION ***** = ', iRotate
  width, height = img.size
  try:
      draw = ImageDraw.Draw(img)
  except:
      print ('**********')
      print ('Could not Draw: ' + sInFileName)
      print ('**********')
      return
  # font = ImageFont.truetype(<font-file>, <font-size>)
  # this works reasonably well for text to be half way across
  smax = max(width, height)
  fsize = int(smax/30)
  iystart = fsize
  
  if height < width:
      iystart = int(fsize/2)

  font = ImageFont.truetype('Arialbd.ttf',fsize)
  #font = ImageFont.load_default().font

  # use black if very light
  (avg, ravg, gavg, bavg) = avg_pix(img, iystart + fsize/2)
  if bDebugReport:
    print("aRGB=",avg, ravg, gavg, bavg)
  colRGB = colMiddleRGB 
  if avg < 140:
    colRGB = colLightRGB
  elif avg > 159:
    colRGB = colDarkRGB
  else:
    # assign minimum color
    if ravg < gavg:
      if ravg < bavg * 1.5:
        colRGB = colMinRed
      else:
        colRGB = colMinBlue
    else:
      if gavg < bavg * 1.5:
        colRGB = colMinGreen
      else:
        colRGB = colMinBlue
  if bDebugReport:
    print (colRGB)
         
  # draw.text((x, y),"Sample Text",(r,g,b))
  stext=''
  # trim off .jpg or .xxx from text file
  if in_name[-4] == '.':
    photo_text = in_name[:-4]
    if (bOnlyAddDate):
      photo_text = in_name[0:10]
#    print('iy', iystart, fsize)
    draw.text((0, iystart),photo_text,colRGB,font=font)
  else :
    print('Did not recognize file type: ' + in_name)
  img.save(out_dir_name + in_name)

#
# Recursive routine to process directory and sub directories
#

def process_dir(sIndir, sOutdir, sFile):
  sFileDir = sIndir + sFile
  if os.path.isfile(sFileDir):
    print ('Processing file: '+ sFileDir)
    add_photo_text(sIndir, sOutdir, sFile)
    return
  # must be a directory
  sOutdirNew = sOutdir + sFile + "\\"
  sIndirNew = sFileDir + "\\"
  # create it if necessary
  try: 
    os.makedirs(sOutdirNew)
  except OSError:
    if not os.path.isdir(sOutdirNew):
        raise
  print ('--Processing Directory: '+ sIndirNew) 
  dirs = os.listdir(sIndirNew)
  for file in dirs:
    process_dir(sIndirNew, sOutdirNew, file)

#
# process all files in sIndir (no \\ at the end)
#
process_dir(sIndir, sOutDir + '\\', '')





    
