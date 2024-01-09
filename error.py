class SaveDataIntoDatabaseException(Exception):
    pass


class SaveMonitoringRecordIntoDatabase(SaveDataIntoDatabaseException):
    pass


class MonitoringRecordNotInitialized(Exception):
    def __init__(self, msg='Monitoring record not initialized', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class GoogleDriveFileUploadException(Exception):
    pass


class FileDoesNotExistsException(Exception):
    def __init__(self, msg='File does not exist', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
