# Single id upload
import os
from typing import List, Optional

import pandas as pd
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QButtonGroup, QCheckBox, QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from database import Database
from ui.file_explorer import FileExplorer
from ui.utils import Utils

label_styles = "font-size: 14px; line-height: 24px; font-weight: 500; color: #111827; "
input_styles = "width: 100%; border-radius: 6px; border: 0.725 solid #d1d5db; padding: 6px 0; background-color: white; color: #111827; outline: 1px inset #D1D5DB; font-size: 14px; line-height: 1.5;"


# Style everything
form_styles = """
        #contentPanel {
            padding: 24px;
        }
        QLabel {
            font-size: 14px;
            font-weight: 500;
            color: #111827;
            margin-bottom: 4px;
        }
        QLineEdit {
            padding: 8px 12px;
            border: 1px solid #D1D5DB;
            border-radius: 6px;
            background: white;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #4F46E5;
            outline: none;
        }
        QDialog {
       		background-color: white;
           	border: 1px solid #E5E7EB;
            border-radius: 8px;
        }
        #dialogButton {
            background-color: #4F46E5;  /* indigo-600 */
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
            width: 100%;
        }
        QComboBox {

            border: 1px solid #D1D5DB;
            border-radius: 6px;
            background: white;
            font-size: 14px;
        }
        QComboBox:hover {
            border-color: #9CA3AF;
        }
        QComboBox:focus {
            border: 2px solid #4F46E5;
        }
        #dialogButton:hover {
            background-color: #4338CA;  /* indigo-700 */
        }
        #dialogButton:pressed {
            background-color: #3730A3;  /* indigo-800 */
        }
       """

dropdown_styles = f"{input_styles} QLineEdit::placeholder {{color: #9CA3AF;}} QLineEdit::focus {{border: 2px solid #4F46E5;}}"


class SingleIdDialog(QDialog):
    def __init__(self, file_explorer: FileExplorer, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.utils = Utils()

        self.parent_widget = parent
        self.file_explorer = file_explorer

        self.database = Database()

        self.submit_button = None
        # self.provider_id_input = None
        # self.provider_name_input = None
        self.provider_name_label = None
        # self.model_lob_dropdown = None
        self.model_lob_options = [""]
        self.model_type_options = ["Facility", "Professional", "Behavorial Health", "Surgery Centre", "Anesthesia"]
        self.cycle_options: List[str] = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.model_lob_label = None

        self.content = QWidget(self)
        self.submit_button: Optional[QPushButton] = None
        self.init_ui()

    def init_ui(self) -> None:
        # form
        self.setMinimumWidth(500)
        self.setStyleSheet(form_styles)
        form_layout = QFormLayout(self)
        form_layout.setContentsMargins(24, 24, 24, 24)

        self.provider_name_label = QLabel(self)
        self.provider_name_label.setText("Model Provider's Name")
        self.provider_name_input = QLineEdit(self)
        self.provider_name_input.setStyleSheet(input_styles)
        self.provider_name_input.setPlaceholderText("Model provider's name...")
        self.provider_name_input.setToolTip("Enter the full name of the new provider")

        #  Model Line Of Business dropdown
        self.model_lob_options: list[str] = ["Commercial", "SHP", "Medicaid"]
        self.model_lob_dropdown = QComboBox(self)
        self.model_lob_dropdown.setStyleSheet(dropdown_styles)
        self.model_lob_dropdown.setPlaceholderText("Line of business...")
        self.model_lob_dropdown.setToolTip("Select the line of business for this provider")

        self.model_lob_label = QLabel("Model Line Of Business")
        self.model_lob_label.setStyleSheet(label_styles)
        self.model_lob_dropdown.addItems(self.model_lob_options)
        self.model_lob_dropdown.setCurrentText(self.model_lob_options[0])

        provider_id_label = QLabel(self)
        provider_id_label.setStyleSheet(label_styles)
        provider_id_label.setText("Model Provider's Id")

        self.provider_id_input = QLineEdit(self)
        self.provider_id_input.setPlaceholderText("Model provider's id")
        self.provider_id_input.setStyleSheet(input_styles)
        self.provider_id_input.setToolTip("Enter the provider's unique identifier")

        # Model type dropdown
        self.model_type_label = QLabel(text="Model Type", parent=self)
        self.model_type_label.setStyleSheet(label_styles)

        self.model_type_dropdown = QComboBox(self)
        self.model_type_dropdown.setStyleSheet(dropdown_styles)
        self.model_type_dropdown.addItems(self.model_type_options)
        self.model_type_dropdown.setToolTip("Select the model type")

        self.anaylst_label = QLabel(text="Select a financial analyst", parent=self)
        self.anaylst_label.setStyleSheet(label_styles)

        self.analyst_combo = QComboBox(self)
        self.analyst_combo.setStyleSheet(dropdown_styles)
        titled_analyst_names = [analyst.title() for analyst in self.database.get_all_financial_analysts()]
        self.analyst_combo.addItems(titled_analyst_names)
        self.analyst_combo.setToolTip("Select the financial analyst creating this model")

        # cycle
        self.cycle_label = QLabel(text="Select a Cycle", parent=self)
        self.cycle_label.setStyleSheet(label_styles)

        self.cycle_combo = QComboBox(self)
        self.cycle_combo.setStyleSheet(dropdown_styles)
        self.cycle_combo.addItems(self.cycle_options)
        self.cycle_combo.setToolTip("Select the cycle this model will belong to")

        # checkboxes
        # facility checkboxes
        self.in_patient_only_checkbox = QCheckBox(self)
        self.in_patient_only_checkbox.setText("In Patient")
        self.in_patient_only_checkbox.show()  # hide initially and show when a model type has been selected.

        self.out_patient_only_checkbox = QCheckBox(self)
        self.out_patient_only_checkbox.setText("Out Patient")
        self.out_patient_only_checkbox.show()

        # professional model type - categories
        # group the checkboxes to make them exclusive. i.e. only should be selected at any point in time.
        self.professional_categories = QButtonGroup(self)
        self.clinic_and_anesthesia_checkbox = QCheckBox(self)
        self.clinic_and_anesthesia_checkbox.setText("Clinic and Anaesthesia")
        self.clinic_and_anesthesia_checkbox.hide()

        self.clinic_checkbox = QCheckBox(self)
        self.clinic_checkbox.setText("Clinic")
        self.clinic_checkbox.hide()

        self.professional_categories.addButton(self.clinic_checkbox)
        self.professional_categories.addButton(self.clinic_and_anesthesia_checkbox)

        # submit button
        # Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            "border-radius: 6px; background-color: #4f46e5; padding: 12px 8px; font-size: 14px; font-weight: 600; color: white; "
        )
        self.submit_button.setObjectName("dialogButton")
        self.submit_button.clicked.connect(self.on_form_submit)

        # add widgets to the form's layout
        form_layout.setSpacing(20)
        form_layout.addRow(self.provider_name_label, self.provider_name_input)
        form_layout.addRow(provider_id_label, self.provider_id_input)
        form_layout.addRow(self.model_lob_label, self.model_lob_dropdown)
        form_layout.addRow(self.anaylst_label, self.analyst_combo)
        form_layout.addRow(self.cycle_label, self.cycle_combo)
        form_layout.addRow(self.model_type_label, self.model_type_dropdown)

        # only show patient checkboxes when the model type is 'facility'

        form_layout.addRow(self.in_patient_only_checkbox, self.out_patient_only_checkbox)
        form_layout.addRow(self.clinic_checkbox, self.clinic_and_anesthesia_checkbox)
        self.model_type_dropdown.currentIndexChanged.connect(self.show_model_category_checkboxes)

        form_layout.addRow(self.submit_button)

        self.setLayout(form_layout)

    @pyqtSlot(int)
    def show_model_category_checkboxes(self, index: int):
        """update what checkboxes to show based on the selected model type"""
        if index == 0:
            # show only the facility checkboxes and uncheck the hidden checkboxes
            self.in_patient_only_checkbox.show()
            self.out_patient_only_checkbox.show()
            self.clinic_checkbox.hide()
            self.clinic_and_anesthesia_checkbox.hide()
            self.clinic_checkbox.setChecked(False)
            self.clinic_and_anesthesia_checkbox.setChecked(False)

        if index == 1:  # show professional checkboxes
            self.clinic_checkbox.show()
            self.clinic_and_anesthesia_checkbox.show()
            self.in_patient_only_checkbox.hide()
            self.out_patient_only_checkbox.hide()
            self.in_patient_only_checkbox.setChecked(False)
            self.out_patient_only_checkbox.setChecked(False)

        if index != 1 or index != 0:
            """hide the facility checkboxes if other options are selected"""
            self.in_patient_only_checkbox.hide()
            self.out_patient_only_checkbox.hide()
            self.clinic_checkbox.hide()
            self.clinic_and_anesthesia_checkbox.hide()
            self.clinic_checkbox.setChecked(False)
            self.clinic_and_anesthesia_checkbox.setChecked(False)
            self.in_patient_only_checkbox.setChecked(False)
            self.out_patient_only_checkbox.setChecked(False)

    @pyqtSlot()
    def on_form_submit(self):
        """Submit the single id form"""
        self.form_validation()
        self.write_data_to_file()
        self.accept()
        # todo : load the data onto the canvas,
        # todo: refresh the sidebar.

    def form_validation(self) -> None:
        """validate single id form"""
        if not self.provider_name_input.text():
            self.show_error("Model's provider name cannot be empty")

        if not self.provider_name_input.text():
            self.show_error("Provider's ID is required")

        if not self.model_lob_dropdown.currentText():
            self.show_error("Select at least one Line of Business for the model")

    def show_error(self, error_message: str) -> None:
        """Show an error popup"""
        QMessageBox.critical(self, "Validation Error", error_message)

    def selected_model_category(self) -> str:
        """What to return or put in the excel file based on what category is selected in the form"""
        if self.in_patient_only_checkbox.isChecked() and self.out_patient_only_checkbox.isChecked():
            return "BOTH"
        elif self.in_patient_only_checkbox.isChecked():
            return "IN-PATIENT-ONLY"
        elif self.out_patient_only_checkbox.isChecked():
            return "OUT-PATIENT-ONLY"
        elif self.clinic_checkbox.isChecked():
            return "CLINIC"
        elif self.clinic_and_anesthesia_checkbox.isChecked():
            return "CLINIC AND ANESTHEISA"
        else:
            return "NONE"

    def write_data_to_file(self) -> None:
        print("\n=== Starting write_data_to_file ===")
        # create a file from the form's data
        destination_path = os.path.join(
            f"{self.utils.get_current_year_directory()}",
            f"{self.cycle_combo.currentText()}",
            f"{self.provider_name_input.text().title()}-{self.utils.format_model_type_name(self.model_type_dropdown.currentText())}",
        )

        # make the path if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)

        df = pd.DataFrame(
            data={
                "BS_ID": [str(self.provider_id_input.text())],
                "Model Name": [self.provider_name_input.text()],
                "Model Line of Business": [self.model_lob_dropdown.currentText()],
                "Model Type": [self.utils.format_model_type_name(self.model_type_dropdown.currentText())],
                "Financial Analyst": [self.analyst_combo.currentText().title()],
                "Model Category": [self.selected_model_category()],
            }
        )

        output_file_path = os.path.join(
            destination_path, f"{self.provider_name_input.text().upper()}_{self.model_lob_dropdown.currentText().upper()}-RAW_ID.csv"
        )

        # save the file to the destination
        df.to_csv(output_file_path, index=False)

        # Refresh the file explorer after creating the file.
        print(f"trying to load: {output_file_path}")

        if self.file_explorer:
            print(f"File explorer instance found: {self.file_explorer}")
            print("Emitting refresh_requested signal")
            print("found the file explorer class")
            self.file_explorer.refresh()
        else:
            print("No file explorer instance found!")

        print("=== Finished write_data_to_file ===\n")
