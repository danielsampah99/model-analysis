import os
import shutil
from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QWidget,
    QPushButton,
    QMessageBox,
    QTableView,
    QFileDialog,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
)
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
import pandas as pd
import datetime

tab_list = ["Search", "Data" "Code", "Charge Master", "Scenarios", "Reports"]

base_directory = os.getcwd()


class IdDateModel(QAbstractTableModel):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__()

        self._data_frame = data_frame

    def get_shape(self):
        """return the shape of the data as tuple in the form(row_count, column_count)"""
        return self._data_frame.shape

    def get_data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data_frame.iat[index.row(), index.column()])

        return None

    def get_data_headers(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._data_frame.columns[section]

            else:
                return str(section + 1)

        return None


class UploadFormDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setWindowTitle("Provider IDs Form")
        self.setGeometry(500, 500, 500, 500)

        # Create the form's layout
        form_layout = QFormLayout()

        # LineEdit for filename input
        self.filename_input = QLineEdit(self)
        form_layout.addRow("Name of Blue Shield Provider:", self.filename_input)

        #  Bill type element of the form
        self.bill_type_dropdown = QComboBox(self)
        self.bill_type_dropdown.addItems(["Bill Type 1", "Bill Type 2", "Bill Type 3"])
        form_layout.addRow("Bill Type", self.bill_type_dropdown)

        # mv eff dt element of the form
        self.mv_eff_dt = QLineEdit(self)
        form_layout.addRow("MV_EFF_DT", self.mv_eff_dt)

        # par in network 0011
        self.par_in_network_011 = QLineEdit(self)
        form_layout.addRow("Par in Network 0011", self.par_in_network_011)

        # wh flag descending
        self.wh_flag_desc = QLineEdit(self)
        form_layout.addRow("WH FLAG DESC", self.wh_flag_desc)

        # MV STUS C
        self.mv_stus_c = QLineEdit(self)
        form_layout.addRow("MV_STUS_C", self.mv_stus_c)

        # LAST UPDATE
        self.last_update = QLineEdit(self)
        form_layout.addRow("Last Update", self.last_update)

        # ADDRESS LINE ONE
        self.address_line_1 = QLineEdit(self)
        form_layout.addRow("Address LIne 1", self.address_line_1)

        # Button to select a file
        self.file_button = QPushButton(
            "Select csv or file with Blue Shied Provider IDs", self
        )
        self.file_button.clicked.connect(self.select_file)

        # element for the selected file's name
        self.selected_file_label = QLabel("")  # Initialized with empty text
        form_layout.addRow(self.file_button, self.selected_file_label)

        #  Form Submission Button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_data)
        form_layout.addWidget(self.submit_button)

        # Completing the form's layout
        self.setLayout(form_layout)
        self.selected_file = None

    def select_file(self):
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

    def submit_data(self):
        #  Retrieve the form's value.

        # uploaded_file = self.uploaded_file_input.text()
        selected_file_name_value = self.selected_file_label.text()
        blue_shield_provider_name = self.filename_input.text()

        if not selected_file_name_value:
            QMessageBox.warning(
                self, "Error", "please select a file that contains only the ids."
            )
            return

        if not blue_shield_provider_name:
            QMessageBox.warning(
                self, "Error", "Please enter the Blue Shield Provider's name"
            )
            return

        self.load_provider_from_csv(
            file_path=self.selected_file,
            blue_shield_provider_name=blue_shield_provider_name,
        )

        print(
            f"slected file name: {self.selected_file}\n, blue shield id: {blue_shield_provider_name}"
        )

        """
            1. get the file path,
            2. open it with pandas, check if it's a .csv or excel file use the appopriate method.
            3. add the the blue_shield provider name as the second column while keeping the first and use the same variable as the name of the file to be stored.
            4. display the file in the other dialog
        """

        self.accept()

    def load_provider_from_csv(self, file_path: str, blue_shield_provider_name: str):
        # #  clear existing data in the grid table.
        # self.model.clear()

        # Load the data from the csv file.
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    dataframe = pd.read_csv(file_path)
                elif file_path.endswith(".xlsx", ".xls"):
                    dataframe = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file type")

                # add the blue shield provider name as the second column.
                dataframe.insert(
                    1, "Blue Shield Provider Name", blue_shield_provider_name
                )

                #  save the output file.
                # get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                destination_path = os.path.join(
                    f"{base_directory}", "providers", blue_shield_provider_name
                )
                os.makedirs(
                    destination_path, exist_ok=True
                )  # create the directory is it's non-existent.

                output_file_name = os.path.join(
                    destination_path, f"{blue_shield_provider_name.lower()}_{timestamp}.csv"
                )  # constructing the output file's name.

                dataframe.to_csv(output_file_name, index=False)

                #  success confirmation
                QMessageBox.information(
                    self, "Success", f"File saved successfully: {output_file_name}"
                )

            except FileNotFoundError:
                QMessageBox.warning(
                    self, "Error", "file not found or save was unsuccessful"
                )
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error loading {file_path}: {e}")


class SearchTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        search_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        upload_button = QPushButton("Upload IDs")
        download_button = QPushButton("Download Template")
        view_ids_table_widget = QWidget()

        download_button.pressed.connect(self.download_template_slot)
        upload_button.pressed.connect(self.upload_ids_file_slot)

        button_layout.addWidget(upload_button)
        button_layout.addWidget(download_button)

        search_layout.addLayout(button_layout)

        # Loading the template file into the dataframe
        try:
            template_file = os.path.join(
                base_directory, "resources", "template_ids.csv"
            )
            self.dataframe = pd.read_csv(template_file)
            self.model = IdDateModel(self.dataframe)

            #  setting up the table view
            self.table = QTableView()
            self.table.setModel(self.model)

        except Exception as e:
            QMessageBox.critical(
                self, "Something went wrong", f"Failed to show template file: {str(e)}"
            )

        search_layout.addWidget(view_ids_table_widget)
        self.setLayout(search_layout)

    def download_template_slot(self):
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
                "File download complete.",
                f"Templage file was downlaoded to {destination}",
            )

        else:
            QMessageBox.warning(
                self,
                "File Not Found Error",
                "File was unable to download. please try again.",
            )

    def upload_ids_file_slot(self):
        """Open the form dialog and enter necessary values.
        Save the uploaded file to a directory on the S Drive"""
        formDialog = UploadFormDialog(self)
        # dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # dialog.setDirectory(
        #     os.path.join(os.path.expanduser("~"), "Downloads")
        # )
        # dialog.setNameFilter("File containing list of ids(*.csv)")
        # dialog.setViewMode(QFileDialog.ViewMode.List)

        if formDialog.exec() == QDialog.DialogCode.Accepted:
            print("Dialog submission was successful...")


class TeamAPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)

        self.search_tab = SearchTab()
        tabs.addTab(self.search_tab, "Search")

        page_layout = QVBoxLayout()

        page_layout.addWidget(tabs)
        self.setLayout(page_layout)
