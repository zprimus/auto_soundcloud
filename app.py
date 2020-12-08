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

try:
	local.record()
except ValueError:
	print('ERROR: Recording failed. Check audio input device.')
