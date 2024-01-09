class SaveDataIntoDatabaseException(Exception):
    pass


class SaveMonitoringRecordIntoDatabase(SaveDataIntoDatabaseException):
    pass


class MonitoringRecordNotInitialized(Exception):
    def __init__(self, msg='Monitoring record not initialized', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class GoogleDriveFileUploadException(Exception):
    pass
