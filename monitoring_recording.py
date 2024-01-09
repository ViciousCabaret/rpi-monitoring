from sqlite3 import IntegrityError
from typing import Optional
from error import SaveMonitoringRecordIntoDatabase, MonitoringRecordNotInitialized
from database import Database


class MonitoringRecording:
    id: Optional[int] = None
    name: str = None
    is_sent: bool = None
    timestamp: Optional[int] = None

    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name = name
        self.is_sent = kwargs.get('is_sent', False)
        self.id = kwargs.get('id', None)
        self.timestamp = kwargs.get('timestamp', None)

    def save(self):
        database = Database()
        if self.name is None or self.is_sent is None:
            raise SaveMonitoringRecordIntoDatabase("Some of properties are missing")
        try:
            database.execute(
                f'INSERT INTO monitoring_recordings (name, is_sent) VALUES ("{self.name}", {self.is_sent})')
        except IntegrityError as e:
            raise SaveMonitoringRecordIntoDatabase("Monitoring recording with this name already exists")

    @staticmethod
    def get(id: int):
        database = Database()
        data = database.fetchone(f'SELECT * FROM monitoring_recordings WHERE id = {id}')

        if data is None:
            return data

        return MonitoringRecording(
            data[1],
            is_sent=bool(data[2]),
            id=data[0],
            timestamp=data[3]
        )

    @staticmethod
    def get_not_sent():
        database = Database()
        data = database.fetchall(f'SELECT * FROM monitoring_recordings WHERE is_sent = FALSE')

        results = []
        for datum in data:
            results.append(MonitoringRecording(
                datum[1],
                is_sent=bool(datum[2]),
                id=datum[0],
                timestamp=datum[3]
            ))

        return results

    def mark_as_sent(self):
        if self.id is None:
            raise MonitoringRecordNotInitialized()

        database = Database()
        database.execute("UPDATE monitoring_recordings SET is_sent = TRUE WHERE id = {}".format(self.id))