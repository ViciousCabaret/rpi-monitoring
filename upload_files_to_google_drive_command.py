import os

from error import GoogleDriveFileUploadException
from google_client import GoogleDriveClient
from monitoring_recording import MonitoringRecording

BASE_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    print("Command upload_files_to_google_drive_command.py started")
    print("Retrieving not sent monitoring recordings from database")
    monitoring_recordings = MonitoringRecording.get_not_sent()
    google_drive_client = GoogleDriveClient()

    print("Found " + str(len(monitoring_recordings)) + " monitoring recordings to upload")
    for monitoring_recording in monitoring_recordings:
        try:
            print("Uploading monitoring recording {} into google drive".format(monitoring_recording.name))
            filepath = os.path.join('monitoring_recording_files', monitoring_recording.name)
            google_drive_client.upload_h264_file(filepath)
            monitoring_recording.mark_as_sent()

        except GoogleDriveFileUploadException as e:
            print(e)

        print("Successfully uploaded monitoring recording {}".format(filepath))
