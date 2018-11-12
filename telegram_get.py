import time
import requests
#
#This module monitors the telegram bot and processes responses from the keyboard sent to the user
#
#Constants defined here
#
#LOG_FILENAME = '/home/pi/gdm/ds.log'
TELEGRAM_URL_FILE = '/home/pi/gdm/telegram_url.txt'
UPDATEID_FILE = '/home/pi/gdm/previous_updateID.txt'
getUpdate_TIMEOUT = 5          #long polling timeout
GARAGE_DOOR_1 = 1
GARAGE_DOOR_2 = 2

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
def get_telegram_message(next_updateID):
	telegram_file = open(TELEGRAM_URL_FILE, 'r')
	telegram_url = telegram_file.read()
	r1 = requests.get('https://' + telegram_url + '/getUpdates?offset=' + str(next_updateID) + '&timeout=' + str(getUpdate_TIMEOUT))
	return r1.json()

def get_previous_update_ID():
        updateID_file = open(UPDATEID_FILE, 'r')
        update_ID = int(updateID_file.read())
        updateID_file.close()
	return update_ID

def put_previous_update_ID(update_ID):
        updateID_file = open(UPDATEID_FILE, 'w')
	#print ("writing: " + str(update_ID))
        updateID_file.write(str(update_ID))
        updateID_file.close()
	return 1
               
#
#Code starts here
#

#read previous_updateID from file and add 1
previous_updateID = get_previous_update_ID()

#The main loop
while True:


	result = get_telegram_message(previous_updateID + 1)
	for message in result['result']:
		previous_updateID = message['update_id']
		messageText = message['message']['text']
		#print messageText

	#print previous_updateID
	#write update ID to file
	put_previous_update_ID(previous_updateID)


	if messageText != 'Ignore':
		if messageText == 'Close Garage Door 1':
			print messageText	
		elif messageText == 'Close Garage Door 2':
			print messageText
		elif messageText == 'Get Photo':
			print messageText	
		else:
			print messageText
		
				
