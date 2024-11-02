import os

import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedLayout, QDockWidget,
)
from PyQt6.QtCore import Qt, pyqtSlot

from .file_explorer import FileExplorer
from .team_a_page import TeamAPage
from .team_b_page import TeamBPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Model Analysis")
        self.setMinimumSize(1000, 1000)

        # getting the directory
        base_directory = os.path.join(os.getcwd(), 'providers')
        print(f"base directory: {base_directory}")

        # sidebar
        self.file_explorer = FileExplorer(base_directory)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer)
        # Connect signals with debug prints
        print(f"Before: {self.file_explorer.file_selected}")
        self.file_explorer.file_selected.connect(self.on_file_selected)
        # self.file_explorer.file_selected.emit("/Documents/projects/model-analysis/providers/Netflix/NETFLIX_SHP.csv")
        print(f"After: {self.file_explorer.file_selected}")




        # Creating the different layouts
        page_layout = QVBoxLayout()
        tabs_layout = QHBoxLayout()
        self.stack_layout = QStackedLayout()

        page_layout.addLayout(tabs_layout)
        page_layout.addLayout(self.stack_layout)

        # creating the tabs for the teams
        team_a_tab_button = QPushButton("FINANCIAL ANALYST")
        team_a_tab_button.clicked.connect(self.activate_team_a_tab)

        tabs_layout.addWidget(team_a_tab_button)
        self.team_a_page = TeamAPage()
        self.stack_layout.addWidget(self.team_a_page)

        team_b_tab_button = QPushButton("PROVIDER PARTNER")
        tabs_layout.addWidget(team_b_tab_button)
        self.team_b_page = TeamBPage()
        team_b_tab_button.clicked.connect(self.activate_team_b_tab)

        self.stack_layout.addWidget(self.team_b_page)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def activate_team_a_tab(self):
        self.stack_layout.setCurrentIndex(0)

    def activate_team_b_tab(self):
        self.stack_layout.setCurrentIndex(1)

    def on_file_selected(self, file_path: str):
        print(f"file being loaded: {file_path}")
        self.team_a_page.search_tab.on_load_sidebar_file_to_table(file_path)


