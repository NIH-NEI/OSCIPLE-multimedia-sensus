import obsws_python as obs
import serial, time, argparse
from termcolor import colored
from threading import Thread
from http.server import BaseHTTPRequestHandler,HTTPServer
PORT_NUMBER = 8081

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="idle")
parser.add_argument('--deck', default="betacam")
parser.add_argument('--obs', default="192.168.1.173")
parser.add_argument('--skippack', default="no")
args = parser.parse_args()

if args.deck == "betacam":
	ser = serial.Serial("/dev/tty.usbserial-A10N3SUD", 38400,
							 serial.EIGHTBITS, serial.PARITY_ODD,
							 serial.STOPBITS_ONE)
elif args.deck == "vhs":
    ser = serial.Serial("/dev/tty.usbserial-140", 9600)
else:
    print ("deck not found: {rofl}".format(rofl=args.deck))
    
print (ser)


cl = obs.ReqClient(host=args.obs, port=4455, password='mylife')


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
	
def deckResponse():
	time.sleep(.1)
	charcount = ser.inWaiting()
	rtn = ser.read(charcount)
	# for i in range(0, charcount):
	# 	print (hex(rtn[i]), bin(rtn[i]))
  
	return rtn
	
def sonyDeckStatus(ser):
	sonySend(ser, 6, b"\x20", b'\x0a')
	status = deckResponse()
	
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
	else:
		return status

def jvcDeckStatus(ser):
    ser.write(b"\xd7\x0a")
    status = deckResponse()
    
    if status[3] & 0b10000000:
        return "play"
    if status[3] & 0b01000000:
        return "fast forward"
    if status[3] & 0b00100000:
        return "rewind"
    if status[3] & 0b00010000:
        return "stop"
    if status[3] & 0b00001000:
        return "standby"
    if status[3] & 0b00000100:
        return "eject"
    if status[3] & 0b00000010:
        return "record" # uh oh
    if status[3] & 0b00000001:
        return "a dub mode"
    
    return status
    
    
    
def deckStatus(deck, ser):
    if deck == "betacam":
        return sonyDeckStatus(ser)
    elif deck == "vhs":
        return jvcDeckStatus(ser)
    
    

# ser.write(b"\x3f\x0a") # stop
# ser.write(b"\xab\x0a") # ff
# ser.write(b"\xac\x0a") # rew
# ser.write(b"\xa3\x0a") # eject
# ser.write(b"\x3a\x0a") # play
# ser.write(b"\xd7\x0a") # status sense


# sonySend(ser, 6, b"\x20", b'\x0a') # status
# sonySend(ser, 2, b"\x01")  # play
# sonySend(ser, 2, b"\x00")  # stop
# sonySend(ser, 2, b"\x10")  # fast forward
# sonySend(ser, 2, b"\x20")  # rewind
# sonySend(ser, 2, b"\x0f")  # eject

def deckSend(deck, command):
    jvcCommands = {"stop": b"\x3f\x0a",
                   "fast forward": b"\xab\x0a",
                   "rewind": b"\xac\x0a",
                   "eject": b"\xa3\x0a",
                   "play": b"\x3a\x0a",
                   "status": b"\xd7\x0a"}
    
    sonyCommands = {"status": (ser, 6, b"\x20", b'\x0a'),
                    "play": (ser, 2, b"\x01"),
                    "stop": (ser, 2, b"\x00"),
                    "fast forward": (ser, 2, b"\x10"),
                    "rewind": (ser, 2, b"\x20"),
                    "eject": (ser, 2, b"\x0f")}
    
    if deck=="vhs":
        ser.write(jvcCommands[command])
    elif deck=="betacam":
        sonySend(sonyCommands[command]())
    else:
        print (colored("error: {deck} not found!".format(deck=deck), "red"))
        
	
	


def mode_idle():
	print ("idle")
	
def mode_go():
	global MODE, ser
	print ("go")
 
	status = deckStatus(args.deck, ser)
	if status == "standby" or status == "stop":
		if args.skippack != "no":
			print ("tape inserted; fast-forwarding")
			deckSend(args.deck, "fast forward")
		else:
			print ("tape inserted.  pack is being skipped by request; rewinding instead")
			deckSend(args.deck, "rewind")
			MODE = "pack"
	elif status == "fast forward":
		print ("tape is fast-forwarding; switching to 'pack' mode")
		MODE = "pack"
	elif status == "rewind":
		print ("tape is already rewinding; switching to 'pack' mode")
		MODE = "pack"
	elif status == "tape out":
		print ("tape out; waiting for tape to be inserted")
	elif status == "play":
		print ("the tape is playing prematurely; stopping and resuming fast forward")
		# sonySend(ser, 2, b"\x00")  # stop
		deckSend(args.deck, "stop")
		time.sleep(1)
		# sonySend(ser, 2, b"\x10")  # fast forward
		deckSend(args.deck, "fast forward")
	else:
		print (status)
		

	
def mode_pack():
	global MODE
	print ("pack")

	status = deckStatus(args.deck, ser)
	if status == "standby" or status == "stop":
		print ("tape has returned to standby mode; switching to 'obsrecord' mode")
		MODE = "obsrecord"
	elif status == "play":
		print ("the tape is playing prematurely; stopping and rewinding")
		deckSend(args.deck, "stop")
		time.sleep(1)
		deckSend(args.deck, "rewind")
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
	cl.set_current_program_scene("slate")
	cl.start_record()
	time.sleep(5)
	cl.set_current_program_scene("record")
	MODE = "ingest"
	
	
def mode_ingest():
	global MODE
	print ("ingest")
 
	status = deckStatus(args.deck, ser)
	if status == "standby" or status == "stop":
		print ("beginning ingest")
		# sonySend(ser, 2, b"\x01")  # play
		deckSend(args.deck, "play")
	elif status == "play":
		print ("play successful; switching to waitforfinish")
		MODE = "waitforfinish"
	# else:
	# 	print ("unexpected deck status {status}; aborting".format(status=status))
	# 	MODE = "idle"
  

def mode_waitforfinish():
	global MODE
	
	status = deckStatus(args.deck, ser)
	if status == "play":
		print ("recording")
	else:
		print ("tape seems to be finished")
		MODE = "finished"

def mode_finished():
	global MODE
	# sonySend(ser, 2, b"\x0f")  # eject
	deckSend(args.deck, "eject")
	cl.stop_record()
	print ("finished")
	MODE = "idle"


def mode_error():
	global MODE
	print ("error")

modes = {"idle": mode_idle,
		 "go": mode_go,
		 "pack": mode_pack,
		 "obsrecord": mode_obsrecord,
		 "ingest": mode_ingest,
		 "waitforfinish": mode_waitforfinish,
		 "finished": mode_finished,
		 "error": mode_error,
}

MODE = args.mode


	



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



