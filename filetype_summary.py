import os, csv, datetime, argparse, time
from threading import Thread


"""
1. Creates a Summary File with a list of Extension, #Number Of Files, Drive and Total Size
2. Returns a list object which contains array of file list if there was a duplicate file name in the directory
"""

class filetypeSummary:
	def __init__(self):
		self.lastFile = "(start)"
		self.lastFileTime = datetime.datetime.now()
		self.startTime = 0.0
		self.filecount = 0
		self.skipUntil = 0

	def findFileTypes(self, filepath, skipUntil=0, maxfiles=pow(2, 100)):
		self.skipUntil = int(skipUntil)

		ic = "NEI"
		listpath = ic + "-Summary.csv"

		# Get the current date
		now = datetime.datetime.now()
		
		print ("{filepath} scan started at {datetime}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		fileextensions = {}
	
		# List of file type getting scanned
		extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpg", ".mpeg", ".3gp", ".ogg", ".mp3", ".wav", ".aac", ".flac", ".wma", ".m4a",
				 ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico", ".psd", ".raw", ".heic", ".heif",
				   ".mpg", ".mpeg", ".m4v", ".f4v", ".m2ts", ".mts", ".mxf", ".vob", ".rm", ".rmvb", ".mov", ".mng", ".qt",
					 ".swf", ".divx", ".xvid", ".drc", ".tif", ".snd", ".pre", ".eps", ".cr2", ".au"]
		
		self.startTime = time.time()
			
		for root, dirs, files in os.walk(filepath):
				if self.filecount >= maxfiles:
					break	

				for file in files:
					self.filecount += 1

					ext = os.path.splitext(file)[1].lower()
					path = os.path.join(root, file)
					parts = path.split('/')
					filename = file

					if self.filecount >= self.skipUntil:
						# skip system files and other unlikely-to-be-useful stuff that tends to make the results enormous
						if ext in extensions:
							self.lastFile = path
							self.lastFileTime = datetime.datetime.now()
							
							try:
								filesize = os.path.getsize(path)
							except:
								filesize = 0

							if filesize > 0:
								print ("{size} {path}".format(size=filesize, path=path))

								newExt = ext + "-" + parts[2]

                                # Creating Summary File Object
								if newExt not in fileextensions:
									fileextensions[newExt] = {"count": 1, "ext": ext, "filesize": filesize, "directory": parts[2]}
									print ("found file type: {ext} in directory : {directory}".format(ext=ext, directory=parts[2]))
								else:
									fileextensions[newExt]["count"] += 1
									fileextensions[newExt]["filesize"] += filesize
									fileextensions[newExt]["directory"] = parts[2]


					else:
						print ("file count is {fc}; skipping until {su} ({fn})".format(fc=self.filecount, su=self.skipUntil, fn=path))
				
			
		# Generating Summary File CSV	
		with open(listpath, "a", newline='') as tehfile:
			writer = csv.writer(tehfile)

			# Write the Header Row
			writer.writerow(["FileType", "Count", "Size", "Drive", "LastScanned"])
			
			for ext, count in fileextensions.items():
				writer.writerow([count["ext"], count["count"], count["filesize"], count["directory"], now.month + "-" + now.year])
	
		print ("{filepath} scan ended at {datetime}.  Total runtime: {rt}s  Total hashbuf: {hb}".format(filepath=filepath, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rt=round(time.time() - self.startTime, 1), hb=0))
  
  
	def reporter(self):
		try:
			while True:
				print ("Last file: {f} at time: {t}.   File count: {fc}   Runtime: {rt}s   bufRate: {br}".format(f=self.lastFile, t=self.lastFileTime.strftime("%Y-%m-%d %H:%M:%S"), fc=self.filecount, rt=round(time.time() - self.startTime, 1), br=0))
				time.sleep(5)
		except KeyboardInterrupt:
			pass




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="File Type Finder", description="Makes a Summary CSV Which contains list of Extension, #Number Of Files, Drive and Total Size.")
	parser.add_argument('filepath', help="The path to scan")
	parser.add_argument('--maxhashreps', help="How many 16kb chunks to generate hash for each file.  Default: the entire file.", default=pow(2, 100)) # basically infinity
	parser.add_argument('--skipuntil', help="For continuing incomplete previous scans.  Will skip until this file number is encountered.", default=0)
	parser.add_argument('--maxfiles', help="Only count this many files.", default=pow(2, 100))
	args = parser.parse_args()
 
	finder = filetypeSummary()
 
	reporterThread = Thread(target=finder.reporter)
	reporterThread.daemon = True
	reporterThread.start()

	finder.findFileTypes(args.filepath, args.skipuntil, int(args.maxfiles))
