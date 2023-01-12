# !/usr/bin/python

# path = "/volumes/One Touch/ingest history 2 pre qc/betacam trimmed"
path = "/volumes/One Touch/ingest history 2 pre qc/betacam sp trimmed"
# path = "/volumes/One Touch/ingest history 2 pre qc/u-matic trimmed"

import os, csv, ffmpeg

videoformats = ["mov"]

with open("videolist-betacam-sp.csv", "w") as csvfile:
	rofl = csv.writer(csvfile)
	rofl.writerow(["filename", "filesize", "job", "status", "convertdate"])
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			filepath = os.path.join(root, name)
			filesize = os.path.getsize(filepath)

			try:
				if name.rsplit(".")[1] in videoformats and filepath.find(".Spotlight") == -1 and filepath.find(".Trashes") == -1:
					rofl.writerow([filepath.replace(path, ""), filesize, "transcode", "pending", ""])
					print (filepath)
			except IndexError:
				pass
			# rofl.writerow([filepath, filesize])
		# for name in dirs:
			# print(os.path.join(root, name))
   
			

	  
