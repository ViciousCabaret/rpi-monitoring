from error import GoogleDriveFileUploadException
from google_client import GoogleDriveClient
from monitoring_recording import MonitoringRecording
from dotenv import load_dotenv

load_dotenv()

import logging
import os

BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'log', 'upload_files_to_google_drive_command.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)
if __name__ == '__main__':
    logging.info("Command upload_files_to_google_drive_command.py started")
    logging.info("Retrieving not sent monitoring recordings from database")

    monitoring_recordings = MonitoringRecording.get_not_sent()
    google_drive_client = GoogleDriveClient(os.getenv("GOOGLE_DRIVE_FOLDER_ID"))

    logging.info("Found " + str(len(monitoring_recordings)) + " monitoring recordings to upload")
    for monitoring_recording in monitoring_recordings:
        try:
            logging.info("Uploading monitoring recording {} into google drive".format(monitoring_recording.name))
            filepath = os.path.join('monitoring_recording_files', monitoring_recording.name)
            google_drive_client.upload_h264_file(filepath)
            monitoring_recording.mark_as_sent()
            logging.info("Successfully uploaded monitoring recording {}".format(filepath))

        except GoogleDriveFileUploadException as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)
