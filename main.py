from migration.database import Database
from migration.migration import Migrator
from model.monitoring_recording import MonitoringRecording

if __name__ == '__main__':
    # database = Database()
    # migration = Migrator(database).migrate()

    # print("test saving data:")

    monitoring_recording = MonitoringRecording("testtest222223", is_sent=True)
    monitoring_recording.save()
    #
    monitoring_recordings = MonitoringRecording.get_not_sent()

    for monitoring_recording in monitoring_recordings:
        print(monitoring_recording.id)
        print(monitoring_recording.name)
        print(monitoring_recording.is_sent)
