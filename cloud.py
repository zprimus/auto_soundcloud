import requests
from requests.exceptions import HTTPError

import pickle
import os
from time import sleep
from os import listdir
from os.path import isfile, join
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']

FOLDER_METADATA = {
	'name': 'raw',
	'mimeType': 'application/vnd.google-apps.folder'
}

def get_local_files():
	fileList = [f for f in listdir(FOLDER_METADATA['name']) if isfile(join(FOLDER_METADATA['name'], f))]
	
	return fileList
	
def get_cloud_files(account):
	results = account.files().list(pageSize=5, fields="nextPageToken, files(id, name, parents)").execute()
	fileList = results.get('files', [])
	
	return fileList

def upload_files(account):
	# get lists of all files
	local_file_list = get_local_files()
	
	cloud_file_list = get_cloud_files(account)
	
	# see if folder already exists on google drive
	for item in cloud_file_list:
		id = item["id"]
		name = item["name"]
		
		folderExists = False
		
		if(name == FOLDER_METADATA['name']):
			folderExists = True
			break
	
	if(folderExists):
		folder_id = id
	else:
		file = account.files().create(body=FOLDER_METADATA, fields='id').execute()
	
		folder_id = file.get('id')	
	
	# minimize cloud list to the files in the path we care about
	new_cloud_list = []
	for item in cloud_file_list:
		if(item['parents'] == [folder_id]):
			new_cloud_list.append(item)
	
	# display existing files in the cloud directory
	list_files(new_cloud_list)
	
	# compare local files to cloud files and upload
	for local_item_name in local_file_list:
		fileExists = False
		
		for cloud_item in new_cloud_list:
			if(local_item_name == cloud_item['name']):
				fileExists = True
							
		file_metadata = {
			'name': local_item_name,
			'parents': [folder_id],
			'path': FOLDER_METADATA['name'] + '/' + local_item_name
		}
		
		# upload local file to cloud
		if(not fileExists):
			media = MediaFileUpload(file_metadata['path'], resumable=True)
			file = account.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
			print('File created.')
			print('File ID: ', file.get('id'))
			print('File Name: ', file.get('name'))

	return

# authenticate google account
def get_gdrive_service():
	creds = None
	
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			print('Authenticating account using token.pickle')
			creds = pickle.load(token)
			
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			print('Refreshing authentication token')
			creds.refresh(Request())
		else:
			print('Authenticating account using credentials.json')
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			print('Redirecting to google for manual authentication')
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			print('Creating token.pickle')
			pickle.dump(creds, token)
	print('Building driver')
	return build('drive', 'v3', credentials=creds)

# list items in google drive
def list_files(items):
	if not items:
		print('No files found.')
	else:
		print('Files found.')
		rows = []
		for item in items:
			id = item["id"]
			name = item["name"]
			try:
				parents = item["parents"]
			except:
				parents = "N/A"
			
			rows.append((id, name, parents))
		print("Files:")
		
		table = tabulate(rows, headers=["ID", "Name", "Parents"])
		print(table)
	return

# main function
def main():
	service = get_gdrive_service()
	
	upload_files(service)
	
	return

##### Main Code #####
while(True):
	try:
		main()
	except Exception as e:
		print('Error: ', e)
		
	# run every 5 min
	sleep(300)
