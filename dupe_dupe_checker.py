import csv, argparse, time, datetime


"""Removes all dupes from a list that are simply a reverse of another dupe."""

def dedupe(filename):
	dupes = []

	with open(filename, "r") as csvfile:
		csvreader = csv.reader(csvfile)
		
		for line in csvreader:
			dupes.append(line)
			
	deduped = dupes.copy()

	startTime = time.time()
	for count in range(0, len(dupes)):
		percentDone = count / len(dupes)
		elapsedTime = time.time() - startTime
		try:
			totalEstimate = elapsedTime / percentDone
		except ZeroDivisionError:
			totalEstimate = -1
		print ("current/total: {a}/{b}   elapsed time: {c}   percent done: {d}   total estimate: {e}".format(a=count,b=len(dupes), c=str(datetime.timedelta(seconds=elapsedTime)), d=round(percentDone, 4), e=str(datetime.timedelta(seconds=totalEstimate))))
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