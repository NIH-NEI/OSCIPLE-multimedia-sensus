import gspread, datetime, subprocess, requests, serial, traceback
from termcolor import colored
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Bioviz Ingest - NIH History Batch 3")

commandHistory = []

formatsToSheets = {"BC": "Betacam",
				   "BSP": "Betacam SP",
				   "DVC": "DVCPRO",
				   "HI8": "Hi8",
				   "MDV": "MiniDV",
				   "UM": "U-Matic",
	   			   "CASS": "Cassette",
				   "TEST": "Tester tapes",
				   "VHS": "VHS",
	   			   "FD": "Floppy disk"}

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



class Automator:
	def __init__(self):
		self.cell = None
		self.ws = None
  
	def findRecordingDeck(self, deck):
		if deck == "betacam":
			ws = sheet.worksheet("Betacam")
			cell = ws.find("Recording")
			print ("cell: ", cell)
			if cell == None:
				ws = sheet.worksheet("Betacam SP")
				cell = ws.find("Recording")
				print ("cell: ", cell)
				if cell == None:
					mediaTitle = "None"
				else:
					mediaTitle = ws.cell(cell.row, 1).value
					
			else:
				mediaTitle = ws.cell(cell.row, 1).value
		elif deck == "umatic":
			ws = sheet.worksheet("U-Matic")
			cell = ws.find("Recording")
			if cell == None:
				mediaTitle = "None"
			else:
				mediaTitle = ws.cell(cell.row, 1).value
	
		elif deck == "hi8":
			ws = sheet.worksheet("Hi8")
			cell = ws.find("Recording")
			if cell == None:
				mediaTitle = "None"
			else:
				mediaTitle = ws.cell(cell.row, 1).value
	
		elif deck == "vhs":
			ws = sheet.worksheet("VHS")
			cell = ws.find("Recording")
			if cell == None:
				mediaTitle = "None"
			else:
				mediaTitle = ws.cell(cell.row, 1).value
	
		else:
			mediaTitle = "deck not recognized"
   
		return mediaTitle

	def updateMedia(self, stageName, location, format, captureDate=""):
		rowcolrange = gspread.utils.rowcol_to_a1(self.cell.row, 1)+":"+gspread.utils.rowcol_to_a1(self.cell.row, self.ws.col_count)
		self.ws.update_cell(self.cell.row, 3, stageName)
		self.ws.update_cell(self.cell.row, 4, location)
		if captureDate != "":
			self.ws.update_cell(self.cell.row, 2, captureDate)
		format_cell_range(self.ws, rowcolrange, format)
		msg = "Updated {media} to {stageName}, {location}".format(media=self.cell.value, stageName=stageName, location=location)
		# print (colored(msg, "green"))
		subprocess.Popen(["afplay", "chime-success.wav"])
		
		
		deckMedia = ""
		deckLocation = self.ws.title
		if stageName == "Recording":
			deckStatus = "Recording"
			deckMedia = self.cell.value
		elif stageName == "Awaiting QC":
			deckStatus = "Idle"
		else:
			deckStatus = "Unknown"

		wtf =  {0: {"messageType": "updateMedia", "message": {"media": self.cell.value, "stageName": stageName, "location": location}},
			1: {"messageType": "success", "message": msg},
   			2: {"messageType": "deckStatus", "message": {"deck": deckLocation, "status": deckStatus, "media": deckMedia}}}
		print (colored(wtf, "yellow"))
		return wtf
 
 
	def lcd(self, line1, line2, color=""):
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
  
  
	def commandParse(self, cmd):
		# global cell, ws
		cmd = cmd.upper()
		
		commandHistory.append([cmd, datetime.datetime.now()])
	
		if cmd[0:4] == "HS-3":
			# lcd(cmd, "", "y")
			if cmd[5:7] == "ST":
				if self.cell is None:
					# print (colored("Error: No media selected", "red"))
					subprocess.Popen(["afplay", "chime-error.wav"])
					return {0: {"messageType": "error", "message": "Error: No media selected"}}
				else:
					stage = int(cmd[7:8])
					bin = int(cmd[10:11])
					if stage == 2:
						return self.updateMedia("Serial assigned", "Bin {bin}".format(bin=bin), format_serialAssigned)
					elif stage == 4:
						return self.updateMedia("Awaiting QC", "Bin {bin}".format(bin=bin), format_awaitingQC)
					elif stage == 5:
						return self.updateMedia("Outbox", "Bin {bin}".format(bin=bin), format_outbox)
					elif stage == 6:
						return self.updateMedia("Tapes with problems", "Bin {bin}".format(bin=bin), format_tapesWithProblems)
			else:
				format = cmd.split("-")[2]
	
				try:
					self.ws = sheet.worksheet(formatsToSheets[format])
					print (self.ws)
					self.cell = self.ws.find(cmd)
					print (self.cell)
					if self.cell is not None:
						rowProperties = self.ws.row_values(1)
						rowValues = self.ws.row_values(self.cell.row)
						rtn = {}
						for i in range(0, len(self.ws.row_values(self.cell.row))):
							property = rowProperties[i]
							value = rowValues[i]
							color = "white"
							if property == "Stage":
								if value == "Inbox":
									color = "magenta"
								elif value == "Serial assigned":
									color = "blue"
								elif value == "Awaiting QC":
									color = "yellow"
								elif value == "Outbox":
									color = "green"
								elif value == "Tapes with problems":
									color = "red"
							# print (colored("{property}: {value}".format(property=rowProperties[i], value=rowValues[i]), color))
							rtn[property] = value
						subprocess.Popen(["afplay", "chime-read.wav"])
						return {0: {"messageType": "media", "message": rtn}}
					else:
						# print (colored("Error: Media not found", "red"))
						subprocess.Popen(["afplay", "chime-error.wav"])
						return {0: {"messageType": "error", "message": "Error: No media selected"}}
				except KeyError:
					# print (colored("Error: Format not found", "red"))
					# traceback.print_exc()
					subprocess.Popen(["afplay", "chime-error.wav"])
					return {0: {"messageType": "error", "message": traceback.format_exc()}}
		
		elif cmd[0:4] == "TEST":
			format = "TEST"
			try:
				self.ws = sheet.worksheet(formatsToSheets[format])
				self.cell = self.ws.find(cmd)
				if self.cell != None:
					rowProperties = self.ws.row_values(1)
					rowValues = self.ws.row_values(self.cell.row)
					for i in range(0, len(self.ws.row_values(self.cell.row))):
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
	
		elif cmd == "VHS-DONE":
			try:
				print (requests.get("http://localhost:8081/mode/finished"))
			except:
				print (colored("Error sending message to vhs server", "red"))
				return {0: {"messageType": "error", "message": "Error sending message to betacam server"}}

		else:
			if self.cell is None:
				print (colored("Error: No media selected", "red"))
				subprocess.Popen(["afplay", "chime-error.wav"])
				return {0: {"messageType": "error", "message": "Error: No media selected"}}
			else:
				captureDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				if cmd == "BC-IN":
					# try:
					# 	print (requests.get("http://192.168.1.140:8081/mode/go"))
					# except:
					# 	print (colored("Error sending message to betacam server", "red"))
					return self.updateMedia("Recording", "Betacam deck", format_recording, captureDate)
				elif cmd == "UM-IN":
					return self.updateMedia("Recording", "U-Matic deck", format_recording, captureDate)
				elif cmd == "DVCFW-IN":
					return self.updateMedia("Recording", "DVCPRO (FireWire) deck", format_recording, captureDate)
				elif cmd == "DVCA-IN":
					return self.updateMedia("Recording", "DVCPRO (analog) deck", format_recording, captureDate)
				elif cmd == "MDV-IN":
					return self.updateMedia("Recording", "MiniDV deck", format_recording, captureDate)
				elif cmd == "HI8-IN":
					return self.updateMedia("Recording", "Hi8 deck", format_recording, captureDate)
				elif cmd == "VHS-IN":
					return self.updateMedia("Recording", "VHS deck", format_recording, captureDate)
					try:
						print (requests.get("http://localhost:8081/mode/go"))
					except:
						print (colored("Error sending message to betacam server", "red"))
				elif cmd == "CASS-1-IN":
					return self.updateMedia("Recording", "Cassette deck 1", format_recording, captureDate)
				elif cmd == "CASS-2-IN":
					return self.updateMedia("Recording", "Cassette deck 2", format_recording, captureDate)
				elif cmd == "CASS-3-IN":
					return self.updateMedia("Recording", "Cassette deck 3", format_recording, captureDate)
				elif cmd == "BAKE":
					return self.updateMedia("Baking", "", format_tapesWithProblems, captureDate)
				elif cmd == "PRINT":
					try:
						ser = serial.Serial('/dev/tty.usbserial-120')  # open serial port
						for i in range(0, len(self.ws.row_values(self.cell.row))):
							rowProperties = self.ws.row_values(1)
							rowValues = self.ws.row_values(self.cell.row)
							ser.write(bytearray("{property}: {value}\n".format(property=rowProperties[i], value=rowValues[i]), "ascii", "ignore"))     # write a string
						ser.write(b"\n\n\n\n")
						ser.close()             # close port
					except:
						print (colored("Error: Printer not available", "red"))
						subprocess.Popen(["afplay", "chime-error.wav"])
	

automator = Automator()

if __name__ == "__main__":
	while True:
		print ()
		cmd = input()
		print (automator.commandParse(cmd))
 
	
