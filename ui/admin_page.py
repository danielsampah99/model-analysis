import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ui.users import Users


class AdminPage(QWidget):
	"""All the features exclusive to the administrator"""

	def __init__(self):
		super().__init__()

		self.tabs = QTabWidget(self)
		self.tabs.setTabPosition(QTabWidget.TabPosition.West)

		self.users_tab = Users()
		self.tabs.addTab(self.users_tab, "Users")

		self.page_layout = QVBoxLayout(self)
		self.page_layout.addWidget(self.tabs)

		self.setLayout(self.page_layout)
