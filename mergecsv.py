import csv, argparse

def mergecsv(file1, file2, outfile):
    merged = []
    
    with open(file1, "r") as file1file:
        file1reader = csv.reader(file1file)
        for row in file1reader:
            merged.append(row)
            
    with open(file2, "r") as file2file:
        file2reader = csv.reader(file2file)
        for row in file2reader:
            merged.append(row)
            
    with open(outfile, "w", newline='') as outfilefile:
        outfilewriter = csv.writer(outfilefile)
        for row in merged:
            outfilewriter.writerow(row)
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CSV Merge",
                                     description="Merges two CSV files.")
    parser.add_argument("file1", help="The first CSV file")
    parser.add_argument("file2", help="The second CSV file")
    parser.add_argument("outfile", help="The output CSV file")
    args = parser.parse_args()
    
    mergecsv(args.file1, args.file2, args.outfile)