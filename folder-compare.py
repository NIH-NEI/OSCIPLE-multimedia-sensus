import csv, os, pprint

uniquefolders = {}

with open("dupes-jpg.csv", "r") as filefile:
	rofl = csv.reader(filefile)
 
	for line in rofl:
		dir, file = os.path.split(line[0])
		if dir not in uniquefolders:
			uniquefolders[dir] = []
   
		hashcombo = {file: line[3]}
   
		if hashcombo not in uniquefolders[dir]:
			uniquefolders[dir].append({file: line[3]})
   
   
pprint.pprint(uniquefolders)


for folderAName, folderAContents in uniquefolders.items():
    # print (folderA)
    for folderBName, folderBContents in uniquefolders.items():
        if folderAName != folderBName:
            filematches = 0
            filecount = len(folderAContents)
            
            for file in folderAContents:
                # print (file)
                if file in folderBContents:
                    filematches += 1
                    # print (file)
                    
            if filematches > 0:
                print ("{filematches} matches out of {filecount} files in {folderA}, {folderB}".format(filematches=filematches, filecount=filecount, folderA=folderAName, folderB=folderBName))
  
  