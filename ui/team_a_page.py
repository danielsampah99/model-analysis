import os

from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.financial_analysts import FinancialAnalyst

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
        self.financial_analysts = FinancialAnalyst()

        tabs.addTab(self.search_tab, "Search")
        tabs.addTab(self.financial_analysts, "Financial Analysts")

        page_layout = QVBoxLayout()

        page_layout.addWidget(tabs)

        self.setLayout(page_layout)
