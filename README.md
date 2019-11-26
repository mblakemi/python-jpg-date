# python-jpg-date
Python programs: 

## DatetoName.py
This program uses the date taken from the jpg file and adds it to the filename. It allows the standard sort to on filename to also sort by date. The format is:
yyyy-mm-dddd hh x
where hh is the hour in 24 hour notation and x is a-z based on the time the photo was taken during the hour. If more that 24 photos were taken, then hhxx is used where xx starts at aa, ab .... zz. This scheme allows up to 700 photos with unique date prefixes to be generated for each hour. The x or xx allows the photos to be sorted by date.

See 'Photo_Processing.docx' for more details


## NametoJPG.py
This program reads the files from the input directory and generates new output file (in the 'out' directory) with the first 10 characters displayed on the photo in the upper left corner. If it is used after DatetoName.py, then the date is displayed on the photo. This is useful when lots of family photos are displayed on a photo frame that cycles through the photos. Note, the generated photos do not include JPG information (date, gps info etc.)

See 'Photo_Processing.docx' for more details

## Compress.py
This program uses the same algorithm as NametoJPG.py but doesn't change the photo. The new photos are compressed jpg photo and do not include JPG information (date, gps info etc.). It uses CompressIn as the input directory and CompressOut as the output directory.

## AtLocation.py

Atlocation allows the location of a photo to be added to the name of photos. GEO information from jpg photos named for location (e.g. ScienceMuseum.jpg) is stored in the 'geophoto' folder and the names from the closest photo (within range - see below) are added after the end of the filenames in the 'photo' folder. If the filename already has a '@', the old location is discarded and replaced by the new location.

This program uses the file name in the 'geophoto' directory to rename jpg files in the 'photo' directory. The filename up to a '@' is the geographical name used and an optional '@fff' where fff is a number with an optional decimal point as a location standard with the range specified as fff. If no range is given, the default is .1 miles. 

For each photo in the 'photo' directory, the geographical distance to the photos is the geophoto directory are calculated. For the photos within the range (.1 miles or the specified range), a '@' character and the name from the closest photo in the geophoto directory is added to the photo in the 'photo' directory. If no photos are within the specified range, then '@unknown' is added. If the name of the current photo already includes an '@' character, that character and the rest of the file name is removed before adding an updated '@location'.

See AtLocation.docx for more details.

## FindClose.py

This program is used to search multiple sub-folders of jpg files to determine if they are close to jpg file in a geo information folder. Note that the search is recursive so sub-folders of sub-folders of the path specified by 'path=' are searched.

The searched folder path is defined by 'path=' in the program. The folder of jpg files with geo information is specified by 'gpath=' in the program. The maximum allowed distance from the geo information jpg files is .1 miles unless the name ends with @ and a distance in miles. For example, 
Home.jpg would be matched with any jpg file within .1 miles of Home.jpg.
Park@1.5.jpg would be matched with any jpg file within 1.5 miles of Park@1.5.jpg.

Typical output would be:
Dir: e:/Old Photo/65 Old Photo/2019-03-31 MarD Spain has 271
No GPS:30  out count = 15137
Madrid Thyssen has 204
Madrid Reina Sofia has 67

which shows that 204 photos in the 'e:/Old Photo/65 Old Photo/2019-03-31 MarD Spain has 271' folder were close to 'Madrid Thyssen.jpg' in the geo information folder and 67 photos in the 'e:/Old Photo/65 Old Photo/2019-03-31 MarD Spain has 271' folder were close to 'Madrid Reina Sofia.jpg' in the geo information folder.

For a simple test, copy the ShortTest folder to the photos folder and run FindClose.py. The output should be:
gpath= geophoto/
path= photos
pathfile= geophoto/Michigan@1.5.JPG
name Michigan  rad= 1.5
Michigan@1.5.JPG 42.2768472222 -83.7416388889
Michigan ((0.0806582572458013, -0.7354934980094948, 0.6727135794109017), 1.5)


Dir: photos\ShortTest has 1
No GPS:1  out count = 1
Michigan has 1

The information from the gpath jpg files are displayed first. Finally, ShortTest has 1 match and the match is for the Michigan@???.jpg file.

