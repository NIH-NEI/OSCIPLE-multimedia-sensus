from filecmp import dircmp
def format_diff_files(dcmp):
    rofl = ""
    for name in dcmp.diff_files:
        rofl += "diff_file %s found in %s and %s\n" % (name, dcmp.left,
              dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        rofl += format_diff_files(sub_dcmp)
        
    return rofl

# dcmp = dircmp('dir1', 'dir2') 
# print_diff_files(dcmp) 

import os

dirlist = []

for x in os.walk("/Users/nickpiegari/Desktop"):
	dirlist.append(x[0])
 
for dir1 in dirlist:
    for dir2 in dirlist:
        if dir1 != dir2:
            print (format_diff_files(dircmp(dir1, dir2)))