import datetime
from typing import Optional

from PyQt6.QtCore import QSize, Qt, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from ui import static_data, styles, utils


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

		# the heading widget
		self.heading_text = QLabel(self)
		self.heading_text.setText("Run Data")
		self.heading_text.setProperty("class", "heading_label")
		self.heading_text.setStyleSheet(styles.HEADING)

		# implementing the run button and it's dialog.
		# run button implementation
		self.run_button_icon = QIcon("./icons/run-data-icon.svg")
		self.run_button = QPushButton(self)
		self.run_button.setText("Run Data")
		self.run_button.setIcon(self.run_button_icon)
		self.run_button.setIconSize(QSize(20, 20))
		self.run_button.setProperty("class", "run-button")
		self.run_button.setStyleSheet(styles.HEADING)
		self.run_button.clicked.connect(self.run_button_clicked)

		header_layout.addWidget(self.heading_text)

		# add space to force the button to the right.
		header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
		header_layout.addWidget(self.run_button)
		header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		# Add other layouts to the page layout
		page_layout.addLayout(header_layout)

	def run_button_clicked(self):
		"""A slot/function of what happens when the run button is clicked. Open the dialog for filtering and fetching data"""
		self.run_dialog = RunDataDialog(self.run_button_icon, self)

		if self.run_dialog.exec():
			print("fetching data was a success")
		else:
			print("fetching data faileld")


class RunDataDialog(QDialog):
	"""
	A dialog that lets users select specific data based on filter values.
	Contains three dropdown menus to filter by model type, year, and cycle.
	When the user confirms their selection, it fetches the corresponding data and passes it back to the main application.
	"""

	def __init__(self, window_icon: QIcon, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent)
		self.utils = utils.Utils()

		current_year = datetime.date.today().year

		self.setWindowTitle("Run Data")
		self.setWindowIcon(window_icon)
		self.setWindowIconText("Run data based on type, cycle and year.")
		self.dialog_layout = QVBoxLayout()

		self.setLayout(self.dialog_layout)

		self.filter_layout = QHBoxLayout()

		# type section
		self.type_layout, self.fiscal_layout, self.year_layout = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
		self.type_label = QLabel()
		self.type_label.setText("Select a model type")
		self.type_label.setStyleSheet(styles.FORM_LABEL)
		self.type_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignRight)
		self.type_combo = QComboBox()

		# adding the dropdown types and their values.
		for display_name, value in static_data.RUN_DATA_MODEL_TYPES.items():
			self.type_combo.addItem(display_name, userData=value)

		# add the type layout to the filter layout
		self.type_layout.addWidget(self.type_label, alignment=Qt.AlignmentFlag.AlignLeft)
		self.type_layout.addWidget(self.type_combo)
		self.filter_layout.addLayout(self.type_layout)

		# fiscal year section
		self.fiscal_label = QLabel()
		self.fiscal_label.setText("Select fiscal year")
		self.fiscal_label.setStyleSheet(styles.FORM_LABEL)
		self.fiscal_combo = QComboBox()
		self.fiscal_combo.setWhatsThis(
			"Select the fiscal year, with mid year being the quaters in the year and full year being a full calendar year with 12 months"
		)

		for display, value in static_data.RUN_DATA_FISCAL_YEARS.items():
			self.fiscal_combo.addItem(display, userData=value)

		self.fiscal_layout.addWidget(self.fiscal_label, alignment=Qt.AlignmentFlag.AlignTop)
		self.fiscal_layout.addWidget(self.fiscal_combo, alignment=Qt.AlignmentFlag.AlignBottom)

		self.filter_layout.addLayout(self.fiscal_layout)

		# year section
		self.year_label = QLabel()
		self.year_label.setText("Select a year")
		self.year_label.setStyleSheet(styles.FORM_LABEL)
		self.year_combo = QComboBox()
		self.year_combo.setToolTip("Select the year whose filter will be applied when fetching data")
		self.year_combo.setWhatsThis("Select the year whose filter will be applied when fetching data")
		self.year_combo.setProperty("class", "run-combo")
		self.year_combo.setStyleSheet(styles.HEADING)
		self.year_combo.addItems([str(year) for year in self.utils.get_decade_span(current_year)])
		self.year_combo.setCurrentIndex(5)  # set the current year as the default value

		self.year_layout.addWidget(self.year_label, alignment=Qt.AlignmentFlag.AlignTop)
		self.year_layout.addWidget(self.year_combo, alignment=Qt.AlignmentFlag.AlignBottom)
		self.filter_layout.addLayout(self.year_layout)

		# run button
		self.run_button = QPushButton()
		self.run_button.setText("Run Data")
		self.run_button.setIcon(window_icon)
		self.run_button.setIconSize(QSize(24, 24))
		self.run_button.setProperty("class", "run-button")
		self.run_button.setStyleSheet(styles.HEADING)

		self.dialog_layout.addLayout(self.filter_layout)
		self.dialog_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
		self.dialog_layout.addWidget(self.run_button)
		self.setMinimumHeight(30)
		self.setMinimumWidth(500)
