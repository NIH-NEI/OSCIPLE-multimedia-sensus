import serial, time

ser = serial.Serial("/dev/tty.usbserial-A10N3SUD", 38400,
                             serial.EIGHTBITS, serial.PARITY_ODD,
                             serial.STOPBITS_ONE)

print (ser.rts)
print (ser.cts)

# ser.setRTS(True)
# ser.write(0)
# time.sleep(1)


# ser.open()

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
    for i in msg:
        print (hex(i), bin(i))
    ser.write(msg)
    
    
def sonySend2(ser, cmd1, cmdtwo, data=b'', tempchecksum=0):
    datacount = len(data)
    # cmd1 = (cmdone << 4) + (datacount & 15)
    msg = cmd1.to_bytes(1, 'big') + cmdtwo + data
    msg = msg + sonyChecksum(msg)
    for i in msg:
        print (hex(i), bin(i))
    ser.write(msg)
    
    


# ser.write(0)
sonySend(ser, 6, b"\x20", b'\x0a') # status
# sonySend(ser, 2, b"\x01")  # play
# sonySend(ser, 2, b"\x00")  # stop
# sonySend(ser, 2, b"\x10")  # fast forward
# sonySend(ser, 2, b"\x20")  # rewind
# sonySend(ser, 2, b"\x0f")  # eject
print()

# while True:
#     ser.write(1)

# ser.write(1)

# print (ser.read(4))
time.sleep(.1)
charcount = ser.inWaiting()
rtn = ser.read(charcount)
for i in range(0, charcount):
	print (hex(rtn[i]), bin(rtn[i]))
# while rofl 
#     print (rofl)
# for i in ser:
#     print (ord(i))
# print (rtn)


 


ser.close()