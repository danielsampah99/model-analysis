from PyQt6.QtWidgets import (
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class TeamBPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        tabs = QTabWidget()
        tabs.setMovable(True)
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        page_layout = QVBoxLayout()

        label = QLabel("Team B Page")

        page_layout.addWidget(label)
        self.setLayout(page_layout)
