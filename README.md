# Dupefinder

## Main Workflow

### dupefinder-all-in-one.py

This script handles the entire process in one step.

Note: the all-in-one process is ideal where there's minimal chance the process will be interrupted, such as a local drive.

1. Choose a folder you'd like to scan for duplicates
2. Copy the path to that folder.  This will be the first parameter (e.g. "/Folder")
3. Choose a name for the output file containing the resulting .csv file of all suspected duplicate files.  (e.g. 
"folder-2024-05-01-dupes.csv").  This is the second parameter
4. Choose a name for this job (e.g. "folder-2024-05-01").  This is the third parameter
5. Run it...

```
python3 dupefinder-all-in-one.py /Folder older-2024-05-01-dupes.csv folder-2024-05-01
```


#### Optional parameters

* --csvfile - List of all filetypes the script encounters.  Default: "filetypes.csv".
* --maxhashreps - How many 16kb chunks to generate hash for each file.  Default: the entire file.  Lower values will generate a hash from a smaller portion of each file, which can save time, but may also result in false positives.  Default: entire file.
* --skipuntil - For continuing incomplete previous scans.  Will skip until this file number is encountered.  Default: no skips.
* --maxfiles - Only count this many files.  Default: scans all files.




## Alternate workflow

In the event that the process might be interrupted (such as with a network share), it may be desirable to run the steps one at a time.

1. Run filetype_finder.py.  Specify the folder you'd like to scan as the first parameter.  You may also want to specify a nickname for this scan, e.g. "folder-2024-05-01".
    * If the file-finder operation is interrupted, you can restart the scan at the last successful file number using --skipuntil.  Be sure to save it to a new .csv file and append the .csv files before running dupefinder.py.
2. Run dupefinder.py.  The first parameter is the nickname specified above with "-all.csv" appended to it, e.g. "folder-2024-05-01-all.csv".  The second parameter is the name of all detected duplicates, e.g. "folder-2024-05-01-dupes.csv".
3. Run dupe-dupe-checker.py.  The dupefinder process sometimes finds the same duplicate twice, but in opposite directions; in other words, file X is the same as file Y *and* file Y is the same as X.  Running this process detects and eliminate such entries.  The only parameter is the output of the dupefinder step; the original file is overwritten.




## Utilities

### filetype-finder.py

Makes a CSV list of every file type in a path.  Additionally, creates a separate list of every file of each file type
in the specified folder (defaults to filetypes/)

parser.add_argument('filepath', help="The path to scan")
	parser.add_argument('--csvfile', help="Output filetype list", default="filetypes.csv")
	parser.add_argument('--filetypefolder', help="Folder where lists of files of each type will be written.  Do not include trailing slash", default="filetypes")
	parser.add_argument('--maxhashreps', help="How many 16kb chunks to generate hash for each file.  Default: the entire file.", default=pow(2, 100)) # basically infinity
	parser.add_argument('--skipuntil', help="For continuing incomplete previous scans.  Will skip until this file number is encountered.", default=0)
	parser.add_argument('--maxfiles', help="Only count this many files.", default=pow(2, 100))


### csvscramble.py

### dupe_dupe_checker.py

### dupefinder-all-in-one.py

### dupefinder.py

### file-types-compare.py

### filetype_finder.py

### folder-compare.py

### hashmaker.py

### mergecsvfiles.py

### mergecsv.py

### time_estimate.py


