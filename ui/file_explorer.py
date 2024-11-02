import os
from os import PathLike
from typing import Optional

import pandas as pd
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDockWidget, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot


class FileExplorer(QDockWidget):
    file_selected = pyqtSignal(str)
    data_loaded = pyqtSignal(pd.DataFrame)

    def __init__(self, directory: str,  parent=None):
        super().__init__(parent)

        self.current_selected_file: Optional[str] = None

        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        # widget to hold the layout.
        self.content_widget = QWidget()


        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Provider IDs")
        self.tree_widget.setColumnCount(1)
        self.tree_widget.itemClicked.connect(self.on_file_clicked)


        self.file_explorer_layout = QVBoxLayout(self.content_widget)
        self.file_explorer_layout.addWidget(self.tree_widget)
        self.file_explorer_layout.setContentsMargins(5, 20, 5, 20)
        self.setWidget(self.content_widget)

        self.load_directory(directory)

    def load_directory(self, directory: str | PathLike[str]) -> None:
        try:
            for file in os.listdir(path=directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    self.add_to_file_list(file, file_path)
                else:
                    self.add_to_folder_list(file, file_path)
        except PermissionError:
            QMessageBox.warning(self, "Permission Error", f"Permission denied accessing {directory}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading directory {directory}: {str(e)}")

    def add_to_folder_list(self, folder_name: str, path: str | PathLike[str]):
        folder_item = QTreeWidgetItem()
        folder_item.setText(0, folder_name)
        folder_icon = QIcon("./icons/folder_icon.svg")
        folder_item.setIcon(0, folder_icon)

        self.tree_widget.addTopLevelItem(folder_item)
        self.load_directory(path) # Recursively load the subdirectory

    def add_to_file_list(self, file_name: str, file_path: str):
        file_item = QTreeWidgetItem(self.tree_widget)
        file_item.setText(0, file_name)
        file_icon = QIcon("./icons/file_icon.svg")
        file_item.setIcon(0, file_icon)

        file_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
        self.tree_widget.addTopLevelItem(file_item)


    @pyqtSlot(QTreeWidgetItem)
    def on_file_clicked(self, item: QTreeWidgetItem) -> None:
        print("Item clicked!")  # Debug print
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path):
            try:
                file_data = pd.read_csv(file_path)
                self.current_selected_file = file_path

                self.file_selected.emit(file_path)
                self.data_loaded.emit(file_data)

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Something went wrong: {str(e)}")

