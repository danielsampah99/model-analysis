import os

from PyQt6.QtWidgets import (
	QTabWidget,
	QVBoxLayout,
	QWidget,
)

from .paramters_tab import ParamtersTab
from .search_tab import SearchTab

# import datetime

tab_list = ["Search", "DataCode", "Charge Master", "Scenarios", "Reports"]

base_directory = os.getcwd()


class TeamAPage(QWidget):
	def __init__(self) -> None:
		super().__init__()

		tabs = QTabWidget()
		tabs.setTabPosition(QTabWidget.TabPosition.West)
		tabs.setMovable(True)

		self.search_tab = SearchTab()
		self.paramters_tab = ParamtersTab()

		tabs.addTab(self.search_tab, "Search")
		tabs.addTab(self.paramters_tab, "Parameters")

		page_layout = QVBoxLayout()

		page_layout.addWidget(tabs)

		self.setLayout(page_layout)
