import random, csv, argparse


"""Inputs a CSV file and outputs it in random row order.  Technically works with any CR-delimited file."""

def csvscramble(in_name, out_name):
    with open(in_name, "r") as f:
        lines = f.readlines()


    with open(out_name, "w") as outfile:
        while len(lines) > 0:
            randomline = lines[random.randrange(len(lines))]
            outfile.write(randomline)
            lines.remove(randomline)
            print (len(lines))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CSV Scramble",
                                     description="Inputs a CSV file and outputs it in random row order.  Technically works with any CR-delimited file.")
    parser.add_argument('in_name', help="Input file")
    parser.add_argument('out_name', help="Scrambled output file")
    args = parser.parse_args()

    csvscramble(args.in_name, args.out_name)
