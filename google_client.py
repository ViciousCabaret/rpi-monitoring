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

# A single auth scope is used for the zero-touch enrollment customer API.
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_KEY_FILE = 'credentials.json'


class GoogleDriveClient:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_KEY_FILE = 'credentials.json'
    GOOGLE_DIR_ID = "179zvkP60csuLPrLMsZH_x7g3MI4kzVlQ"
    service = None

    def get_credentials(self):
        credential = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(BASE_DIR, SERVICE_ACCOUNT_KEY_FILE), SCOPES)

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
                    body={"name": tail, "parents": ["179zvkP60csuLPrLMsZH_x7g3MI4kzVlQ"]},
                    media_body=media
                ).execute())

            print(f'Uploaded file ID: {file.get("id")}')

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise GoogleDriveFileUploadException(error)