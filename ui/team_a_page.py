import os

from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.users import Users

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
        self.users = Users()

        tabs.addTab(self.search_tab, "Search")
        tabs.addTab(self.users, "Users")

        page_layout = QVBoxLayout()

        page_layout.addWidget(tabs)

        self.setLayout(page_layout)
