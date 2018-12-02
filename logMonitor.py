import time
import requests
#
#This module monitors the ds.log file and sends any messages posted to telegram
#
#Constants defined here
#
LOG_FILENAME = '/home/pi/gdm/ds.log'
LOG__MONITOR_FILENAME = '/home/pi/gdm/logMonitor.log'
TELEGRAM_URL_FILE = '/home/pi/gdm/telegram_url.txt'
MESSAGE_TIMER = 2		#don't process times older than x minutes
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
def write_message_to_log(message):
        logfile = open(LOG__MONITOR_FILENAME, 'a')
        logfile.write(str(time.asctime(time.localtime(time.time()))) + ': ' + str(message) + '\n')
        logfile.close()
	return 1
        
def send_telegram_message(message, garage_door):
	telegram_file = open(TELEGRAM_URL_FILE, 'r')
	telegram_url = telegram_file.read()
	if garage_door == GARAGE_DOOR_1:
		write_message_to_log ("GD1 write to: " + telegram_url)
		message = 'https://' + telegram_url + '/sendMessage?chat_id=765138485&reply_markup={"keyboard": [["Close Garage Door 1"], ["Close Garage Door 2"],["Get Photo"], ["Get Video"], ["Ignore"]],"one_time_keyboard": true}&parse_mode=Markdown&text=' + message
		
	elif garage_door == GARAGE_DOOR_2:
		write_message_to_log ("GD2 write to: " + telegram_url)
		message = 'https://' + telegram_url + '/sendMessage?chat_id=765138485&reply_markup={"keyboard": [["Close Garage Door 1"],["Close Garage Door 2"], ["Get Photo"], ["Get Video"], ["Ignore"]],"one_time_keyboard": true}&parse_mode=Markdown&text=' + message
	r2 = requests.post(message)
	return r2.json()


#Code starts here
#


#The main loop
while True:

	#delay a little bit
	time.sleep(10)
	
	#read the log into an array of strings
	logfile = open(LOG_FILENAME, 'r')
        messages = [record.rstrip('\n') for record in logfile]
	logfile.close()

	#Are there any new messages, if so process them
	new_message_count = len(messages) - previous_message_count
	while new_message_count > 0:
		current_message = messages[len(messages) - new_message_count].split()
		if float(current_message[0]) > time.time() - MESSAGE_TIMER * 60:
#			print messages[len(messages) - new_message_count]
			if int(current_message[1]) == GARAGE_DOOR_1:
				user_response = send_telegram_message(messages[len(messages) - new_message_count],GARAGE_DOOR_1)
			elif int(current_message[1]) == GARAGE_DOOR_2:	
				user_response = send_telegram_message(messages[len(messages) - new_message_count],GARAGE_DOOR_2)
		new_message_count -= 1
		
	previous_message_count = len(messages)		
