import serial, time
from threading import Thread
from http.server import BaseHTTPRequestHandler,HTTPServer
PORT_NUMBER = 8081

ser = serial.Serial("/dev/tty.usbserial-A10N3SUD", 38400,
							 serial.EIGHTBITS, serial.PARITY_ODD,
							 serial.STOPBITS_ONE)


def sonyChecksum(msg):
	checksum = 0
	for i in msg:
		checksum += i
		
	return (checksum & 255).to_bytes(1,'big')

def sonySend(ser, cmdone, cmdtwo, data=b'', tempchecksum=0):
	datacount = len(data)
	cmd1 = (cmdone << 4) + (datacount & 15)
	msg = cmd1.to_bytes(1, 'big') + cmdtwo + data
	msg = msg + sonyChecksum(msg)
	# for i in msg:
	# 	print (hex(i), bin(i))
	ser.write(msg)
	
def sonyResponse():
	time.sleep(.1)
	charcount = ser.inWaiting()
	rtn = ser.read(charcount)
	# for i in range(0, charcount):
	# 	print (hex(rtn[i]), bin(rtn[i]))
  
	return rtn
	
def sonyDeckStatus(ser):
	sonySend(ser, 6, b"\x20", b'\x0a')
	status = sonyResponse()
	
	if status[2] == 0x30:
		return "tape out"
	elif status[2] == 0x10 and status[3] == 0xa0:
		return "standby"
	elif status[2] == 0x10 and status[3] == 0x81:
		return "play"
	elif status[2] == 0x10 and status[3] == 0x84:
		return "fast forward"
	elif status[2] == 0x10 and status[3] == 0x88:
		return "rewind"
	
	


def mode_idle():
	print ("idle")
	
def mode_go():
	global MODE
	print ("go")
 
	status = sonyDeckStatus(ser)
	if status == "standby":
		print ("tape inserted; fast-forwarding")
		sonySend(ser, 2, b"\x10")  # fast forward
	elif status == "fast forward":
		print ("tape is fast-forwarding; switching to 'pack' mode")
		MODE = "pack"
	elif status == "rewind":
		print ("tape is already rewinding; switching to 'pack' mode")
		MODE = "pack"
	elif status == "tape out":
		print ("tape out; waiting for tape to be inserted")
	elif status == "playing":
		print ("the tape is playing prematurely; stopping and resuming fast forward")
		sonySend(ser, 2, b"\x00")  # stop
		time.sleep(1)
		sonySend(ser, 2, b"\x10")  # fast forward
		

	
def mode_pack():
	global MODE
	print ("pack")

	status = sonyDeckStatus(ser)
	if status == "standby":
		sonySend(ser, 2, b"\x01")  # play
		print ("tape has returned to standby mode; playing tape")
	elif status == "play":
		print ("tape has started playing; switching to 'ingest' mode")
		MODE = "ingest"
	elif status == "fast forward":
		print ("tape is still fast-forwarding; pack still in progress")
	elif status == "rewind":
		print ("tape is still rewinding; pack still in progress")
	elif status == "tape out":
		print ("tape has been ejected; canceling and returning to idle")
		MODE = "idle"
  
  
def mode_obsrecord():
	global MODE
	print ("obsrecord")
	
def mode_ingest():
	global MODE
	print ("ingest")
	
def mode_finished():
	global MODE
	print ("finished")
	
def mode_eject():
	global MODE
	print ("eject")

def mode_error():
	global MODE
	print ("error")

modes = {"idle": mode_idle,
		 "go": mode_go,
		 "pack": mode_pack,
		 "obsrecord": mode_obsrecord,
		 "ingest": mode_ingest,
		 "finished": mode_finished,
		 "eject": mode_eject,
		 "error": mode_error,
}

MODE = "idle"


	



# ser.write(0)
# sonySend(ser, 6, b"\x20", b'\x0a') # status
# sonySend(ser, 2, b"\x01")  # play
# sonySend(ser, 2, b"\x00")  # stop
# sonySend(ser, 2, b"\x10")  # fast forward
# sonySend(ser, 2, b"\x20")  # rewind
# sonySend(ser, 2, b"\x0f")  # eject
# print()


# time.sleep(.1)
# charcount = ser.inWaiting()
# rtn = ser.read(charcount)
# for i in range(0, charcount):
# 	print (hex(rtn[i]), bin(rtn[i]))


# ser.close()


def requestHandler_index(_get):
	return "text/html", "<html><body><h1>betacam server</h1></body></html>"

def requestHandler_mode(_get):
	global MODE
	mode = _get[2]
	if mode in modes:
		MODE = mode
	print(mode)

	return "text/plain", mode




httpRequests = {''      : requestHandler_index,
				'mode': requestHandler_mode,
}


class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		elements = self.path.split('/')

		responseFound = False
		for httpRequest, httpHandler in httpRequests.items():
			# print elements[1] + " == " + httpRequest
			if elements[1] == httpRequest: # in other words, if the first part matches
				contentType, response = httpHandler(elements)
				responseFound = True

				self.send_response(200)
				# self.send_header("Access-Control-Allow-Origin", "*")
				self.send_header('Content-type', contentType)
				self.end_headers()

				self.wfile.write(bytes(response, "utf-8"))
		if not responseFound:
			contentType, response = requestHandler_index('/')

			self.send_response(200)
			# self.send_header("Access-Control-Allow-Origin", "*")
			self.send_header('Content-type', contentType)
			self.end_headers()

			self.wfile.write(bytes(response, "utf-8"))
			
		return


def http():
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)

	server.serve_forever()

httpThread = Thread(target=http)
httpThread.daemon = True
httpThread.start()



while True:
	modes[MODE]()
	time.sleep(5)



