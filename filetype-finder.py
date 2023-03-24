import os, csv

fileextensions = []

with open("filetype-list2.csv", "a") as tehfile:
	writer = csv.writer(tehfile)
	for root, dirs, files in os.walk("/Volumes/LaCie"):
		for file in files:
			# print (file)
			ext = os.path.splitext(file)[1]
			if ext not in fileextensions:
				join = os.path.join(root, file)
				if join.find(".bzvol") == -1 and join.find("$Recycle") == -1 and join.find(".com") == -1 and join.find(".Spotlight") == -1 and join.find(".Volume") == -1 and join.find(".DS") == -1:
					fileextensions.append(ext)
					print (os.path.join(root, file))
					writer.writerow([ext, join])
