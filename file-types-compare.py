from dupefinder import *
from hashmaker import *
from dupe_dupe_checker import *
import time, datetime

print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
filetypes = [".jpg", ".gif", ".mov", ".mp4", ".png"]



hashmaker("hashfile.csv", filetypes, "/")

print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
	

for filetype in filetypes:
	startTime = time.time()
	filename = "dupes-{filetype}.csv".format(filetype=filetype.replace(".", ""))
	dupefinder("hashfile.csv", filename, filetype)
	dedupe(filename)
	print ("{filetype} completed in {time}".format(filetype=filetype, time=time.time() - startTime))