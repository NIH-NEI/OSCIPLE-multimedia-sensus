import csv, argparse, os

def mergecsvs(path, outfile):
    merged = []

    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvf = os.path.join(path, file)

            with open(csvf, "r") as csvfile:
                csvread = csv.reader(csvfile)
                for line in csvread:
                    merged.append(line)
    
    with open(outfile, "w") as outjawn:
        csvwrite = csv.writer(outjawn)
        for line in merged:
            csvwrite.writerow(line)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CSV Merge",
                                     description="Merges two CSV files.")
    parser.add_argument("path", help="The folder where all csv files will be merged into one")
    parser.add_argument("outfile", help="The resulting csv file")
    args = parser.parse_args()
    
    mergecsvs(args.path, args.outfile)