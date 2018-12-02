import RPi.GPIO as GPIO
import time

#
#Constants defined here
#
#these constants represent the GPIO pins the sensors are connected to
DOOR_1_RELAY = 17
DOOR_2_RELAY = 18

#the log file name is set here
LOG_FILENAME = '/home/pi/ds.log'


5
#
#Variables defined here
#
#these variables track whether the door is currently open 
door_1_current = False
door_2_current = False

#these variables are used to track the current and previous sensor state read from the GPIO
#
#Function definitions start here
#
#
#Code starts here
#
#set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DOOR_1_RELAY, GPIO.OUT)
GPIO.setup(DOOR_2_RELAY, GPIO.OUT)

#The main loop
while True:

	#delay a little bit
	time.sleep(2)
	
	#read the sensors
	door_1_sensor_state = GPIO.output(DOOR_1_RELAY, GPIO.HIGH)
	print ("Turned On: ", door_1_sensor_state)
	time.sleep(2)
	door_1_sensor_state = GPIO.output(DOOR_1_RELAY, GPIO.LOW)
	print ("Turned Off: ", door_1_sensor_state)
#Cleanup the GPIO
GPIO.cleanup ()