import os, csv
from hashmaker import *

fileextensions = {}

for root, dirs, files in os.walk("/Users/nickpiegari"):
	for file in files:
		ext = os.path.splitext(file)[1].lower()
		path = os.path.join(root, file)
  
		try:
			filesize = os.path.getsize(path)
		except:
			filesize = 0
   
		try:
			hash = makeOneHash(path)
		except:
			hash = 0
   
		if path.find(".bzvol") == -1 and path.find("$Recycle") == -1 and path.find(".com") == -1 and path.find(".Spotlight") == -1 and path.find(".Volume") == -1 and path.find(".DS") == -1:
			if ext not in fileextensions:
				fileextensions[ext] = {"count": 1, "filesize": filesize, "hash": hash}
				print ("found file type: {ext}".format(ext=ext))
				with open("filetypes/filetype-{ext}.csv".format(ext=ext[1:]), "w") as rofl:
					rofl.write("\"{path}\",{size},{hash}\n".format(path=path.replace("\"","'"),size=filesize, hash=hash))
			else:
				fileextensions[ext]["count"] += 1
				fileextensions[ext]["filesize"] += filesize
				fileextensions[ext]["hash"] = hash
				with open("filetypes/filetype-{ext}.csv".format(ext=ext[1:]), "a") as rofl:
					rofl.write("\"{path}\",{size},{hash}\n".format(path=path.replace("\"","'"),size=filesize,hash=hash))
	
	
with open("filetype-list.csv", "w") as tehfile:
	writer = csv.writer(tehfile)
	for ext, count in fileextensions.items():
		writer.writerow([ext, count["count"], count["filesize"]])
