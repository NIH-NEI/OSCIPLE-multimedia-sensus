import gspread, pprint, os, re
from termcolor import colored
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)



spreadsheet = client.open("Bioviz Ingest - NIH History Batch 2")


media = {}


sheets = spreadsheet.worksheets()

for sheet in sheets:
	for record in sheet.get_all_records():
		media[record["Serial #"]] = record["Title"]
	   

	
for root, dirs, files in os.walk('/volumes/lacie/Ingest - NIH History Batch 2'):
	for item in dirs:
		if item.upper() in media:
			newtitle = "{item} {name}".format(item=item.upper(), name=media[item])
			newtitle = re.sub(r'[^\w_. -]', '_', newtitle)
			print (newtitle)
			itempath = os.path.join(root, item)
			newpath = os.path.join(root, newtitle)
			print("Renaming '{orig}' to '{newtitle}'".format(orig=item, newtitle=newtitle))
			print (itempath)
			print (newpath)
			os.rename(itempath, newpath)
			print ()
			
	for item in files:
		spl = item.rsplit(".", 1)
		name = spl[0].upper()
		ext = spl[1]
		if name in media and ext != "":
			newtitle = "{origname} {title}.{ext}".format(origname=name.upper(), title=re.sub(r'[^\w_. -]', '_', media[name]), ext=ext)
			print (newtitle)
			itempath = os.path.join(root, "{item}.{ext}".format(item=spl[0], ext=spl[1]))
			newpath = os.path.join(root, newtitle)
			# yee = input("Rename '{orig}' to '{newtitle}'?".format(orig=item, newtitle=newtitle))
			print("Renaming '{orig}' to '{newtitle}'".format(orig=item, newtitle=newtitle))
			# if yee == "y" or yee == "yes" or yee == "":
			print (itempath)
			print (newpath)
			os.rename(itempath, newpath)
			# else:
			# 	print ("skipping")
			print ()
