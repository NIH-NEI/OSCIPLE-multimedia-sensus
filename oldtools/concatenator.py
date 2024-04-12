# path = "/Volumes/LaCie/Ingest/"
path = "/Volumes/nickpiegari/Desktop/dv concatenation test/"

import os, ffmpeg

			

dir_list = os.listdir(path)
for dir in dir_list:
	# print (dir)
	try:
		dirpath = os.path.join(path, dir)
		files = os.listdir(dirpath)
		# print (files)
		concatpath = os.path.join(dirpath, "concat.txt")
		with open(concatpath, "w") as concat_file:
			filecount = 0
			for file in sorted(files):
				filesplitext = os.path.splitext(file)
				if filesplitext[1] == ".dv":
					filecount += 1
					filepath = os.path.join(dirpath, file)
					rofl = "{path}-output{ext}".format(path=filesplitext[0], ext=filesplitext[1])
					# print (filepath)
					concat_file.write("file '{filepath}'\n".format(filepath=rofl))
     
					ffmpeg.input(filepath).filter_("fps", fps=30).output(rofl).run()
	
		if filecount > 1:
			outputpath = os.path.join(dirpath, "output.dv")
			print (outputpath)
			ffmpeg.input(concatpath, f='concat', safe=0).output(outputpath, codec='copy').run()
				
	except NotADirectoryError:
		pass
