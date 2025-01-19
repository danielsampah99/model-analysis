import os
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout, QWidget

from .file_explorer import FileExplorer
from .team_a_page import TeamAPage
from .team_b_page import TeamBPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Model Analysis")
        self.setMinimumSize(800, 800)

        # getting the directory
        self.base_directory = os.path.join(os.getcwd(), "providers", "raw-ids")

        # create the folders
        self.create_starting_folders()

        # sidebar
        self.file_explorer = FileExplorer(self.base_directory)
        self.file_explorer.file_selected.connect(self.on_file_selected)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer)

        # Creating the different layouts
        page_layout = QVBoxLayout()
        tabs_layout = QHBoxLayout()
        self.stack_layout = QStackedLayout()

        page_layout.addLayout(tabs_layout)
        page_layout.addLayout(self.stack_layout)

        # creating the tabs for the teams
        team_a_tab_button = QPushButton("FINANCIAL ANALYST")
        team_a_tab_button.clicked.connect(self.activate_team_a_tab)  # type: ignore

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

    def create_starting_folders(self):
        """create the folders by which the whole application will organize models into years"""
        number_of_years = 10
        current_year = datetime.now().year

        for i in range(number_of_years):
            year_path = os.path.join(self.base_directory, str(current_year + i))
            os.makedirs(name=year_path, exist_ok=True)
