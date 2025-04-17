import typing

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class ProfessionalParameter(QWidget):
	"""Professional parameter tab of the financial anaylst page"""

	def __init__(self, parent: typing.Optional["QWidget"] = None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		"""Initialize the ui of this widget"""

		# title and description
		title_label = QLabel("Professional Parameters", self)
		title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

		self.run_button = QPushButton("Run")
		self.run_button.setStyleSheet(
			"background-color: #6366F1; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold;"
		)

		page_heading_layout = QHBoxLayout()
		page_heading_layout.addWidget(title_label)
		page_heading_layout.addStretch(1)
		page_heading_layout.addWidget(self.run_button)

		# layout for the main widget.
		page_main_layout = QVBoxLayout()

		self.setLayout(page_main_layout)
