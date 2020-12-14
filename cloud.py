import requests
from requests.exceptions import HTTPError

import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_names_of_files():
	for url in ['https://api.github.com', 'https://www.googleapis.com/drive/v3/files']:
		try:
			response = requests.get(url)	
			
			response.raise_for_status()
		except HTTPError as http_err:
			print(f'HTTP error occurred -> {http_err}')
		except Exception as err:
			print(f'Other error occurred -> {err}')
		else:
			print('Success!')
			
	return

def upload_files():

	return
	
def get_gdrive_service():
	creds = None
	
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
			
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return build('drive', 'v3', credentials=creds)
		
def main():
	service = get_gdrive_service()
	
	results = service.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
	
	items = results.get('files', [])
	
	list_files(items)
	#print(items)
	
	return
	
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

##### Main Code #####
#get_names_of_files()
try:
	main()
except:
	print('error')
