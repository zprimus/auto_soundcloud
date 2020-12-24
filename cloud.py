import requests
from requests.exceptions import HTTPError

import pickle
import os
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

def upload_files(account):
	# see if folder already exists on google drive
	results = account.files().list(pageSize=5, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	
	for item in items:
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
	
	print('Folder ID: ', folder_id)
	
	local_filename = '2020-12-13_18-2-30'
	local_foldername = 'raw'
	file_metadata = {
		'name': local_filename,
		'parents': [folder_id],
		'path': local_foldername + '/' + local_filename
	}
	
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
			try:
				size = get_size_format(int(item["size"]))
			except:
				size = "N/A"
			
			mime_type = item["mimeType"]
			
			modified_time = item["modifiedTime"]
			
			rows.append((id, name, parents, size, mime_type, modified_time))
		print("Files:")
		
		table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
		print(table)
	return

# main function
def main():
	service = get_gdrive_service()
	
	results = service.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
	items = results.get('files', [])
	list_files(items)
	
	upload_files(service)
	
	results = service.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
	items = results.get('files', [])
	list_files(items)
	
	return

##### Main Code #####
try:
	main()
except Exception as e:
	print('Error: ', e)
