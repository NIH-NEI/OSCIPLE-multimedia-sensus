# !/usr/bin/python

path = "/volumes/One Touch/ingest history 2 pre qc/betacam trimmed"
# path = "/volumes/One Touch/ingest history 2 pre qc/betacam sp trimmed"
# path = "/volumes/One Touch/ingest history 2 pre qc/u-matic trimmed"

import ffmpeg, datetime
import pandas as pd

# reading the csv file
df = pd.read_csv("videolist.csv")

count = 0
for rofl in df.iterrows():
	filepath = path + df.loc[count, "filename"]
	print (filepath)

	try:
		if df.loc[count, "status"] == "pending":
			outfile = path + df.loc[count, "filename"].rsplit(".", 1)[0] + ".mp4"
		
			ffmpeg.input(filepath).output(outfile).run()
		
			df.loc[count, "status"] = "done"
			df.loc[count, "convertdate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			
		
			df.to_csv("videolist.csv", index=False)
		else:
			print ("skipping")
	except:
		pass

	count += 1

# # updating the column value/data
# df.loc[5, 'Name'] = 'SHIV CHANDRA'

# # writing into the file
# df.to_csv("videolist.csv", index=False)
   
			

	  
