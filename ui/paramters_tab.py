from typing import Optional

from PyQt6.QtWidgets import QHBoxLayout, QTabWidget, QVBoxLayout, QWidget

from ui.professional_parameter import ProfessionalParameter


class ParamtersTab(QWidget):
	"""The parameters page of financial analysts"""

	def __init__(self, parent: Optional[QWidget] = None):
		super().__init__(parent)
		self.professional_param = ProfessionalParameter()
		self.init_ui()

	def init_ui(self):
		"""Initialize the user interface"""
		page_layout = QVBoxLayout()

		self.tabs = QTabWidget(self)
		self.tabs.setTabPosition(QTabWidget.TabPosition.South)
		self.tabs.setTabShape(QTabWidget.TabShape.Rounded)
		self.tabs.addTab(self.professional_param, "Professional")

		page_layout.addWidget(self.tabs)
		heading_layout = QHBoxLayout()
		page_layout.addLayout(heading_layout)
		self.setLayout(page_layout)
