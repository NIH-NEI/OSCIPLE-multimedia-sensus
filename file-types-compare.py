from dupefinder import *
from hashmaker import *
from dupe_dupe_checker import *
import time, datetime, argparse



def fileTypesCompare(hashcsvfile, filetypes, filepath):
	print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))

	hashmaker(hashcsvfile, filetypes, filepath)

	print ("starting hash gather {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
		
	for filetype in filetypes:
		startTime = time.time()
		filename = "dupes-{filetype}.csv".format(filetype=filetype.replace(".", ""))
		dupefinder(hashcsvfile, filename, filetype)
		print ("deduping {filetype}".format(filetype=filetype))
		dedupe(filename)
		print ("{filetype} completed in {time} seconds".format(filetype=filetype, time=round(time.time() - startTime, 2)))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="File Types Compare",
								  description="Runs the whole sequence at once:  makes a hashfile, checks for dupes, and removes the duplicate dupes.")
	parser.add_argument('filepath', help="Path to search for duplicates")
	parser.add_argument('filetypes', help="Comma-separated list of all file types you'd like to check, e.g. '.jpg,.gif,.bmp")
	parser.add_argument('--hashcsvfile', default="hashfile.csv", help="Optional path for hash CSV file; hashfile.csv is used by default")
	args = parser.parse_args()
 
	fileTypesCompare(args.hashcsvfile, args.filetypes.split(","), args.filepath)