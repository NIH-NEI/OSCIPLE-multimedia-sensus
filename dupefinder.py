import csv

def dupefinder(hashcsvfile, dupefilepath, filetype):

	with open(hashcsvfile, "r") as hashfile:
		hashes = hashfile.readlines()

	with open(dupefilepath, "w") as dupefile:
		rofl = csv.writer(dupefile)
		for i in range(0, len(hashes)):
			hash = hashes[i].split(",")
			# print ("hash3: {hash3}   filetype: {filetype}".format(hash3=hash[3], filetype=filetype))
			if hash[3].rstrip() == filetype:
				for j in range(0, len(hashes)):
					comparehash = hashes[j].split(",")
					if comparehash[3].rstrip() == filetype:
						if i != j and hash[0].find(".DS_Store") == -1 and hash[0].find(".Spotlight-V100") == -1 and hash[0].find(".Trashes") == -1 and comparehash[0].find(".DS_Store") == -1 and comparehash[0].find(".Spotlight-V100") == -1 and comparehash[0].find(".Trashes") == -1:
							# print (comparehash)
							try:
								if hash[1] == comparehash[1] and hash[2] == comparehash[2]:
									print ("dupe detected: {name}, {name2}".format(name = hash[0], name2 = comparehash[0]))
									rofl.writerow([hash[0], comparehash[0], hash[1], hash[2]])
							except IndexError:
								pass