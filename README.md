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



