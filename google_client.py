import os
import os.path

from error import GoogleDriveFileUploadException

BASE_DIR = os.path.dirname(__file__)

import sys
from apiclient import discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class GoogleDriveClient:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_KEY_FILE = 'credentials.json'
    service = None
    google_dir_id = None

    def __init__(self, google_dir_id):
        self.google_dir_id = google_dir_id

    def get_credentials(self):
        credential = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(BASE_DIR, self.SERVICE_ACCOUNT_KEY_FILE), self.SCOPES)

        if not credential or credential.invalid:
            print('Unable to authenticate using service account key.')
            sys.exit()

        return credential

    def get_service(self):
        if self.service is None:
            http_auth = self.get_credentials().authorize(httplib2.Http())
            self.service = discovery.build('drive', 'v3', http=http_auth)

        return self.service

    def upload_h264_file(self, filepath):
        try:
            media = MediaFileUpload(filepath, mimetype="video/h264", resumable=True)
            head, tail = os.path.split(filepath)
            file = (
                self.get_service().files().create(
                    body={"name": tail, "parents": [self.google_dir_id]},
                    media_body=media
                ).execute()
            )

            print(f'Uploaded file ID: {file.get("id")}')

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise GoogleDriveFileUploadException(error)
