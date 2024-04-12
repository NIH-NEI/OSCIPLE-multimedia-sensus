# !/usr/bin/python
import os, csv, sys, hashlib, time, argparse


BUF_SIZE = 65536


class hashMaker:
	def __init__(self):
		self.bufSize = 65536
		self.bufRate = 0
		self.bufTotal = 0

	def makeOneHash(self, filepath, maxreps=pow(2, 100)):
		sha1 = hashlib.sha1()

		reps = 0
		with open(filepath, 'rb') as f:
			while reps < maxreps:
				reps += 1
				data = f.read(self.bufSize)
				self.bufRate += self.bufSize
				self.bufTotal += self.bufSize
				sys.stdout.write(".")
				sys.stdout.flush()
				if not data:
					break
				sha1.update(data)

		return sha1.hexdigest()


	def makehash(self, hashcsvfile, filetypes, path):
		with open(hashcsvfile, "w", newline='') as csvfile:
			rofl = csv.writer(csvfile)
			for root, dirs, files in os.walk(path, topdown=False):
				for name in files:
					filetype = os.path.splitext(name)[1]
					if filetype in filetypes:
						startTime = time.time()
						try:
							filepath = os.path.join(root, name)
							filesize = os.path.getsize(filepath)
		
							if filesize > 0:
			
								sha1 = self.makeOneHash(filepath)

								rofl.writerow([filepath.replace(path, "").encode("utf-8"), filesize, sha1, filetype, time.time() - startTime])
						except:
							pass
	
		print ("Generated {csv}".format(csv=hashcsvfile))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Hashmaker",
                                  description="Generates the CSV list of hashes of the given path for use by Dupemaker")
	parser.add_argument('filetypes', help="Comma-separated list of all file types you'd like to check, e.g. '.jpg,.gif,.bmp")
	parser.add_argument('path', help="The path for which to make hashes")
	parser.add_argument('--hashcsvfile', default="hashfile.csv", help="Optional path for hash CSV file; hashfile.csv is used by default")
	args = parser.parse_args()

	hashmake = hashMaker()
 
	hashmake.makehash(args.hashcsvfile, args.filetypes.split(","), args.path)