#dir directories
import re
from datetime import date, timedelta, datetime
import sys
bSkipShorten = 0

d = datetime(2016, 1, 1, 2)
h = -7

delt = timedelta(0,h*60*60)
print (d)
print (d + delt, ' later by', h, 'hours')


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

# quit() # this exits interpreter
if bSkipShorten:
    sys.exit('skip shorten part')

ad ='%02d-%02d-%02d ' % (d.year, d.month, d.day)
ah = '%02d' % d.hour
print(ad, ah, '+', h)
(ad1, ah1) = FixPana(ad, ah, h)
print(ad1, ah1)

