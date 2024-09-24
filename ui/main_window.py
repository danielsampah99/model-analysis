from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedLayout,
)


from .team_a_page import TeamAPage
from .team_b_page import TeamBPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Model Analysis")

        # Creating the different layouts
        page_layout = QVBoxLayout()
        tabs_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        page_layout.addLayout(tabs_layout)
        page_layout.addLayout(self.stacklayout)

        # creating the tabs for the teams
        team_a_tab_button = QPushButton("TEAM A")
        team_a_tab_button.pressed.connect(self.activate_team_a_tab)

        tabs_layout.addWidget(team_a_tab_button)
        self.team_a_page = TeamAPage()
        self.stacklayout.addWidget(self.team_a_page)

        team_b_tab_button = QPushButton("TEAM B")
        tabs_layout.addWidget(team_b_tab_button)
        self.team_b_page = TeamBPage()
        team_b_tab_button.pressed.connect(self.activate_team_b_tab)

        self.stacklayout.addWidget(self.team_b_page)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def activate_team_a_tab(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_team_b_tab(self):
        self.stacklayout.setCurrentIndex(1)
