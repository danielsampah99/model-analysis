from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


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
		header_layout = QHBoxLayout()
