import os

from PyQt6.QtWidgets import (
	QTabWidget,
	QVBoxLayout,
	QWidget,
)

from ui.run_data import RunDataTab

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

		# defining the tabs on the left side of the application
		self.search_tab = SearchTab()
		self.run_data_tab = RunDataTab()
		self.paramters_tab = ParamtersTab()

		tabs.addTab(self.search_tab, "Search")
		tabs.addTab(self.run_data_tab, "Run Data")
		tabs.addTab(self.paramters_tab, "Parameters")

		page_layout = QVBoxLayout()

		page_layout.addWidget(tabs)

		self.setLayout(page_layout)
