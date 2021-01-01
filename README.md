# auto_soundcloud
Automatically upload realtime audio to SoundCloud.

## install PyAudio
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg
sudo pip install pyaudio

## install NumPy
sudo pip install numpy

## set up google api
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib tabulate requests tqdm

sudo pip install --upgrade google-api-python-client google-auth-oauthlib tabulate

Enable Google Drive API (create api key and o-auth key)
Download o-auth configuration and save in project directory as 'credentials.json'
