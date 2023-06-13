from dupefinder import *
from hashmaker import *
import time, datetime

print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
filetypes = [".gif"]



hashmaker("hashfile.csv", filetypes, "/Users/nickpiegari/Documents")

print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
	

for filetype in filetypes:
	startTime = time.time()
	dupefinder("hashfile.csv", "dupes-{filetype}.csv".format(filetype=filetype.replace(".", "")), filetype)
	print ("{filetype} completed in {time}".format(filetype=filetype, time=time.time() - startTime))