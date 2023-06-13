# !/usr/bin/python



import os, csv, sys, hashlib, time


BUF_SIZE = 65536 * 16


def makeOneHash(filepath):
	sha1 = hashlib.sha1()

	with open(filepath, 'rb') as f:
		# while True:
		data = f.read(BUF_SIZE)
			# if not data:
			# 	break
		sha1.update(data)

	return sha1.hexdigest()


def hashmaker(hashcsvfile, filetypes, path):
	with open(hashcsvfile, "w") as csvfile:
		rofl = csv.writer(csvfile)
		# rofl.writerow(["filename", "hash"])
		for root, dirs, files in os.walk(path, topdown=False):
			for name in files:
				filetype = os.path.splitext(name)[1]
				if filetype in filetypes:
					startTime = time.time()
					try:
						filepath = os.path.join(root, name)
						filesize = os.path.getsize(filepath)
	  
						if filesize > 0:
          
							sha1 = makeOneHash(filepath)

							print (filepath, sha1)
							rofl.writerow([filepath.replace(path, ""), filesize, sha1, filetype, time.time() - startTime])
					except:
						pass

if __name__ == "__main__":
	filetypes = [".gif"]
	hashmaker("hashfile.csv", filetypes, "/Users/nickpiegari")
   
			
