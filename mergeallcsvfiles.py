import os, csv, argparse

def mergeallcsvfiles(path, outfile):
	with open(outfile, "w", newline='') as outfilefile:
		combowriter = csv.writer(outfilefile)
  
		files = os.listdir(path)
		for file in files:
			# ext = file.replace("filetype-", "").replace(".csv","")
			with open(os.path.join(path, file), "r") as filefile:
				csvread = csv.reader(filefile)
				for row in csvread:
					# combowriter.writerow(row + [ext])
					combowriter.writerow(row)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Merge All CSV Files",
                                  description="Merges an entire folder of file type CSVs into a single one with an extra column for file extension")
	parser.add_argument('path', help="Folder full of file types")
	parser.add_argument('outfile', help="Destination for merged CSV file")
	args = parser.parse_args()
 
	mergeallcsvfiles(args.path, args.outfile)