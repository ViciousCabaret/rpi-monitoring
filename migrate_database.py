from database import Database
from migration import Migrator

if __name__ == "__main__":
    database = Database()
    migration = Migrator(database).migrate()