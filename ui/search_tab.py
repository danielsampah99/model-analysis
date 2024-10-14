import shutil
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QMessageBox,
    QDialog,
)
from PyQt6.QtCore import pyqtSlot
import os
import pandas as pd

from .blue_shield_id_model import BlueShieldIdModel
from .upload_form_dialog import UploadFormDialog


base_directory = os.getcwd()

class SearchTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        search_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        upload_button = QPushButton("Upload IDs")
        download_template_button = QPushButton("Run Query")

        upload_button.clicked.connect(self.upload_ids_file_slot)
        download_template_button.clicked.connect(self.download_template_slot)

        button_layout.addWidget(upload_button)
        button_layout.addWidget(download_template_button)

        search_layout.addLayout(button_layout)

        self.table_view = QTableView()
        search_layout.addWidget(self.table_view)

        self.setLayout(search_layout)

        self.load_template_data()

    def load_template_data(self) -> None:
        """Load the template data into the table view."""
        try:
            template_file = os.path.join(
                base_directory, "resources", "template_ids.csv"
            )
            dataframe = pd.read_csv(template_file)
            self.update_table_model(dataframe)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to load template file: {str(e)}"
            )

    def update_table_model(self, dataframe: pd.DataFrame) -> None:
        """Update the table view with new data."""
        model = BlueShieldIdModel(dataframe)
        self.table_view.setModel(model)

    @pyqtSlot()
    def download_template_slot(self) -> None:
        """Download the template file to the user's Downloads folder."""
        template_file = os.path.join(
            self.base_directory, "resources", "template_ids.csv"
        )

        if os.path.isfile(template_file):
            destination = os.path.join(
                os.path.expanduser("~"), "Downloads", "template_ids.csv"
            )
            shutil.copy(template_file, destination)
            QMessageBox.information(
                self,
                "File Download Success",
                f"Template file was downloaded to {destination}",
            )
        else:
            QMessageBox.warning(
                self,
                "File Not Found Error",
                "File was unable to download. Please try again.",
            )

    @pyqtSlot()
    def upload_ids_file_slot(self) -> None:
        """Open the form dialog to upload IDs file."""
        form_dialog = UploadFormDialog(self)
        form_dialog.data_loaded.connect(self.on_data_loaded)

        if form_dialog.exec() == QDialog.DialogCode.Accepted:
            print("Dialog submission was successful...")

    @pyqtSlot(pd.DataFrame)
    def on_data_loaded(self, dataframe: pd.DataFrame) -> None:
        """Handle the loaded data from the UploadFormDialog."""
        self.update_table_model(dataframe)


# class SearchTabs(QWidget):
#     def __init__(self) -> None:
#         super().__init__()

#         search_layout = QVBoxLayout()
#         button_layout = QHBoxLayout()

#         upload_button = QPushButton("Upload IDs")
#         run_query_button = QPushButton("Download Template")

#         self.table_widget = QTableView()
#         # view_ids_table_widget = QWidget()

#         run_query_button.pressed.connect(self.download_template_slot)
#         upload_button.pressed.connect(self.upload_ids_file_slot)

#         button_layout.addWidget(upload_button)
#         button_layout.addWidget(run_query_button)

#         search_layout.addLayout(button_layout)

#         # Loading the template file into the dataframe
#         try:
#             template_file = os.path.join(
#                 base_directory, "resources", "template_ids.csv"
#             )
#             self.dataframe = pd.read_csv(template_file)
#             self.model = BlueShieldIdModel(self.dataframe)

#             #  setting up the table view
#             self.table = QTableView()
#             self.table.setModel(self.model)

#         except Exception as e:
#             QMessageBox.critical(
#                 self, "Something went wrong", f"Failed to show template file: {str(e)}"
#             )

#         # adding the table mdoel to the view.
#         self.form_dialog = UploadFormDialog(self)
#         self.blue_shield_data = self.form_dialog.blue_shield_id_data

#         print(self.blue_shield_data)

#         self.blue_shield_id_model = BlueShieldIdModel(
#             self.blue_shield_data
#         )  # find a way to get the dataframe into this.
#         self.table.setModel(self.blue_shield_id_model)
#         search_layout.addWidget(self.table_widget)

#         self.setLayout(search_layout)

#     def download_template_slot(self):
#         template_file = os.path.join(base_directory, "resources", "template_ids.csv")

#         #  check if file exists. if it exists, download the file to the users computer. and alert them the file has been downloaded.
#         if os.path.isfile(template_file):
#             destination = os.path.join(
#                 os.path.expanduser("~"), "Downloads", "template_ids.csv"
#             )

#             shutil.copy(template_file, destination)

#             #  show a file download complete alert to the user
#             QMessageBox.information(
#                 self,
#                 "File Download Success.",
#                 f"Templage file was downlaoded to {destination}",
#             )

#         else:
#             QMessageBox.warning(
#                 self,
#                 "File Not Found Error",
#                 "File was unable to download. please try again.",
#             )

#     def upload_ids_file_slot(self):
#         """Open the form dialog and enter necessary values.
#         Save the uploaded file to a directory on the S Drive"""
#         formDialog = UploadFormDialog(self)
#         # dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
#         # dialog.setDirectory(
#         #     os.path.join(os.path.expanduser("~"), "Downloads")
#         # )
#         # dialog.setNameFilter("File containing list of ids(*.csv)")
#         # dialog.setViewMode(QFileDialog.ViewMode.List)

#         if formDialog.exec() == QDialog.DialogCode.Accepted:
#             print("Dialog submission was successful...")
