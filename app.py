##########################################################################
# Title: auto_soundcloud                                                 #
#                                                                        #
# Creator: zprimus                                                       #
#                                                                        #
# Description: Record live music and upload to SoundCloud automatically. #
#                                                                        #
# Requirements: Microphone, Internet access                              #
##########################################################################

import local
import cloud

while(True):
	try:
		local.listen()
	except ValueError:
		print('ERROR: Listening failed. Check audio input device.')
	
	try:
		local.record()
	except ValueError:
		print('ERROR: Recording failed. Check audio input device.')

