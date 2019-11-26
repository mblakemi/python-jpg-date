#print files not starting with 19 or 20
import os
import re

path = 'temp\\'
path = 'photos\\'
count = 0
for (dirname, dirs, files) in os.walk(path):
    print ('DIR:', dirname)
    for file in files:
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
            os.rename(path+file, path+newstr)
print str(count)+' Renamed'

            

 
