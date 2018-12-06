import os
import time
import requests
import json
from picamera import PiCamera
import RPi.GPIO as GPIO
#
#This module monitors the telegram bot and processes responses from the keyboard sent to the user
#
#Constants defined here
#
LOG_FILENAME = '/home/pi/gdm/actionEngine.log'
TELEGRAM_URL_FILE = '/home/pi/gdm/telegram_url.txt'
PHOTO_FILE = '/home/pi/gdm/images/image.jpg'
VIDEO_FILE = '/home/pi/gdm/images/video.h264'
CONVERTED_VIDEO_FILE = '/home/pi/gdm/images/video.mp4'
UPDATEID_FILE = '/home/pi/gdm/previous_updateID.txt'
getUpdate_TIMEOUT = 600          #long polling timeout
GARAGE_DOOR_1 = 1
GARAGE_DOOR_2 = 2
VIDEO_RECORDING_TIME = 10
DOOR_1_RELAY = 17
DOOR_2_RELAY = 18

#variables defined here
#
#
previous_message_count = 0
new_message_count      = 0
message_time	= 0.0
current_message = '' 
#
#Function definitions start here
#
def write_message_to_log(message):
        logfile = open(LOG_FILENAME, 'a')
        logfile.write(str(time.asctime(time.localtime(time.time()))) + ': ' + str(message) + '\n')
        logfile.close()
	return 1
#
def get_telegram_message(next_updateID):
	telegram_file = open(TELEGRAM_URL_FILE, 'r')
	telegram_url = telegram_file.read()
	r1 = requests.get('https://' + telegram_url + '/getUpdates?offset=' + str(next_updateID) + '&timeout=' + str(getUpdate_TIMEOUT))
	telegram_file.close()
	json_data = json.loads(r1.text)
        return json_data

def get_previous_update_ID():
        updateID_file = open(UPDATEID_FILE, 'r')
        update_ID = int(updateID_file.read())
        updateID_file.close()
	return update_ID

def put_previous_update_ID(update_ID):
        updateID_file = open(UPDATEID_FILE, 'w')
        updateID_file.write(str(update_ID))
        updateID_file.close()
	return 1

def closeGarageDoor(GarageDoor):

	#set up the GPIO pins
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(DOOR_1_RELAY, GPIO.OUT)
	GPIO.setup(DOOR_2_RELAY, GPIO.OUT)

	if GarageDoor == 1:
		DoorRelay = DOOR_1_RELAY
	elif GarageDoor == 2:
		DoorRelay = DOOR_2_RELAY
	else:
		write_message_to_log('Error: Incorrect Garage Door Number: ' + str(GarageDoor))
		return

	#activate relay for two seconds and turn off
	GPIO.output(DoorRelay, GPIO.LOW)
	write_message_to_log('Turned On: ' + str(GarageDoor))
	time.sleep(2)
	GPIO.output(DoorRelay, GPIO.HIGH)
	write_message_to_log('Turned Off: ' + str(GarageDoor))

def sendImage():
	telegram_file = open(TELEGRAM_URL_FILE, 'r')
	telegram_url = telegram_file.read()
	url ="https://" + telegram_url + "/sendPhoto"
	data = {"chat_id":"765138485"}
	files = {'photo': open(PHOTO_FILE, 'rb')}
	r= requests.post(url, files=files, data=data)
	message = "GDM Photo: " + str(time.asctime(time.localtime(time.time())))
	message = 'https://' + telegram_url + '/sendMessage?chat_id=765138485&reply_markup={"keyboard": [["Close Garage Door 1"],["Close Garage Door 2"], ["Get Photo"], ["Get Video"], ["Ignore"]],"one_time_keyboard": true}&parse_mode=Markdown&text=' + message
	r=requests.post(message)
	write_message_to_log('Image Sent: ' + str(r.status_code) + str(r.reason) + str(r.content))
	telegram_file.close()
	return

def sendVideo():
	telegram_file = open(TELEGRAM_URL_FILE, 'r')
	telegram_url = telegram_file.read()
	url ="https://" + telegram_url + "/sendVideo"
	data = {"chat_id":"765138485", "height":"480", "width":"320"}
	videoFile = open(CONVERTED_VIDEO_FILE, 'rb')
	files = {'video': videoFile}
	r= requests.post(url, files=files, data=data)
	message = "GDM Video: " + str(time.asctime(time.localtime(time.time())))
	message = 'https://' + telegram_url + '/sendMessage?chat_id=765138485&reply_markup={"keyboard": [["Close Garage Door 1"],["Close Garage Door 2"], ["Get Photo"], ["Get Video"], ["Ignore"]],"one_time_keyboard": true}&parse_mode=Markdown&text=' + message
	r=requests.post(message)
	write_message_to_log('Video Sent: ' + str(r.status_code) + str(r.reason) + str(r.content))
	telegram_file.close()
	videoFile.close()
	videoFilename = 'rm ' + CONVERTED_VIDEO_FILE
        os.system(videoFilename)
	return


def getPicture(piCamera):
	time.sleep(2)
	piCamera.capture(PHOTO_FILE)
	return

def getVideo(piCamera, recordingtime):
	piCamera.start_recording(VIDEO_FILE)	
	time.sleep(recordingtime)
	piCamera.stop_recording()
	convertToMP4 = 'MP4Box -add ' + VIDEO_FILE + ' ' + CONVERTED_VIDEO_FILE
        os.system(convertToMP4)
	videoFilename = 'rm ' + VIDEO_FILE
        os.system(videoFilename)
        return

#
#Code starts here
#

#read previous_updateID from file and add 1
previous_updateID = get_previous_update_ID()
messageText = ''

camera=PiCamera()

#The main loop
while True:
	previous_updateID += 1
	result = get_telegram_message(previous_updateID)
	for message in result['result']:
		previous_updateID = message['update_id']
		messageText = message['message']['text']

	#write update ID to file
	put_previous_update_ID(previous_updateID)


	if messageText == 'Close Garage Door 1':
		write_message_to_log('Message Received: ' + messageText)
		closeGarageDoor(GARAGE_DOOR_1)	
	elif messageText == 'Close Garage Door 2':
		write_message_to_log('Message Received: ' + messageText)
		closeGarageDoor(GARAGE_DOOR_2)
	elif messageText == 'Get Photo':
		write_message_to_log('Message Received: ' + messageText)
		getPicture(camera)
		sendImage()
	elif messageText == 'Get Video':
		write_message_to_log('Message Received: ' + messageText)
		getVideo(camera,VIDEO_RECORDING_TIME)
		sendVideo()	
	elif messageText == 'Ignore' :
		write_message_to_log('Message Received: ' + messageText)
	messageText = ''	
				
