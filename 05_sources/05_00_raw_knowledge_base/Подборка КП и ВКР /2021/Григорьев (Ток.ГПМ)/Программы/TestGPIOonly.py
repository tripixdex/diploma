# %Run ProbV17E.py
import time
import RPi.GPIO as GPIO

IN1ST = 7 # Input 1 from stanok
IN2ST = 5
IN1RB = 8 # Input 1 from robot
IN2RB = 3
INEST = 10 # Input e-stop
OUT1ST = 15
OUT2ST = 16
OUT1RB = 13
OUT2RB = 11
OUTEST = 12

GPIO.setwarnings(False)
GPIO.cleanup() #reset gpio ports
GPIO.setmode(GPIO.BOARD) # configure gpio on names, not numbers

GPIO.setup(IN1ST, GPIO.IN) #configure to input
GPIO.setup(IN2ST, GPIO.IN)
GPIO.setup(IN1RB, GPIO.IN)
GPIO.setup(IN2RB, GPIO.IN)
GPIO.setup(INEST, GPIO.IN)

GPIO.setup(OUT1ST, GPIO.OUT) #configure to output
GPIO.setup(OUT2ST, GPIO.OUT)
GPIO.setup(OUT1RB, GPIO.OUT)
GPIO.setup(OUT2RB, GPIO.OUT)
GPIO.setup(OUTEST, GPIO.OUT)

GPIO.output(OUT1ST, GPIO.LOW) #write 0
GPIO.output(OUT2ST, GPIO.LOW)
GPIO.output(OUT1RB, GPIO.LOW)
GPIO.output(OUT2RB, GPIO.LOW)
GPIO.output(OUTEST, GPIO.HIGH)

while 1:
    command = input("input command: ")
    
    if (int(command[4]))==1:
        GPIO.output(OUTEST, GPIO.HIGH)
    else:
        GPIO.output(OUTEST, GPIO.LOW)
    
    if (int(command[3]))==1:
        GPIO.output(OUT2RB, GPIO.HIGH)
    else:
        GPIO.output(OUT2RB, GPIO.LOW)
    
    if (int(command[2]))==1:
        GPIO.output(OUT1RB, GPIO.HIGH)
    else:
        GPIO.output(OUT1RB, GPIO.LOW)
    
    if (int(command[1]))==1:
        GPIO.output(OUT2ST, GPIO.HIGH)
    else:
        GPIO.output(OUT2ST, GPIO.LOW)
    
    if (int(command[0]))==1:
        GPIO.output(OUT1ST, GPIO.HIGH)
    else:
        GPIO.output(OUT1ST, GPIO.LOW)
    
    Inputs = ['0', '0', '0', '0', '0']
    if (GPIO.input(IN1ST) == True):
        Inputs[0]='1'
    if (GPIO.input(IN2ST) == True):
        Inputs[1]='1'
    if (GPIO.input(IN1RB) == True):
        Inputs[2]='1'
    if (GPIO.input(IN2RB) == True):
        Inputs[3]='1'
    if (GPIO.input(INEST) == True):
        Inputs[4]='1'
    
    print(Inputs)
    
    
