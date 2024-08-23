### Description

Script scans a specified directory and its subdirectories for media files, analyzes them based on their file types, and generates a summary report in CSV format.

The summary report includes the following columns:
* File Type: The type of the media file (e.g., .mov, .mp4).
* Total Files: The total number of files for each filetype.
* Total Size: The cumulative size of all files of each filetype (in bytes).
* Directory: The directory where these files are located (First Level Directory Name only).

The output CSV file is named '{IC}-Summary.csv' and is saved in the current working directory.

### To run a scan, please use the following command.

* Update Line Number 20 to have your IC name in file filetype_summary.py

## MACOS

* Map Network Drive
* **Command:** python3 {pythonfilename} {filepath} 
	* Where pythonfilename = Python file name trying to execute and filepath = Path trying to Scan

* **Example:** python3 filetype_summary.py /Volumes

## Windows

* **Download Python** (Visit the official Python website: python.org)

* **Install Python**:
	* Run the downloaded installer.
		* **Important:** Make sure to check the box that says **Add Python to PATH** before clicking the Install Now button. This will allow you to run Python from the command line.
		* Proceed with the installation.

* **Verify Python Installation**:
	* Open the Command Prompt by typing **cmd** in the search bar and pressing Enter.
		* In the Command Prompt, type: **python --version**
		* This should display the version of Python that you installed. If you see the version number, Python is successfully installed.

* **Running Python Scripts from the command line**:
	* Navigate to the directory where your Python script is located using the cd command.
		* For example, if your script is in **C:\Users\YourName\Scripts**, type: **cd C:\Users\YourName\Scripts**
		* Once in the directory, run your Python script by typing: **python3 filetype_summary.py {Mapped Drive Path Trying to Scan}**

### How to Scan Multiple Drives ?

* You can always scan multiple drive in parallel.
* Open a new terminal and start scanning the first drive using command menioned above based on OS.
* Again, open a new terminal and start scanning the second drive using command menioned above based on OS.
* Follow the same procedure if there are more than 2 drives.
* There will always be **ONE** ouput CSV file generated at the end of the scan, no matter if we scan one or multiple dirve together. 

### Steps to do after Scan has completed

* Email output CSV file with name **{IC}-Summary.csv** to [NEI IT Developers](mailto:NEIITD@nei.nih.gov) or [Hays, Dustin](dustin.hays@nih.gov).

### Questions ?

* Please forward any questions to [NEI IT Developers](mailto:NEIITD@nei.nih.gov).



