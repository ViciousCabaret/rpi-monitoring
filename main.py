import os

from monitoring_recording import MonitoringRecording

BASE_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    print("test main function")
    # google drive file upload: DONE
    # google_drive_client = GoogleDriveClient()
    # google_drive_client.upload_h264_file(os.path.join(BASE_DIR, 'google_upload', '1.h264'))

    # database = Database()
    # migration = Migrator(database).migrate()

    print("test saving data:")

    monitoring_recording = MonitoringRecording("testtest222223", is_sent=False)
    monitoring_recording.save()
    #
    monitoring_recordings = MonitoringRecording.get_not_sent()
    #
    # for monitoring_recording in monitoring_recordings:
    #     print(monitoring_recording.id)
    #     print(monitoring_recording.name)
    #     print(monitoring_recording.is_sent)
