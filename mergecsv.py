import csv, argparse

def mergecsv(file1, file1name, file2, file2name, outfile):
    merged = []
    
    with open(file1, "r") as file1file:
        file1reader = csv.reader(file1file)
        for row1 in file1reader:
            row1.append(file1name)
            merged.append(row1)
            
    with open(file2, "r") as file2file:
        file2reader = csv.reader(file2file)
        for row2 in file2reader:
            row2.append(file2name)
            merged.append(row2)
            
    with open(outfile, "w", newline='') as outfilefile:
        outfilewriter = csv.writer(outfilefile)
        for row in merged:
            outfilewriter.writerow(row)
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CSV Merge",
                                     description="Merges two CSV files.")
    parser.add_argument("file1", help="The first CSV file")
    parser.add_argument("file1name", help="Text to be added to each row of file 1, to tell them apart")
    parser.add_argument("file2", help="The second CSV file")
    parser.add_argument("file2name", help="Text to be added to each row of file 2")
    parser.add_argument("outfile", help="The output CSV file")
    args = parser.parse_args()
    
    mergecsv(args.file1, args.file1name, args.file2, args.file2name, args.outfile)