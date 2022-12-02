import csv

with open("hashlist.csv", "r") as hashfile:
	hashes = hashfile.readlines()
	
# print (len(hashes))

with open("dupelist.csv", "w") as dupefile:
	rofl = csv.writer(dupefile)
	for i in range(0, len(hashes)):
		hash = hashes[i].split(",")
		for j in range(0, len(hashes)):
			comparehash = hashes[j].split(",")
			if i != j and hash[0].find(".DS_Store") == -1 and hash[0].find(".Spotlight-V100") == -1 and hash[0].find(".Trashes") == -1 and comparehash[0].find(".DS_Store") == -1 and comparehash[0].find(".Spotlight-V100") == -1 and comparehash[0].find(".Trashes") == -1:
				# print (comparehash)
				try:
					if hash[1] == comparehash[1] and hash[2] == comparehash[2]:
						print ("dupe detected: {name}, {name2}".format(name = hash[0], name2 = comparehash[0]))
						rofl.writerow([hash[0], comparehash[0]])
				except IndexError:
					pass