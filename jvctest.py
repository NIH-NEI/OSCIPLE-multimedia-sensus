import serial, time

ser = serial.Serial("/dev/tty.usbserial-140", 9600)

# ser.write(b"\x3f\x0a") # stop
# ser.write(b"\xab\x0a") # ff
# ser.write(b"\xac\x0a") # rew
# ser.write(b"\xa3\x0a") # eject
# ser.write(b"\x3a\x0a") # play
# ser.write(b"\xd7\x0a") # status sense

time.sleep(0.1)

def deckResponse():
	time.sleep(.1)
	charcount = ser.inWaiting()
	rtn = ser.read(charcount)
	# for i in range(0, charcount):
	# 	print (hex(rtn[i]), bin(rtn[i]))
  
	return rtn

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
    
    
# ser.write(b"\x3f\x0a") # stop
# ser.write(b"\xab\x0a") # ff
# ser.write(b"\xac\x0a") # rew
# ser.write(b"\xa3\x0a") # eject
# ser.write(b"\x3a\x0a") # play
# ser.write(b"\xd7\x0a") # status sense
ser.write(b"\xd9\x0a") # ctl sense

print (deckResponse())
# time.sleep(1)    
# print(jvcDeckStatus(ser))