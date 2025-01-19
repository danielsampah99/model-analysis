# Single id upload
import os
from typing import Optional

import pandas as pd
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from ui.file_explorer import FileExplorer

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

        self.parent_widget = parent
        self.file_explorer = file_explorer

        self.submit_button = None
        # self.provider_id_input = None
        # self.provider_name_input = None
        self.provider_name_label = None
        # self.model_lob_dropdown = None
        self.model_lob_options = [""]
        self.model_type_options = ["Facility", "Professional", "Behavorial Health", "Surgery Centre", "Anesthesia"]
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
        self.model_type_label = QLabel(text="Type of Model Provider", parent=self)
        self.model_type_label.setStyleSheet(label_styles)

        self.model_type_dropdown = QComboBox(self)
        self.model_type_dropdown.setStyleSheet(dropdown_styles)
        self.model_type_dropdown.addItems(self.model_type_options)
        self.model_type_dropdown.setToolTip("Select the type of model provider")

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
        form_layout.addRow(self.model_type_label, self.model_type_dropdown)
        form_layout.addRow(self.submit_button)

        self.setLayout(form_layout)

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

    def write_data_to_file(self) -> None:
        print("\n=== Starting write_data_to_file ===")
        # create a file from the form's data
        destination_path = os.path.join(f"{os.getcwd()}", "providers", "raw-ids", f"{self.provider_name_input.text()}")

        # make the path if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)

        df = pd.DataFrame(
            data={
                "BS_ID": [str(self.provider_id_input.text())],
                "Model Name": [self.provider_name_input.text()],
                "Model Line of Business": [self.model_lob_dropdown.currentText()],
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
