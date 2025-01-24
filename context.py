from database import Database


class AppContext:
    def __init__(self, database: Database) -> None:
        self._database = database

    @property
    def database(self):
        return self._database
