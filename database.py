import os
from os import PathLike

from pandas.io.parsers.readers import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class Database:
    """handle all database activities"""

    def __init__(self, database_name: str = "model-analysis.sqlite") -> None:
        self.database_name = database_name
        self.connection = QSqlDatabase.addDatabase("QSQLITE")
        self.connection.setDatabaseName(self.database_name)

        if not self.connection.open():
            print(f"Error: Could not connect to the database. \n Error: {self.connection.lastError().text()}")

            sys.exit(1)


    def execute_sql_file(self, file_path: str | PathLike) -> bool:
        """Execute the sql file that creates all tables"""
        try:
            with open(file_path, "r") as file:
                sql_script = file.read()
            query = QSqlQuery(self.connection)
            if not query.exec(sql_script):
                print(f"Error executing sql script '{file_path}'")
                return False
            return True
        except Exception as e:
            print(f"An unexpected error occured when creating db tables: {str(e)}")
            return False


    def create_all_tables(self) -> bool:
        """create the database table for users."""
        return self.execute_sql_file(os.path.join(os.getcwd(), 'db_script.sql'))
