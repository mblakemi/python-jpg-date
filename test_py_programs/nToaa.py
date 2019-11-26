#dir directories
import os,sys
from PIL import Image
import re
import datetime


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
   
##mylist = [' b 1', ' a 2', 'bb 3', ' c 4', ' b 5', 'aa 6']
##mylist.sort()
##for a in mylist:
##    print (a)

nlist = [1,4,25,26,27, 100, 500, 1000, 1500]
ntext = []
for n in nlist:
    ntext.append(nToAA(n))
ntestsort = ntext.copy()
ntestsort.sort()
i = 0
for v in ntext:
    print(v, ntestsort[i])
    i += 1

filename = '2016-12-20 03-00-35 P1070664.JPG'
# check that correct ####-##-## ##-##-## format
found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (.*?) \d\d\d\.(...$)', filename)
bOK = True
if len(found) == 0:
    # check for panasonic
    found = re.findall('^(\d\d\d\d-\d\d-\d\d )(\d\d)-(\d\d)-\d\d (P)\d+\.(...$)', filename)
    if len(found) == 0:
        bOK = False
if (bOK):
    d, h, m, name, ext = found[0]
        

