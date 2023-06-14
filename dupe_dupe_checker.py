import csv, argparse


def dedupe(filename):
	dupes = []

	with open(filename, "r") as csvfile:
		rofl = csv.reader(csvfile)
		
		for jawn in rofl:
			dupes.append(jawn)
			
	deduped = dupes.copy()


	for thingo in range(0, len(dupes)):
		thingy = dupes[thingo]

		for wtf in dupes:
			try:
				if thingy[0] == wtf[1] and wtf[0] == thingy[1]:
					del deduped[thingo]
			except:
				pass
			
	with open(filename, "w", newline='') as csvfile:
		rofl = csv.writer(csvfile)
		for line in deduped:
			rofl.writerow(line)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Dupe Dupe Checker",
                    description="Removes all dupes from a list that are simply a reverse of another dupe.")
	parser.add_argument('dupecsvfile', help="The CSV file containing the list of dupes.  Required.  Overwrites the existing file.")
 
	args = parser.parse_args()
 
	dedupe(args.dupecsvfile)