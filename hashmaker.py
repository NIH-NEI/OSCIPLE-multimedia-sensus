# !/usr/bin/python

path = "/Volumes/LaCie/Ingest/"

import os, csv, sys, hashlib


BUF_SIZE = 65536 * 16




with open("hashlist.csv", "w") as csvfile:
	rofl = csv.writer(csvfile)
	rofl.writerow(["filename", "hash"])
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			filepath = os.path.join(root, name)
			filesize = os.path.getsize(filepath)
   
			sha1 = hashlib.sha1()

			with open(filepath, 'rb') as f:
				# while True:
				data = f.read(BUF_SIZE)
					# if not data:
					# 	break
				sha1.update(data)
   
			sha1 = sha1.hexdigest()

			print (filepath, sha1)
			rofl.writerow([filepath.replace(path, ""), filesize, sha1])
		# for name in dirs:
		# 	print(os.path.join(root, name))
   
			
