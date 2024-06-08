import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service-account.json'  # Service file present in the root directory of the project
PARENT_FOLDER_ID = "15NeqZ-007biTeo_GxsYc_97i77nW0D6L"  # Id of the folder under which videos will be uploaded


class Uploader:
    def __init__(self, file_with_path, job_id, to="GDrive"):
        self.job_id = job_id
        self.to = to
        self.file_with_path = file_with_path

    def __authenticate(self):
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return creds

    def upload(self):
        print("Starting to upload the video file to " + self.to + "..........................")
        creds = self.__authenticate()
        service = build('drive', 'v3', credentials=creds)
        file_name = self.job_id + "-" + self.file_with_path.split("/")[-1]
        file_metadata = {
            'name': file_name,
            'parents': [PARENT_FOLDER_ID]
        }

        file = service.files().create(
            body=file_metadata,
            media_body=self.file_with_path
        ).execute()
        print("File uploaded...............\n\n")
