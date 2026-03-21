import serial
import time
import RPi.GPIO as GPIO

LatheCOM=serial.Serial('/dev/ttyUSB0', 9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.1)
RobotCOM=serial.Serial('/dev/ttyUSB1', 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, timeout=0.1)

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
GPIO.cleanup() #Reset gpio ports
GPIO.setmode(GPIO.BOARD) # Configure gpio on names, not numbers

GPIO.setup(IN1ST, GPIO.IN) #Configure to input
GPIO.setup(IN2ST, GPIO.IN)
GPIO.setup(IN1RB, GPIO.IN)
GPIO.setup(IN2RB, GPIO.IN)
GPIO.setup(INEST, GPIO.IN)

GPIO.setup(OUT1ST, GPIO.OUT) #Configure to output
GPIO.setup(OUT2ST, GPIO.OUT)
GPIO.setup(OUT1RB, GPIO.OUT)
GPIO.setup(OUT2RB, GPIO.OUT)
GPIO.setup(OUTEST, GPIO.OUT)

GPIO.output(OUT1ST, GPIO.LOW) #Write 0
GPIO.output(OUT2ST, GPIO.LOW)
GPIO.output(OUT1RB, GPIO.LOW)
GPIO.output(OUT2RB, GPIO.LOW)
GPIO.output(OUTEST, GPIO.HIGH) #Turn ON the E-stop

def LatheSend(command):
    command = "$$MACHINE FROM "+str(command).upper()+".FNC"+bytes.decode(b'\x0d', encoding = 'ascii')
    LatheCOM.write(bytes(command, encoding = 'ascii'))

def RobotSend(command):
    command = str(command)+bytes.decode(b'\x0d', encoding = 'ascii')+bytes.decode(b'\x0d', encoding = 'ascii')
    RobotCOM.write(bytes(command, encoding = 'ascii'))

def LatheWait():
    while (GPIO.input(IN1ST) == True):   #If this function started before applying command on lathe,
        time.sleep(0.001)                 #it waits the start of busyness of the lathe
    #while (GPIO.input(IN1ST) == False):  #Wait of the end of busyness of the lathe
        #time.sleep(0.001)

def RobotWait():
    while (GPIO.input(IN1RB) == True):
        time.sleep(0.001)
    while (GPIO.input(IN1RB) == False):
        time.sleep(0.001)

#_________________Moving Test Part____________________

#Prepare the lathe
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Door_Open')              #Open the door
LatheWait()
LatheSend('Chuck_Open')             #Open the chuck
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
#Put right billet in the lathe
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
####################### Maybe need to send settings command for robot
RobotSend('OB +4')                  # Shows robot is busy
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('MP 36,-334,600,-4,87')   #Up on right billet
RobotSend('MP 36,-334,380,-4,87')   #Little up on right billet
RobotSend('MP 36,-334,326,-4,87')   #Catch the right billet
RobotSend('GC')                     #Close the grip
RobotSend('MP 36,-334,380,-4,87')   #Little up on right billet
RobotSend('MP 36,-334,600,-4,87')   #Up on right billet
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP -57,296,550,17,134')  #In the chuck
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Chuck_Close')            #Close the chuck
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('GO')                     #Open the grip
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
# Machinning
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Door_Close')             #Close the door
LatheWait()
LatheSend('Machinning')             #Machinning
LatheWait()
LatheSend('Door_Open')              #Open the door
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
#Put right billet on the pallet
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP -57,296,550,17,134')  #In the chuck
RobotSend('GC')                     #Close the grip
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Chuck_Open')             #Open the chuck
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('MP 36,-334,600,-4,87')   #Up on right billet
RobotSend('MP 36,-334,380,-4,87')   #Little up on right billet
RobotSend('MP 36,-334,326,-4,87')   #Catch the right billet
RobotSend('GO')                     #Open the grip
RobotSend('MP 36,-334,380,-4,87')   #Little up on right billet
RobotSend('MP 36,-334,600,-4,87')   #Up on right billet
RobotSend('OB -4')
# RobotSend Output
RobotWait()
#Put left billet in the lathe
RobotSend('OB +4')
RobotSend('MP 88,-326,600,-4,87')   #Up on left billet
RobotSend('MP 88,-326,380,-4,87')   #Little up on left billet
RobotSend('MP 88,-326,326,-4,87')   #Catch the left billet
RobotSend('GC')                     #Close the grip
RobotSend('MP 88,-326,380,-4,87')   #Little up on left billet
RobotSend('MP 88,-326,600,-4,87')   #Up on left billet
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP -57,296,550,17,134')  #In the chuck
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Chuck_Close')            #Close the chuck
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('GO')                     #Open the grip
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
# Machinning
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Door_Close')             #Close the door
LatheWait()
LatheSend('Machinning')             #Machinning
LatheWait()
LatheSend('Door_Open')              #Open the door
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
#Put left billet on the pallet
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP -57,296,550,17,134')  #In the chuck
RobotSend('GC')                     #Close the grip
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free
GPIO.output(OUT1ST, GPIO.HIGH)      #__Show the lathe is busy
LatheSend('Chuck_Open')             #Open the chuck
LatheWait()
GPIO.output(OUT1ST, GPIO.LOW)       #__Show the lathe is free
GPIO.output(OUT1RB, GPIO.HIGH)      #__Show the robot is busy
RobotSend('OB +4')
RobotSend('MP 0,300,550,25,134')    #In front of chuck
RobotSend('MP 0,88,519,9,151')      #In front of lathe
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('MP 88,-326,600,-4,87')   #Up on left billet
RobotSend('MP 88,-326,380,-4,87')   #Little up on left billet
RobotSend('MP 88,-326,326,-4,87')   #Catch the left billet
RobotSend('GO')                     #Open the grip
RobotSend('MP 88,-326,380,-4,87')   #Little up on left billet
RobotSend('MP 88,-326,600,-4,87')   #Up on left billet
RobotSend('MP 56,11,537,-10,142')   #Home
RobotSend('OB -4')
# RobotSend Output
RobotWait()
GPIO.output(OUT1RB, GPIO.LOW)       #__Show the robot is free


    
