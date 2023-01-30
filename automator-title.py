
from flask import Flask, request, make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Bioviz Ingest - NIH History Batch 2")



app = Flask(__name__)

@app.route("/title")
def title():
	deck = request.args["deck"]
	print (deck)
	
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
	else:
		mediaTitle = "deck not recognized"
  
	print (mediaTitle)
  
	rofl = "<html><head><body><div style='color: white; font-size:72px'>{mediaTitle}</div><div style='color: white; font-size:72px'>Biovisualization, LLC</div></body></html>".format(mediaTitle=mediaTitle)
	print (rofl)
		
	resp = make_response(rofl, 200)
	resp.mimetype = "text/html"

	print (resp.data)
	return resp

