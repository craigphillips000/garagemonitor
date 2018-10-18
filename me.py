import time
import requests
#
#This module monitors ds.log and sends any new messages to Telegram
#
#Constants defined here
#
LOG_FILENAME = '/home/pi/gdm/ds.log'
MESSAGE_TIMER = 2		#don't process times older than x minutes

#variables defined here
#
#
previous_message_count = 0
new_message_count      = 0
message_time	= 0.0
current_message = '' 

#
#
#
#Function definitions start here
#
def send_telegram_message(message):

#	r1 = requests.get('https://api.telegram.org/bot199012095:AAGD0Mu1pV4GRAyBSN_nwXLEqyop1bXPVz0/getUpdates?offset=1')
	message = 'https://api.telegram.org/bot199012095:AAGD0Mu1pV4GRAyBSN_nwXLEqyop1bXPVz0/sendMessage?chat_id=125811912&reply_markup={"keyboard": [["Close Garage Door"], ["Get Photo"], ["Get Video"], ["Ignore"]],"one_time_keyboard": true}&parse_mode=Markdown&text=' + message
	r2 = requests.post(message)
	return r2.json()

def write_message_to_log(message):
        logfile = open(LOG_FILENAME, 'a')
        logfile.write(str(time.time()) + ' ')
        logfile.write(time.asctime(time.localtime(time.time())) + ': ')
        logfile.write(message + '\n')
        logfile.close()
	return 1
        
#
#Code starts here
#


#The main loop
while True:

	#read the log into an array of strings
	logfile = open(LOG_FILENAME, 'r')
        messages = [record.rstrip('\n') for record in logfile]
	logfile.close()

	#Are there any new messages, if so process them
	new_message_count = len(messages) - previous_message_count
	while new_message_count > 0:
		current_message = messages[len(messages) - new_message_count].split()
		if float(current_message[0]) > time.time() - MESSAGE_TIMER * 60:
			print messages[len(messages) - new_message_count]
			user_response = send_telegram_message(messages[len(messages) - new_message_count])
#			print user_response	
		new_message_count -= 1
		
	previous_message_count = len(messages)		

