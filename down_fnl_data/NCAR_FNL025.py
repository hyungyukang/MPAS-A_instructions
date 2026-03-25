#!/usr/bin/env python
"""
Python script to download selected files from rda.ucar.edu.
After you save the file, don't forget to make it executable
i.e. - "chmod 755 <name_of_script>"

Reference: https://gdex.ucar.edu/datasets/d083003/
"""
import sys, os
from urllib.request import build_opener
import datetime

#======================================================#
startdate = datetime.date(2024,9,25)
starthour = datetime.time(0, 0, 0)
                        #HH MM DD
enddate = datetime.date(2024,9,25)
endhour = datetime.time(0, 0, 0)
                      #HH MM DD
timeInterval = 6 # hours

starttime = datetime.datetime.combine(startdate,starthour)
endtime = datetime.datetime.combine(enddate,endhour)

nexttime = starttime
#======================================================#

dh = 0

site_fnl025="https://data.rda.ucar.edu/d083003"
file_prim="gdas1.fnl0p25."
file_sub=".f00.grib2"

while (nexttime <= endtime):

   # Date & file name -----------------------------------

   yyyy=nexttime.strftime('%Y')
   mm=nexttime.strftime('%m')
   dd=nexttime.strftime('%d')
   hh=nexttime.strftime('%H')
   datehh = yyyy+mm+dd+hh

   site = site_fnl025+"/"+yyyy+"/"+yyyy+mm+"/"
   fname = site+file_prim+datehh+file_sub

   filelist = [
     fname
   ]

   opener = build_opener()

   for file in filelist:
       ofile = os.path.basename(file)
       sys.stdout.write("downloading " + ofile + " ... ")
       sys.stdout.flush()
       infile = opener.open(file)
       outfile = open(ofile, "wb")
       outfile.write(infile.read())
       outfile.close()
       sys.stdout.write("done\n")

   dh += timeInterval

   nexttime = starttime + datetime.timedelta(hours=dh)

   if ( nexttime > endtime ): break

#======================================================#
