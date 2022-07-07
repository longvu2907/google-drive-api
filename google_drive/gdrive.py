import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaInMemoryUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    creds = None
    if os.path.exists('google_drive/token.pickle'):
        with open('google_drive/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_drive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('google_drive/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def get_files_list():
    service = get_gdrive_service()

    files = service.files().list(
        pageSize=1000,
        q="mimeType contains 'image/'",
        fields="files(id, name, parents, createdTime, trashed)"
    ).execute()['files']

    res = service.files().list(
        q="mimeType = 'application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()['files']

    folders = {}
    for folder in res:
        folders[folder['id']] = folder['name']

    for file in files:
        folder_id = file['parents'][0]
        file['category'] = folders[folder_id]
        file['category_id'] = folder_id
        file['image_url'] = f"https://drive.google.com/uc?id={file['id']}"
        file['created_at'] = file['createdTime']

    return files


def upload_files(name, file_data, folder='album'):
    service = get_gdrive_service()

    #get upload folder
    folder_id = service.files().list(
        q=f"name = '{folder}' and mimeType = 'application/vnd.google-apps.folder'", 
        fields="files(id)"
    ).execute()['files'][0]['id']

    file_metadata = {
        "name": name,
        "parents": [folder_id]
    }

    #upload
    media = MediaInMemoryUpload(file_data)
    file = service.files().create(
        body=file_metadata, 
        media_body=media, 
        fields='id, createdTime'
    ).execute()

    #set permission
    permissions_body = {
        "role": "reader",
        "type": "anyone"
    }
    service.permissions().create(
        fileId=file.get('id'), 
        body=permissions_body
    ).execute()

    return (file.get("id"), folder_id, file.get("createdTime"))
