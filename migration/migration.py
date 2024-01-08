import os

from migration.database import Database

BASE_DIR = os.path.dirname(__file__)


class Migrator:
    database: Database = None

    def __init__(self, database: Database) -> None:
        self.database = database

    def migrate(self):
        if self.database.is_database_empty():
            print("Executing base migration")
            self.database.execute(open(os.path.join(BASE_DIR, 'base.sql'), "r").read())
            print("Base migration successfully migrated")
