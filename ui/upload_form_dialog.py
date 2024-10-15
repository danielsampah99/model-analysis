import os
import shutil
from PyQt6.QtWidgets import (
    QComboBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
)
from PyQt6.QtCore import pyqtSignal


from typing import Optional
import pandas as pd

base_directory = os.getcwd()

class UploadFormDialog(QDialog):
    data_loaded = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Blue Shield Provider IDs Form")
        self.setGeometry(500, 500, 500, 500)

        self.blue_shield_id_data = pd.DataFrame()
        self.selected_file: Optional[str] = None

        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the form's user interface"""

        form_layout = QFormLayout()

        # Provider's name input.
        self.filename_input = QLineEdit(self)
        form_layout.addRow("Model Provider's name:", self.filename_input)

        #  Model Line Of Business dropdown
        self.model_lob_dropdown = QComboBox(self)
        self.model_lob_dropdown.addItems(["Commercial", "SHP", "Medicaid"])
        form_layout.addRow("Model Line Of Business: ", self.model_lob_dropdown)

        # File selection button and label.
        self.file_button = QPushButton("Select Model Provider IDs", self)
        self.file_button.clicked.connect(self.select_file)
        self.selected_file_label = QLabel("")  # Initialized with empty text
        form_layout.addRow(self.file_button, self.selected_file_label)

        # download template file button
        self.download_template_file_button = QPushButton("Download Template File", self)
        self.download_template_file_button.clicked.connect(self.download_template_slot)

        #  Form Submission Button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_data)
        form_layout.addWidget(self.submit_button)

        form_layout.addWidget(self.download_template_file_button)

        # Completing the form's layout
        self.setLayout(form_layout)
        self.selected_file = None

        # download the template file.

    def download_template_slot(self) -> None:
        template_file = os.path.join(base_directory, "resources", "template_ids.csv")

        #  check if file exists. if it exists, download the file to the users computer. and alert them the file has been downloaded.
        if os.path.isfile(template_file):
            destination = os.path.join(
                os.path.expanduser("~"), "Downloads", "template_ids.csv"
            )

            shutil.copy(template_file, destination)

            #  show a file download complete alert to the user
            QMessageBox.information(
                self,
                "File Download Success.",
                f"Template file was downloaded to {destination}",
            )

        else:
            QMessageBox.warning(
                self,
                "File Not Found Error",
                "File was unable to download. please try again.",
            )

    def select_file(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(
            os.path.join(os.path.expanduser("~"), "Downloads")
        )  # TODO: should change to s drive in prod
        file_dialog.setNameFilter("File containing list of ids(*.csv)")

        if file_dialog.exec():
            self.selected_file = file_dialog.selectedFiles()[
                0
            ]  # GET THE PATH OF THE SELECTED FILE
            self.selected_file_label.setText(os.path.basename(self.selected_file))

    def submit_data(self) -> None:
        """Validate form inputs and process the selected file."""

        selected_file_name_value = self.selected_file_label.text()
        blue_shield_provider_name = self.filename_input.text()
        model_lob_value = self.model_lob_dropdown.currentText()

        if not selected_file_name_value:
            QMessageBox.warning(
                self, "Error", "please select a file that contains only the ids."
            )
            return

        if not self.model_lob_dropdown:
            QMessageBox.warning(
                self, "Error", "Please a select a value form the Model LOB field"
            )

        if not blue_shield_provider_name:
            QMessageBox.warning(
                self, "Error", "Please enter the Blue Shield Provider's name"
            )
            return

        self.load_provider_from_csv(
            file_path=self.selected_file,
            blue_shield_provider_name=blue_shield_provider_name,
            model_lob_value=model_lob_value,
        )

        # self.accept()

    def load_provider_from_csv(
        self, file_path: str, blue_shield_provider_name: str, model_lob_value: str
    ):
        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                dataframe = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx", ".xls"):
                dataframe = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file type")

            # add the blue shield provider name as the second column.
            dataframe.insert(1, "Model Name", blue_shield_provider_name)
            dataframe.insert(2, "Model Line of Business", model_lob_value)

            destination_path = os.path.join(
                f"{base_directory}", "providers", blue_shield_provider_name
            )
            os.makedirs(
                destination_path, exist_ok=True
            )  # create the directory is it's non-existent.

            output_file_name = os.path.join(
                destination_path,
                f"{blue_shield_provider_name.upper()}_{model_lob_value.upper()}.csv",
            )  # constructing the output file's name.

            dataframe.to_csv(output_file_name, index=False)
            self.blue_shield_id_data = dataframe  # assigning the filename to the property that will transfer the file path to the table view.

            #  success confirmation
            QMessageBox.information(
                self, "Success", f"File saved successfully: {output_file_name}"
            )

            # emit signal to the loaded data.
            self.data_loaded.emit(self.blue_shield_id_data)

        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "file not found or save was unsuccessful"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading {file_path}: {e}")

