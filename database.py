import os
from os import PathLike
from typing import List, NamedTuple

from pandas.io.parsers.readers import sys
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class DatabaseUser(NamedTuple):
	"""data type of users table in the database"""

	first_name: str
	last_name: str
	email: str
	role: str
	created_at: str


class Database(QObject):
	"""handle all database activities"""

	def __init__(self, database_name: str = "model-analysis.sqlite") -> None:
		self.database_name = database_name
		self.connection = QSqlDatabase.addDatabase("QSQLITE")
		self.connection.setDatabaseName(self.database_name)

		# signals
		self.new_user_created_signal = pyqtSignal(dict)
		self.db_error_signal = pyqtSignal(str)

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
		return self.execute_sql_file(os.path.join(os.getcwd(), "db_script.sql"))

	def create_new_user(self, first_name: str, last_name: str, email: str, role: str):
		"""Add a new user to the database"""
		query = QSqlQuery(self.connection)
		query.prepare("""
            INSERT INTO users(first_name, last_name, email, role)
            VALUES (?, ?, ?, ?)
        """)
		query.addBindValue(first_name)
		query.addBindValue(last_name)
		query.addBindValue(email)
		query.addBindValue(role)

		if query.exec():
			# #  emit a signal with the user data after insertion. emit another signal to a toast system.
			# self.new_user_created_signal.emit(  # type: ignore
			#     {
			#         "first_name": first_name,
			#         "last_name": last_name,
			#         "email": email,
			#         "role": role,
			#     }
			# )
			return True
		else:
			# emit a database error signal to the toast system.
			# self.db_error_signal.emit(query.lastError().text())  # type: ignore
			return False

	def get_all_users(self) -> List[DatabaseUser]:
		"""fetch all users from the database"""
		query = QSqlQuery(self.connection)
		querystr = "SELECT first_name, last_name, email, role, created_at FROM users;"

		if not query.exec(querystr):
			print(f"Error fetching all users: {query.lastError().databaseText()}")
			return []

		users: List[DatabaseUser] = []
		while query.next():
			user = DatabaseUser(
				first_name=query.value(0),
				last_name=query.value(1),
				email=query.value(2),
				role=query.value(3),
				created_at=query.value(4),
			)

			users.append(user)
		return users

	def get_all_financial_analysts(self) -> List[str]:
		"""Fetch only the full names of financial analysts in the database"""
		query = QSqlQuery(self.connection)
		statement = "SELECT first_name, last_name FROM users WHERE role = 'financial analyst'"

		analysts: List[str] = []

		if not query.exec(statement):
			print(f"Error fetching financial analysts from the database: {query.lastError().text()}")
			return []

		while query.next():
			analyst = f"{query.value(0)} {query.value(1)}"
			analysts.append(analyst)

		return analysts
