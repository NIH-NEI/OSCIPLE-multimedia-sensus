import gspread, datetime, subprocess, requests
from termcolor import colored
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Bioviz Ingest - NIH History Batch 2")

commandHistory = []

formatsToSheets = {"BC": "Betacam",
				   "BSP": "Betacam SP",
				   "DVC": "DVCPRO",
				   "HI8": "Hi8",
				   "MDV": "MiniDV",
				   "UM": "U-Matic"}

# def bytesToNormals(r, g, b):
#     return round(r / 255, 3), round(g / 255, 3), round(b / 255, 3)

# print (bytesToNormals(220, 233, 213))

# 248 230 208
# 253, 243, 208
#220 233 213
format_serialAssigned = cellFormat(backgroundColor=color(0.973, 0.902, 0.816), textFormat=textFormat(foregroundColor=color(0, 0, 0)))
format_recording = cellFormat(backgroundColor=color(1, 1, 0), textFormat=textFormat(foregroundColor=color(1, 0, 0)))
format_awaitingQC = cellFormat(backgroundColor=color(0.992, 0.953, 0.816), textFormat=textFormat(foregroundColor=color(0, 0, 0)))
format_outbox = cellFormat(backgroundColor=color(0.863, 0.914, 0.835), textFormat=textFormat(foregroundColor=color(0, 0, 0)))
format_tapesWithProblems = cellFormat(backgroundColor=color(1.0, 0.4, 0.4), textFormat=textFormat(foregroundColor=color(0.4, 0, 0)))


def updateMedia(ws, cell, stageName, location, format, captureDate=""):
	rowcolrange = gspread.utils.rowcol_to_a1(cell.row, 1)+":"+gspread.utils.rowcol_to_a1(cell.row, ws.col_count)
	ws.update_cell(cell.row, 3, stageName)
	ws.update_cell(cell.row, 4, location)
	if captureDate != "":
		ws.update_cell(cell.row, 2, captureDate)
	format_cell_range(ws, rowcolrange, format)
	print (colored("Updated {media} to {stageName}, {location}".format(media=cell.value, stageName=stageName, location=location), "green"))
	subprocess.Popen(["afplay", "chime-success.wav"])
    

cell = None
while True:
	cmd = input().upper()
 
	commandHistory.append([cmd, datetime.datetime.now()])
 
	if cmd[0:4] == "HS-2":
		if cmd[5:7] == "ST":
			if cell == None:
				print (colored("Error: No media selected", "red"))
				subprocess.Popen(["afplay", "chime-error.wav"])
			else:
				stage = int(cmd[7:8])
				bin = int(cmd[10:11])
				if stage == 2:
					updateMedia(ws, cell, "Serial assigned", "Bin {bin}".format(bin=bin), format_serialAssigned)
				elif stage == 4:
					updateMedia(ws, cell, "Awaiting QC", "Bin {bin}".format(bin=bin), format_awaitingQC)
				elif stage == 5:
					updateMedia(ws, cell, "Outbox", "Bin {bin}".format(bin=bin), format_outbox)
				elif stage == 6:
					updateMedia(ws, cell, "Tapes with problems", "Bin {bin}".format(bin=bin), format_tapesWithProblems)
		else:
			format = cmd.split("-")[2]
   
			try:
				ws = sheet.worksheet(formatsToSheets[format])
				cell = ws.find(cmd)
				if cell != None:
					rowProperties = ws.row_values(1)
					rowValues = ws.row_values(cell.row)
					for i in range(0, len(ws.row_values(cell.row))):
						print (colored("{property}: {value}".format(property=rowProperties[i], value=rowValues[i]), "cyan"))
					subprocess.Popen(["afplay", "chime-read.wav"])
				else:
					print (colored("Error: Media not found", "red"))
					subprocess.Popen(["afplay", "chime-error.wav"])
			except KeyError:
				print (colored("Error: Format not found", "red"))
				subprocess.Popen(["afplay", "chime-error.wav"])
		
	else:
		if cell == None:
			print (colored("Error: No media selected", "red"))
			subprocess.Popen(["afplay", "chime-error.wav"])
		else:
			captureDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			if cmd == "BC-IN":
				updateMedia(ws, cell, "Recording", "Betacam deck", format_recording, captureDate)
				print (requests.get("http://localhost:8081/mode/go"))
			elif cmd == "UM-IN":
				updateMedia(ws, cell, "Recording", "U-Matic deck", format_recording, captureDate)
			elif cmd == "DVCFW-IN":
				updateMedia(ws, cell, "Recording", "DVCPRO (FireWire) deck", format_recording, captureDate)
			elif cmd == "DVCA-IN":
				updateMedia(ws, cell, "Recording", "DVCPRO (analog) deck", format_recording, captureDate)
