import csv, os, pprint, argparse

def folderCompare(dupefile, outfile):

	uniquefolders = {}

	with open(dupefile, "r") as filefile:
		rofl = csv.reader(filefile)
	
		for line in rofl:
			dir, file = os.path.split(line[0])
			print (dir)
			if dir not in uniquefolders:
				uniquefolders[dir] = []
	
			hashcombo = {file: line[3]}
	
			if hashcombo not in uniquefolders[dir]:
				uniquefolders[dir].append({file: line[3]})
	

	with open(outfile, "w", newline='') as outfilefile:
		folderwriter = csv.writer(outfilefile)
		total = len(uniquefolders)
		count = 0
		for folderAName, folderAContents in uniquefolders.items():
			count += 1
			print ("{a}/{b}".format(a=count, b=total))
			# print (folderA)
			for folderBName, folderBContents in uniquefolders.items():
				if folderAName != folderBName:
					filematches = 0
					filecountA = len(folderAContents)
					filecountB = len(folderBContents)
					
					for file in folderAContents:
						# print (file)
						if file in folderBContents:
							filematches += 1
							# print (file)
							
					if filematches > 0:
						out = "{filematches} matches out of {filecount} files in {folderA}, {folderB}".format(filematches=filematches, filecount=filecount, folderA=folderAName, folderB=folderBName)
						print (out)
						# outfilefile.write("{out}\n".format(out=out))
						folderwriter.writerow([filematches, filecountA, filecountB, folderAName, folderBName])
	
	print ("Generated {outfile}".format(outfile=outfile))
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Folder Compare",
								  description="Given a CSV dupe file, will generate a summary of the number of matching files in every permutation of folders.  Useful for determining whether entire *folders* are duplicates, or close to duplicates, of one another")
	parser.add_argument('dupefile', help="The CSV dupe file to use")
	parser.add_argument('outfile', help="File name of the report to generate")
	args = parser.parse_args()
 
	folderCompare(args.dupefile, args.outfile)