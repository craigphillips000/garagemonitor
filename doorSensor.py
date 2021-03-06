import RPi.GPIO as GPIO
import time
#
#This module monitors the GPIO pins connected to the two garage door sensors and writes a message to a log when the state changes for either door. 
#It also writes a message to the log if it determines that either door has been open longer than a specified time.
#
#Constants defined here
#
#these constants represent the GPIO pins the sensors are connected to
DOOR_1_SENSOR = 12
DOOR_2_SENSOR = 13

#Door open duration alarm time in minutes
DOOR_OPEN_ALARM = 10

#These constants are used to evaluate the door sensors
CLOSED = 0
OPEN = 1

#These constants are used to signal which door a message applies to
GARAGE_DOOR_1 = 1
GARAGE_DOOR_2 = 2

#the log file name is set here
LOG_FILENAME = '/home/pi/gdm/ds.log'

#
#Variables defined here
#
#these variables track whether the door is currently open 
door_1_current = False
door_2_current = False

#these variables are used to track the current and previous sensor state read from the GPIO

door_1_previous_state = CLOSED
door_2_previous_state = CLOSED
door_1_sensor_state = CLOSED
door_2_sensor_state = CLOSED

#these variables track how long the door has been open in ticks(seconds)
door_1_open_duration = time.time()
door_2_open_duration = time.time()

#these variables track how many segments the door has been opened
door_1_open_segment_counter = 0
door_2_open_segment_counter = 0

#
#Function definitions start here
#
def write_message_to_log(message, garage_door):
        logfile = open(LOG_FILENAME, 'a')
        logfile.write(str(time.time()) + ' ' + str(garage_door) + ' ' + time.asctime(time.localtime(time.time())) + ': ')
        logfile.write(message + '\n')
        logfile.close()
	return 1
        
#
#Code starts here
#
#set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DOOR_1_SENSOR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(DOOR_2_SENSOR, GPIO.IN, GPIO.PUD_UP)

#Write open message to the logfile.
write_message_to_log('File opened.',0)

#set up messages
door_1_sensor_state = GPIO.input(DOOR_1_SENSOR)
door_2_sensor_state = GPIO.input(DOOR_2_SENSOR)
door_1_previous_state = door_1_sensor_state
door_2_previous_state = door_2_sensor_state

if door_1_sensor_state == OPEN:
	write_message_to_log("doorSensorStarting: Garage Door 1 is Open", GARAGE_DOOR_1)
else:
	write_message_to_log("doorSensorStarting: Garage Door 1 is Closed", GARAGE_DOOR_1)
	
if door_2_sensor_state == OPEN:
	write_message_to_log("doorSensorStarting: Garage Door 2 is Open", GARAGE_DOOR_2)
else:
	write_message_to_log("doorSensorStarting: Garage Door 2 is Closed", GARAGE_DOOR_2)

#The main loop
while True:

	#delay a little bit
	time.sleep(10)
	
	#read the sensors
	door_1_sensor_state = GPIO.input(DOOR_1_SENSOR)
	door_2_sensor_state = GPIO.input(DOOR_2_SENSOR)

	#Have they changed?
	if door_1_sensor_state != door_1_previous_state:
		door_1_previous_state = door_1_sensor_state
		if door_1_sensor_state == CLOSED:
			write_message_to_log('Door 1 has closed.',GARAGE_DOOR_1)
			door_1_open_segment_counter = 0
			door_1_current = True
		else:
			write_message_to_log('Door 1 has opened.',GARAGE_DOOR_1)
			door_1_open_duration = time.time()
			door_1_current = False

	if door_2_sensor_state != door_2_previous_state:
		door_2_previous_state = door_2_sensor_state
		if door_2_sensor_state == CLOSED:
			write_message_to_log('Door 2 has closed.',GARAGE_DOOR_2)
			door_2_open_segment_counter = 0
			door_2_current = True
		else:
			write_message_to_log('Door 2 has opened.',GARAGE_DOOR_2)
			door_2_open_duration = time.time()
			door_2_current = False
			
	#Check if either door open for more than door open alarm limit in minutes
	if ((time.time() - door_1_open_duration) > (DOOR_OPEN_ALARM * 60)) & (door_1_sensor_state == OPEN):
		door_1_open_duration = time.time()
		door_1_open_segment_counter = door_1_open_segment_counter + 1
		write_message_to_log('Door 1 has been open for ' +
                                     str(DOOR_OPEN_ALARM * door_1_open_segment_counter) +
                                     ' minutes.',GARAGE_DOOR_1)
	
	if ((time.time() - door_2_open_duration) > (DOOR_OPEN_ALARM * 60)) & (door_2_sensor_state == OPEN):
		door_2_open_duration = time.time()
		door_2_open_segment_counter = door_2_open_segment_counter + 1
		write_message_to_log('Door 2 has been open for ' +
                                     str(DOOR_OPEN_ALARM * door_2_open_segment_counter) +
                                     ' minutes.',GARAGE_DOOR_2)

#Cleanup the GPIO
GPIO.cleanup ()
