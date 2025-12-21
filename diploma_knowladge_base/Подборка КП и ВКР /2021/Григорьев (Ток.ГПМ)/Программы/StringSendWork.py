# %Run ProbV17E.py
import serial
import time
Com0=serial.Serial('/dev/ttyUSB1', 9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.1)
while 1:
    command = input("input command: ")
    command = "$$MACHINE FROM "+str(command).upper()+".FNC"+bytes.decode(b'\x0d', encoding = 'ascii')
    Com0.write(bytes(command, encoding = 'ascii'))

    report = str(Com0.readline(), encoding = 'ascii')
 
    print(command)
    print(report)