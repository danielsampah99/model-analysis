
from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

tab_list = ["Search", "Dashboard", "Data"]


class SearchTab(QWidget):
    def __init__(self) -> None:
        super().__init__()








class TeamAPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        tabs = QTabWidget()
        tabs.setMovable(True)
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.search_tab = SearchTab()
        tabs.addTab(self.search_tab, 'Search')
        

        page_layout = QVBoxLayout()

        
        page_layout.addWidget(tabs)
        self.setLayout(page_layout)
