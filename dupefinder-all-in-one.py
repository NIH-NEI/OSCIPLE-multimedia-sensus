from filetype_finder import filetypeFinder
from dupefinder import *
from dupe_dupe_checker import *
import argparse
from threading import Thread




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filepath', help="The path to scan")
    parser.add_argument('dupefile', help="Output CSV containing all duplicates")
    parser.add_argument('filetypefolder', help="Folder where lists of files of each type will be written.  Do not include trailing slash", default="filetypes")
    parser.add_argument('--csvfile', help="Output filetype list", default="filetypes.csv")
    parser.add_argument('--maxhashreps', help="How many 16kb chunks to generate hash for each file.  Default: the entire file.", default=pow(2, 100)) # basically infinity
    parser.add_argument('--skipuntil', help="For continuing incomplete previous scans.  Will skip until this file number is encountered.", default=0)
    parser.add_argument('--maxfiles', help="Only count this many files.", default=pow(2, 100))
    
    args = parser.parse_args()


    print ("Step 1, File Type Finder")
    finder = filetypeFinder()
    
    reporterThread = Thread(target=finder.reporter)
    reporterThread.daemon = True
    reporterThread.start()

    finder.findFileTypes(args.filepath, args.csvfile, args.filetypefolder, int(args.maxhashreps), args.skipuntil, int(args.maxfiles))


    print ("Step 2, Dupefinder")
    hashcsvfile = args.filetypefolder + "-all.csv"
    dupefinder(hashcsvfile, args.dupefile)


    print ("Step 3, Dupe-Dupe Checker")
    dedupe(args.dupefile)
    
