import shutil
from fileinput import filename

from PyQt6.QtGui import QIcon, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QMessageBox,
    QDialog, QLabel, QSpacerItem, QSizePolicy,
)
from PyQt6.QtCore import pyqtSlot, QSize, Qt
import os
import pandas as pd

from .blue_shield_id_model import BlueShieldIdModel
from .upload_form_dialog import UploadFormDialog


base_directory = os.getcwd()


class SearchTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.form_dialog = UploadFormDialog(self)

        self.current_df = (
            None  # the current dataframe that is displayed in the tree view
        )
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        search_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.form_dialog.setStyleSheet("background-color: #f8fafc; padding: 20px 16px 16px; border-radius: 6px; ")

        # styling the upload button
        raw_upload_button_icon = QIcon("./icons/upload_ids_icon")

        upload_button = QPushButton(icon=raw_upload_button_icon, text="Upload Ids")
        upload_button.setMinimumHeight(40)
        upload_button.setMaximumWidth(200)
        upload_button.setIconSize(QSize(20, 20))


        upload_button.setStyleSheet("background-color: rgba(0, 0, 250, 0.5); color: white; font-weight: 600; " "border-radius: 8px; ")

        # Keyboard shortcut for the upload button.
        upload_button_shortcut = QKeySequence("CTRL+U")
        upload_button.setShortcut(upload_button_shortcut)

        # Slot for the upload button
        upload_button.clicked.connect(self.upload_ids_file_slot)

        # Run Query button
        run_query_icon = QIcon("./icons/run_query_icon.svg")
        run_query_button = QPushButton(icon=run_query_icon, text="Run Query")
        run_query_button.setMinimumWidth(20)
        run_query_button.setMaximumWidth(200)
        run_query_button.setIconSize(QSize(20, 20))
        run_query_button.setStyleSheet("border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;")

        # run query button slot
        run_query_button.clicked.connect(self.run_query_slot)  # TODO: This button will instead connect to the slot that does the main query

        # EDIT BUTTON
        edit_icon = QIcon("./icons/edit_file_icon.svg")
        edit_button = QPushButton(icon=edit_icon, text="Edit")
        edit_button.setMinimumWidth(20)
        edit_button.setMaximumWidth(200)
        edit_button.setIconSize(QSize(20, 20))
        edit_button.setStyleSheet("border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;")


        # REFRESH BUTTON
        refresh_icon = QIcon("./icons/refresh_file_icon.svg")
        refresh_button = QPushButton(icon=refresh_icon, text="Refresh")
        refresh_button.setMinimumWidth(20)
        refresh_button.setMaximumWidth(200)
        refresh_button.setIconSize(QSize(20, 20))
        refresh_button.setStyleSheet(
            "border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;")

        button_layout.addWidget(upload_button)
        button_layout.addWidget(run_query_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(refresh_button)

        heading_text = QLabel("WELCOME, Financial Analyst")
        heading_text.setStyleSheet("font-size: 30px; margin: 10px 0px; line-height: 28px; font-weight: bold; color: #0f172a; ")

        header_layout = QHBoxLayout()
        header_layout.addWidget(heading_text)
        header_layout.addLayout(button_layout)
        header_layout.addSpacerItem(QSpacerItem(0 ,20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored))


        search_layout.addLayout(header_layout)

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
        # self.current_df = dataframe
        # model = BlueShieldIdModel(dataframe)
        # self.table_view.setModel(model)

        if dataframe is None or dataframe.empty:
            print("DataFrame is None or empty!")  # Debugging step
        else:
            print(dataframe.head())  # Print the first few rows for verification

        self.current_df = dataframe  # Store the new dataframe

        try:
            # Check if the model is correctly initialized with the dataframe
            model = BlueShieldIdModel(dataframe)
            self.table_view.setModel(model)

        except Exception as e:
            print(f"Error in updating table model: {e}")

    @pyqtSlot()
    def download_template_slot(self) -> None:
        """Download the template file to the user's Downloads folder."""
        template_file = os.path.join(base_directory, "resources", "template_ids.csv")

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
        form_dialog = self.form_dialog
        form_dialog.data_loaded.connect(self.on_data_loaded)

        if form_dialog.exec() == QDialog.DialogCode.Accepted:
            print("Dialog submission was successful...")

    @pyqtSlot(pd.DataFrame)
    def on_data_loaded(self, dataframe: pd.DataFrame) -> None:
        """Handle the loaded data from the UploadFormDialog."""
        self.update_table_model(dataframe)

    @pyqtSlot()
    def run_query_slot(self) -> None:
        """Run the query using the data store.csv file against the uploaded ids file"""
        # print(self.current_df.columns)
        if self.current_df is None or self.current_df.empty:
            QMessageBox.warning(self, "No Data", "No Data available for search query.")
            return

        data_store_path = os.path.join(base_directory, "resources", "data store.csv")
        if not os.path.exists(data_store_path):
            QMessageBox.critical(self, "Error", "Data store file not found.")
            return

        try:
            data_store_df = pd.read_csv(data_store_path)
            print(f"data store columns = {data_store_df}")

            if "BS_ID" not in data_store_df.columns:
                QMessageBox.critical(
                    self, "Error", "'data store.csv' must contain 'BS_ID' column."
                )
                return

            self.process_csv_file(data_store_df)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to load data store file: {str(e)}"
            )

    def process_csv_file(self, data_store_df: pd.DataFrame) -> None:
        """Process the data store csv file and merge it with the current data."""
        try:
            if data_store_df.empty:
                raise ValueError("The data store file is empty")

            common_id_name = "BS_ID"
            # if common_id_name not in data_store_df.columns or common_id_name not in self.current_df.columns:
            #     raise ValueError(f"Column '{common_id_name}' is not a valid column name in the datasets.")

            merged_df = pd.merge(
                self.current_df,
                data_store_df,
                how="left",
                on=common_id_name,
                suffixes=("", "_store"),
            )

            print("exporting data to csv")

            output_dir = os.path.join(base_directory, "resources")
            os.makedirs(
                output_dir, exist_ok=True
            )  # Create the directory if it doesn't exist

            try:
                print("exporting data to csv")
                output_path = os.path.join(output_dir, "output.csv")
                merged_df.to_csv(output_path, index=False)
                print("Data exported successfully to:", output_path)
            except Exception as e:
                print(f"Failed to export data to CSV: {e}")

            self.update_table_model(merged_df)
            QMessageBox.information(self, "Query Complete", "Data updated.")

            # update the columns with data from the store where available.
            # for column in data_store_df.columns:
            #     if column != common_id_name:
            #         merged_df[column] = merged_df[column].fillna(merged_df[f"{column}_store"])
            #         merged_df = merged_df.drop(columns=[f'{column}_store'])

            # # Remove rows where no match was found.
            # merged_df = merged_df.dropna(subset=data_store_df.columns, how='all')

            # if merged_df.equals(self.current_df):
            #     QMessageBox.information(self, "No Changes", "No new information returned from query")

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(
                self, "Error", f"Failed to process the query, {str(e)}"
            )
