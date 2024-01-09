import os

from error import MonitoringRecordNotInitialized, FileDoesNotExistsException
from monitoring_recording import MonitoringRecording

if __name__ == '__main__':
    print("Command detele_uploaded_files_command.py started")
    print("Retrieving sent monitoring recordings from database")

    monitoring_recordings = MonitoringRecording.get_sent()
    print("Found " + str(len(monitoring_recordings)) + " monitoring recordings to delete")

    for monitoring_recording in monitoring_recordings:
        print("Deleting already uploaded monitoring recording {}".format(monitoring_recording.name))

        try:
            filepath = os.path.join('monitoring_recording_files', monitoring_recording.name)

            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                raise FileDoesNotExistsException()

            monitoring_recording.delete()
            print("Monitoring recording {} successfully deleted".format(monitoring_recording.name))
        except MonitoringRecordNotInitialized as e:
            print(e)
        except FileDoesNotExistsException as e:
            print(e)
