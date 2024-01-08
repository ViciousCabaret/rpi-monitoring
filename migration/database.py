import os
import sqlite3
from contextlib import closing

BASE_DIR = os.path.dirname(__file__)


class Database:
    DATABASE_DEFAULT_NAME = "database.db"

    connection: sqlite3.Connection = None
    filename: str = DATABASE_DEFAULT_NAME

    def __init__(self, filename=DATABASE_DEFAULT_NAME):
        if filename is not None:
            self.filename = filename
        self.create_database()

    def get_database_default_path(self) -> str:
        return os.path.join(BASE_DIR, self.filename)

    def create_database(self):
        if os.path.isfile(self.get_database_default_path()) is False:
            print("Creating sqlite database")
            file = open(self.get_database_default_path(), 'w')
            file.close()
            print("Created sqlite database at path:", self.get_database_default_path())
        else:
            print("Database already exists at path:", self.get_database_default_path())

    def fetchone(self, query):
        with closing(sqlite3.connect(self.get_database_default_path())) as connection:
            with closing(connection.cursor()) as cursor:
                return cursor.execute(query).fetchone()

    def fetchall(self, query):
        with closing(sqlite3.connect(self.get_database_default_path())) as connection:
            with closing(connection.cursor()) as cursor:
                return cursor.execute(query).fetchall()

    def execute(self, query):
        with closing(sqlite3.connect(self.get_database_default_path())) as connection:
            with closing(connection.cursor()) as cursor:
                return cursor.execute(query)

    def is_database_empty(self):
        return self.fetchone("SELECT name FROM sqlite_master") is None
