import gspread, datetime, subprocess, requests, serial, traceback
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
				   "UM": "U-Matic",
       			   "CASS": "Cassette",
				   "TEST": "Tester tapes"}

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
 
 
def lcd(line1, line2, color=""):
	try:
		ser = serial.Serial("/dev/tty.usbmodem1101", baudrate=115200)  # open serial port
		if color != "":
			ser.write("lc{color}]\n".format(color=color))

		l1 = line1 + (" " * (16 - len(line1)))
		ser.write("lm1{line}".format(l1))
		l2 = line2 + (" " * (16 - len(line2)))
		ser.write("lm2{line}".format(l2))
		ser.close()             # close port
	except:
		pass
		# traceback.print_exc()
		# print (colored("Error: Arduino not available", "red"))
	

cell = None
while True:
	print ()
	cmd = input().upper()
 
	commandHistory.append([cmd, datetime.datetime.now()])
 
	if cmd[0:4] == "HS-2":
		lcd(cmd, "", "y")
		if cmd[5:7] == "ST":
			if cell is None:
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
				print (ws)
				cell = ws.find(cmd)
				print (cell)
				if cell is not None:
					rowProperties = ws.row_values(1)
					rowValues = ws.row_values(cell.row)
					for i in range(0, len(ws.row_values(cell.row))):
						property = rowProperties[i]
						value = rowValues[i]
						color = "white"
						if property == "Stage":
							if value == "Inbox":
								color = "light_red"
							elif value == "Serial assigned":
								color = "light_yellow"
							elif value == "Awaiting QC":
								color = "yellow"
							elif value == "Outbox":
								color = "green"
							elif value == "Tapes with problems":
								color = "red"
						print (colored("{property}: {value}".format(property=rowProperties[i], value=rowValues[i]), color))
					subprocess.Popen(["afplay", "chime-read.wav"])
				else:
					print (colored("Error: Media not found", "red"))
					subprocess.Popen(["afplay", "chime-error.wav"])
			except KeyError:
				# print (colored("Error: Format not found", "red"))
				traceback.print_exc()
				subprocess.Popen(["afplay", "chime-error.wav"])
    
	elif cmd[0:4] == "TEST":
		format = "TEST"
		try:
			ws = sheet.worksheet(formatsToSheets[format])
			cell = ws.find(cmd)
			if cell != None:
				rowProperties = ws.row_values(1)
				rowValues = ws.row_values(cell.row)
				for i in range(0, len(ws.row_values(cell.row))):
					property = rowProperties[i]
					value = rowValues[i]

					print (colored("{property}: {value}".format(property=property, value=value), "cyan"))
				subprocess.Popen(["afplay", "chime-read.wav"])
			else:
				print (colored("Error: Media not found", "red"))
				subprocess.Popen(["afplay", "chime-error.wav"])
		except KeyError:
			print (colored("Error: Format not found", "red"))
			subprocess.Popen(["afplay", "chime-error.wav"])
		
	else:
		if cell is not None:
			print (colored("Error: No media selected", "red"))
			subprocess.Popen(["afplay", "chime-error.wav"])
		else:
			captureDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			if cmd == "BC-IN":
				updateMedia(ws, cell, "Recording", "Betacam deck", format_recording, captureDate)
				# print (requests.get("http://localhost:8081/mode/go"))
			elif cmd == "UM-IN":
				updateMedia(ws, cell, "Recording", "U-Matic deck", format_recording, captureDate)
			elif cmd == "DVCFW-IN":
				updateMedia(ws, cell, "Recording", "DVCPRO (FireWire) deck", format_recording, captureDate)
			elif cmd == "DVCA-IN":
				updateMedia(ws, cell, "Recording", "DVCPRO (analog) deck", format_recording, captureDate)
			elif cmd == "MDV-IN":
				updateMedia(ws, cell, "Recording", "MiniDV deck", format_recording, captureDate)
			elif cmd == "HI8-IN":
				updateMedia(ws, cell, "Recording", "Hi8 deck", format_recording, captureDate)
			elif cmd == "CASS-1-IN":
				updateMedia(ws, cell, "Recording", "Cassette deck 1", format_recording, captureDate)
			elif cmd == "CASS-2-IN":
				updateMedia(ws, cell, "Recording", "Cassette deck 2", format_recording, captureDate)
			elif cmd == "CASS-3-IN":
				updateMedia(ws, cell, "Recording", "Cassette deck 3", format_recording, captureDate)
			elif cmd == "BAKE":
				updateMedia(ws, cell, "Baking", "", format_tapesWithProblems, captureDate)
			elif cmd == "PRINT":
				try:
					ser = serial.Serial('/dev/tty.usbserial-120')  # open serial port
					for i in range(0, len(ws.row_values(cell.row))):
						rowProperties = ws.row_values(1)
						rowValues = ws.row_values(cell.row)
						ser.write(bytearray("{property}: {value}\n".format(property=rowProperties[i], value=rowValues[i]), "ascii", "ignore"))     # write a string
					ser.write(b"\n\n\n\n")
					ser.close()             # close port
				except:
					print (colored("Error: Printer not available", "red"))
					subprocess.Popen(["afplay", "chime-error.wav"])
