### Description

Script scans a specified directory and its subdirectories for media files, analyzes them based on their file types, and generates a summary report in CSV format.

The summary report includes the following columns:
* File Type: The type of the media file (e.g., .mov, .mp4).
* Total Files: The total number of files for each filetype.
* Total Size: The cumulative size of all files of each filetype (in bytes).
* Directory: The directory where these files are located (First Level Directory Name only).

The output CSV file is named '{IC}-SummSummary.csv' and is saved in the current working directory.

### To run a scan, please use the following command.

## MACOS

* Map Network Drive
* **Command:** python3 {pythonfilename} {filepath} 
	* Where pythonfilename = Python file name trying to execute and filepath = Path trying to Scan
* **Example:** python3 filetype_summary.py /Volumes


