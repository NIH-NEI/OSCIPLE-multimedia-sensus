import random, csv

in_name = "alldrives-2023-11-17-hash1-all-dupecount.csv"
out_name = "alldrives-2023-11-17-hash1-all-dupecount-scrambled.csv"

with open(in_name, "r") as f:
    # num_lines = len(f.readlines())
    lines = f.readlines()
    # print (lines)

#     linechoices = []
#     for i in range(0, num_lines):
#         linechoices.append(i)

with open(out_name, "w") as outfile:
    while len(lines) > 0:
        randomline = lines[random.randrange(len(lines))]
        # print (randomline)
        if randomline.find("/lacie/") == -1:
            outfile.write(randomline)
        lines.remove(randomline)
        print (len(lines))

# with open(in_name, "r") as infile:

#     with open(out_name, "w") as outfile:
        
#         while len(linechoices) > 0:
#             randomline = linechoices[random.randrange(len(linechoices))]
#             # print (randomline)
#             infile.seek(randomline)
#             # print (infile.readline())
#             outfile.write(infile.readline())
#             linechoices.remove(randomline)
#             print (len(linechoices))

    