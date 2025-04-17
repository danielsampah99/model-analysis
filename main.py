import sys

from PyQt6.QtWidgets import QApplication

from database import Database
from ui.main_window import MainWindow

if __name__ == "__main__":
	app = QApplication(sys.argv)

	db = Database()
	if db.create_all_tables():
		print("All tables were successfully created")
		main_window = MainWindow()
		main_window.show()
	else:
		print("Error creating tables. Exiting...")
		sys.exit(1)

	sys.exit(app.exec())
