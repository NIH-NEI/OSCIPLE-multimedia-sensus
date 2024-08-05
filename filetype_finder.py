import os, csv, datetime, argparse, time, sys
from hashmaker import *
from threading import Thread


"""
Makes a CSV list of every file type in a path.  Additionally, creates a separate list of every file of each file type
in the specified folder (defaults to filetypes/)
"""

class filetypeFinder:
	def __init__(self):
		self.lastFile = "(start)"
		self.lastFileTime = datetime.datetime.now()
		self.startTime = 0.0
		self.filecount = 0
		self.skipUntil = 0
		self.hashmake = hashMaker()


	def findFileTypes(self, filepath, listpath, filetypesfolder, maxhashreps=pow(2, 100), skipUntil=0, maxfiles=pow(2, 100)):
		self.skipUntil = int(skipUntil)
		
		print ("{filepath} scan started at {datetime}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		fileextensions = {}
	
		ftf = "{f}/".format(f=filetypesfolder)
	
		if not os.path.exists(ftf):
			os.makedirs(ftf)
		else:
			if len(os.listdir(ftf)) > 0:
				input("WARNING: {ftf} folder already contains files, possibly from a previous scan.  Press ctrl-C to quit, or Enter to proceed anyway.".format(ftf=ftf))

		
		self.startTime = time.time()
		with open ("{f}-all.csv".format(f=filetypesfolder), "a", newline='') as bigcsvfile:
			bigcsvwriter = csv.writer(bigcsvfile)
			for root, dirs, files in os.walk(filepath):
				if self.filecount >= maxfiles:
					break
				

				for file in files:
					self.filecount += 1

					ext = os.path.splitext(file)[1].lower()
					path = os.path.join(root, file)
					filename = file

					if self.filecount >= self.skipUntil:
						# skip system files and other unlikely-to-be-useful stuff that tends to make the results enormous
						if path.find(".bzvol") == -1 and path.find("$Recycle") == -1 and path.find(".com") == -1 and path.find(".Spotlight") == -1 and path.find(".Volume") == -1 and path.find(".DS") == -1 and path.find(".tmp") == -1 and path.find(".log") == -1 and path.find(".DS_Store") == -1 and ext != "":
							self.lastFile = path
							self.lastFileTime = datetime.datetime.now()
							
							try:
								filesize = os.path.getsize(path)
							except:
								filesize = 0

							if filesize > 0:
								print ("{size} {path}".format(size=filesize, path=path))
						
								hash = self.hashmake.makeOneHash(path, maxhashreps)

								try: # not all files have a created time
									createdTime = datetime.datetime.fromtimestamp(os.stat(path).st_birthtime).strftime("%Y-%m-%d %H:%M:%S")
								except:
									createdTime = 0

								try: # not all files have a modified time
									modifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
								except:
									modifiedTime = 0

								
								row = [filename, "NEI", path, filesize, hash, ext[1:], root, file, createdTime, modifiedTime]
								try:
									bigcsvwriter.writerow(row)
								except UnicodeEncodeError:
									try:
										row = [filename, "NEI", path.encode("ascii", "ignore"), filesize, hash, ext[1:], root.encode("ascii", "ignore"), file.encode("ascii", "ignore"), modifiedTime, createdTime]
										bigcsvwriter.writerow(row)
									except UnicodeEncodeError:
										row = ["(unicode encode error)"]
			

								if ext not in fileextensions:
									fileextensions[ext] = {"count": 1, "filesize": filesize, "hash": hash}
									print ("found file type: {ext}".format(ext=ext))
									with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "w", newline='', encoding="utf-8") as csvfile:
										csvwriter = csv.writer(csvfile)
										csvwriter.writerow(row)
								else:
									fileextensions[ext]["count"] += 1
									fileextensions[ext]["filesize"] += filesize
									fileextensions[ext]["hash"] = hash
									with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "a", newline='', encoding="utf-8") as csvfile:
										csvwriter = csv.writer(csvfile)
										csvwriter.writerow(row)

					else:
						print ("file count is {fc}; skipping until {su} ({fn})".format(fc=self.filecount, su=self.skipUntil, fn=path))
				
			
			
		with open(listpath, "w", newline='') as tehfile:
			writer = csv.writer(tehfile)
			for ext, count in fileextensions.items():
				writer.writerow([ext, count["count"], count["filesize"]])
	
		print ("{filepath} scan ended at {datetime}.  Total runtime: {rt}s  Total hashbuf: {hb}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rt=round(time.time() - self.startTime, 1), hb=self.hashmake.bufTotal))
  
  
	def reporter(self):
		try:
			while True:
				print ("Last file: {f} at time: {t}.   File count: {fc}   Runtime: {rt}s   bufRate: {br}".format(f=self.lastFile, t=self.lastFileTime.strftime("%Y-%m-%d %H:%M:%S"), fc=self.filecount, rt=round(time.time() - self.startTime, 1), br=self.hashmake.bufRate / 5.0))
				self.hashmake.bufRate = 0
				time.sleep(5)
		except KeyboardInterrupt:
			pass




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="File Type Finder", description="Makes a CSV list of every file type in a path.  Additionally, creates a separate list of every file of each file type in the specified folder (defaults to filetypes/)")
	parser.add_argument('filepath', help="The path to scan")
	parser.add_argument('--csvfile', help="Output filetype list", default="filetypes.csv")
	parser.add_argument('--filetypefolder', help="Folder where lists of files of each type will be written.  Do not include trailing slash", default="filetypes")
	parser.add_argument('--maxhashreps', help="How many 16kb chunks to generate hash for each file.  Default: the entire file.", default=pow(2, 100)) # basically infinity
	parser.add_argument('--skipuntil', help="For continuing incomplete previous scans.  Will skip until this file number is encountered.", default=0)
	parser.add_argument('--maxfiles', help="Only count this many files.", default=pow(2, 100))
	args = parser.parse_args()
 
	finder = filetypeFinder()
 
	reporterThread = Thread(target=finder.reporter)
	reporterThread.daemon = True
	reporterThread.start()

	finder.findFileTypes(args.filepath, args.csvfile, args.filetypefolder, int(args.maxhashreps), args.skipuntil, int(args.maxfiles))
