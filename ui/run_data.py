from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from ui import styles


class RunDataTab(QWidget):
	"""
	The Run data tab of the application, in the financial anaylst section.
	Click the 'run data' button and select the correct filter values(model type, cycle and year) to run specific data.
	"""

	def __init__(self) -> None:
		super().__init__()

		# initiialize the user interface
		self.init_ui()

	def init_ui(self):
		"user interface of the 'run data' tab"
		page_layout = QVBoxLayout()

		# set the central layout of this page.
		self.setLayout(page_layout)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

		header_layout = QHBoxLayout()
		header_layout.setProperty("class", "heading_container")

		self.heading_text = QLabel(self)
		self.heading_text.setText("Run Data")
		self.heading_text.setProperty("class", "heading_label")
		self.heading_text.setStyleSheet(styles.HEADING)

		header_layout.addWidget(self.heading_text)

		# Add other layouts to the page layout
		page_layout.addLayout(header_layout)
