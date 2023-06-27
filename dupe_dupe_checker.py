import csv, argparse


def dedupe(filename):
	dupes = []

	with open(filename, "r") as csvfile:
		csvreader = csv.reader(csvfile)
		
		for line in csvreader:
			dupes.append(line)
			
	deduped = dupes.copy()


	for count in range(0, len(dupes)):
		orig = dupes[count]

		for cross in dupes:
			try:
				if orig[0] == cross[1] and cross[0] == orig[1]:
					del deduped[count]
			except:
				pass
			
	with open(filename, "w", newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		for line in deduped:
			csvwriter.writerow(line)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Dupe Dupe Checker",
                    description="Removes all dupes from a list that are simply a reverse of another dupe.")
	parser.add_argument('dupecsvfile', help="The CSV file containing the list of dupes.  Required.  Overwrites the existing file.")
 
	args = parser.parse_args()
 
	dedupe(args.dupecsvfile)