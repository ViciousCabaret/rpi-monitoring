from migration.database import Database
from migration.migration import Migrator

if __name__ == '__main__':
    database = Database()
    migration = Migrator(database).migrate()
