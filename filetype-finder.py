import os, csv, datetime, argparse, time, sys
from hashmaker import *
from threading import Thread
# import scandir


class filetypeFinder:
	def __init__(self):
		self.lastFile = "(start)"
		self.lastFileTime = datetime.datetime.now()
		self.startTime = 0.0
		self.filecount = 0


	def findFileTypes(self, filepath, listpath, filetypesfolder, maxhashreps=99999999999999999999999):
  
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
				for file in files:
					self.filecount += 1
					ext = os.path.splitext(file)[1].lower()
					path = os.path.join(root, file)
			
					if path.find(".bzvol") == -1 and path.find("$Recycle") == -1 and path.find(".com") == -1 and path.find(".Spotlight") == -1 and path.find(".Volume") == -1 and path.find(".DS") == -1:
						self.lastFile = path
						self.lastFileTime = datetime.datetime.now()
						
						try:
							filesize = os.path.getsize(path)
						except:
							filesize = 0
		
						if filesize > 0:
							print (path)
					
							try:
								hash = makeOneHash(path, maxhashreps)
							except:
								hash = 0

							row = [path, filesize, hash, ext[1:], root, file]
							bigcsvwriter.writerow(row)

							if ext not in fileextensions:
								fileextensions[ext] = {"count": 1, "filesize": filesize, "hash": hash}
								print ("found file type: {ext}".format(ext=ext))
								with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "w", newline='', encoding="utf-8") as csvfile:
									csvwriter = csv.writer(csvfile)
									csvwriter.writerow(row)
									# csvfile.write("\"{path}\",{size},{hash},{ext},{root},{file}\n".format(path=path.replace("\"","'"),size=filesize, hash=hash,ext=ext[1:],root=root,file=file))
							else:
								fileextensions[ext]["count"] += 1
								fileextensions[ext]["filesize"] += filesize
								fileextensions[ext]["hash"] = hash
								with open("{ftf}/filetype-{ext}.csv".format(ext=ext[1:], ftf=ftf), "a", newline='', encoding="utf-8") as csvfile:
									csvwriter = csv.writer(csvfile)
									csvwriter.writerow(row)
									# csvfile.write("\"{path}\",{size},{hash},{ext},{root},{file}\n".format(path=path.replace("\"","'"),size=filesize,hash=hash,ext=ext[1:],root=root,file=file))
			
			
			
		with open(listpath, "w", newline='') as tehfile:
			writer = csv.writer(tehfile)
			for ext, count in fileextensions.items():
				writer.writerow([ext, count["count"], count["filesize"]])
	
		print ("{filepath} scan ended at {datetime}.  Total runtime: {rt}s".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rt=round(time.time() - self.startTime, 1)))
  
  
	def reporter(self):
		try:
			while True:
				print ("Last file: {f} at time: {t}.   File count: {fc}   Runtime: {rt}s".format(f=self.lastFile, t=self.lastFileTime.strftime("%Y-%m-%d %H:%M:%S"), fc=self.filecount, rt=round(time.time() - self.startTime, 1)))
				time.sleep(5)
		except KeyboardInterrupt:
			pass




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="File Type Finder", description="Makes a CSV list of every file type in a path.  Additionally, creates a separate list of every file of each file type in the specified folder (defaults to filetypes/)")
	parser.add_argument('filepath', help="The path to scan")
	parser.add_argument('--csvfile', help="Output filetype list", default="filetypes.csv")
	parser.add_argument('--filetypefolder', help="Folder where lists of files of each type will be written.  Do not include trailing slash", default="filetypes")
	parser.add_argument('--maxhashreps', help="How many 16kb chunks to generate hash for each file.  Default: the whole thing", default=9999999999999999999999999)
	args = parser.parse_args()
 
	finder = filetypeFinder()
 
	reporterThread = Thread(target=finder.reporter)
	reporterThread.daemon = True
	reporterThread.start()

	finder.findFileTypes(args.filepath, args.csvfile, args.filetypefolder)
 
 
# /System/Volumes/Data/private/var/folders/y0/k9wn801n66z_y48k_jmwvq440000gn/T/clr-debug-pipe-932-1686583729-in