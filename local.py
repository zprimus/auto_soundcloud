# record audio

def trigger():

	return

def record():
	import pyaudio
	import wave

	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 3
	filePath = 'raw/' + title_format()

	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Recording')

	stream = p.open(format=sample_format,
		        channels=channels,
		        rate=fs,
		        frames_per_buffer=chunk,
		        input=True)

	frames = []  # Initialize array to store frames

	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * seconds)):
	    data = stream.read(chunk)
	    frames.append(data)

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
	import datetime
	
	currentTime = datetime.datetime.now()
	titleString = str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day) + '_' + str(currentTime.hour) + '-' + str(currentTime.minute) + '-' + str(currentTime.second)
	
	#return titleString
	return 'example'
