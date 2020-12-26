##########################################################################
# Project: auto_soundcloud                                               #
#                                                                        #
# File name: local.py                                                    #
#                                                                        #
# Creator: zprimus                                                       #
#                                                                        #
# Creation date: 12/25/2020                                              #
#                                                                        #
# Description: Record live music and save it locally.                    #
#                                                                        #
# Requirements: Microphone                                               #
##########################################################################

# dependencies
import pyaudio
import wave
import time
import numpy
import datetime

# global variables
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
thresholdAmplitude = 10000
thresholdTime = 5

def listen():
	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Listening')

	stream = p.open(format=sample_format,
		        channels=channels,
		        rate=fs,
		        frames_per_buffer=chunk,
		        input=True)
	
	# initialize peak variable        
	peak = 0

	# Continuously listen
	while(peak < thresholdAmplitude):
	    data = stream.read(chunk)
	    
	    dataDecoded = numpy.frombuffer(data, dtype=numpy.int16)
	    peak = numpy.average(numpy.abs(dataDecoded))*2
	    bars = "|" * int(peak / 1000)
	    
	    #print(bars)
	
	return

def record():
	filePath = 'raw/' + title_format()

	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Recording')

	stream = p.open(format=sample_format,
		        channels=channels,
		        rate=fs,
		        frames_per_buffer=chunk,
		        input=True)
		        
	# init array to store frames
	frames = []
	
	# init timer variable
	t1 = time.time()

	# Store data in chunks when audio level is higher than threshold
	while(True):
		data = stream.read(chunk)
		frames.append(data)
		dataDecoded = numpy.frombuffer(data, dtype=numpy.int16)
		peak = numpy.average(numpy.abs(dataDecoded))*2
		
		if(peak < thresholdAmplitude):
			t = time.time()
			timer_seconds = t - t1
			
			if(timer_seconds > thresholdTime):
				break
		else:
			t1 = time.time()

	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()

	print('Finished recording')

	# Save the recorded data as a WAV file
	wf = wave.open(filePath, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()
	
	return
	
def title_format():
	currentTime = datetime.datetime.now()
	titleString = str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day) + '_' + str(currentTime.hour) + '-' + str(currentTime.minute) + '-' + str(currentTime.second)
	
	return titleString

##### Main Code ######
while(True):
	try:
		listen()
	except Exception as e:
		print('ERROR: ', e)
	
	try:
		record()
	except Exception as e:
		print('ERROR: ', e)
