import os, csv, datetime, argparse
from hashmaker import *



def findFileTypes(filepath, listpath, filetypesfolder):
	print ("{filepath} scan started at {datetime}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	fileextensions = {}
 
	ftf = "{f}/".format(f=filetypesfolder)
 
	if not os.path.exists(ftf):
		os.makedirs(ftf)
	else:
		if len(os.listdir(ftf)) > 0:
			input("WARNING: {ftf} folder already contains files, possibly from a previous scan.  Press ctrl-C to quit, or Enter to proceed anyway.".format(ftf=ftf))

	filecount = 0
	for root, dirs, files in os.walk(filepath):
		for file in files:
			filecount += 1
			if filecount % 1000 == 0:
				print ("found {n} file ({dt})".format(n=filecount, dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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
					with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "w", newline='') as rofl:
						rofl.write("\"{path}\",{size},{hash}\n".format(path=path.replace("\"","'"),size=filesize, hash=hash))
				else:
					fileextensions[ext]["count"] += 1
					fileextensions[ext]["filesize"] += filesize
					fileextensions[ext]["hash"] = hash
					with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "a", newline='') as rofl:
						rofl.write("\"{path}\",{size},{hash}\n".format(path=path.replace("\"","'"),size=filesize,hash=hash))
		
		
	with open(listpath, "w", newline='') as tehfile:
		writer = csv.writer(tehfile)
		for ext, count in fileextensions.items():
			writer.writerow([ext, count["count"], count["filesize"]])
   
	print ("{filepath} scan ended at {datetime}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="File Type Finder", description="Makes a CSV list of every file type in a path.  Additionally, creates a separate list of every file of each file type in the specified folder (defaults to filetypes/)")
	parser.add_argument('filepath', help="The path to scan")
	parser.add_argument('--csvfile', help="Output filetype list", default="filetypes.csv")
	parser.add_argument('--filetypefolder', help="Folder where lists of files of each type will be written.  Do not include trailing slash", default="filetypes")
	args = parser.parse_args()

	findFileTypes(args.filepath, args.csvfile, args.filetypefolder)