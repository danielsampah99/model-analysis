# the financial analysts tab.
from typing import Optional

from PyQt6.QtWidgets import QWidget


class FinancialAnalyst(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
