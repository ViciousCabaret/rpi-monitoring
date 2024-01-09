from error import MonitoringRecordNotInitialized, FileDoesNotExistsException
from monitoring_recording import MonitoringRecording

import os
import logging

logging.basicConfig(
    filename=os.path.join('log', 'delete_uploaded_files_command.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)

if __name__ == '__main__':
    logging.info("Command delete_uploaded_files_command.py started")
    logging.info("Retrieving sent monitoring recordings from database")

    monitoring_recordings = MonitoringRecording.get_sent()
    logging.info("Found " + str(len(monitoring_recordings)) + " monitoring recordings to delete")

    for monitoring_recording in monitoring_recordings:
        logging.info("Deleting already uploaded monitoring recording {}".format(monitoring_recording.name))

        try:
            filepath = os.path.join('monitoring_recording_files', monitoring_recording.name)

            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                raise FileDoesNotExistsException()

            monitoring_recording.delete()
            logging.info("Monitoring recording {} successfully deleted".format(monitoring_recording.name))
        except MonitoringRecordNotInitialized as e:
            logging.error(e)
        except FileDoesNotExistsException as e:
            logging.error(e)
