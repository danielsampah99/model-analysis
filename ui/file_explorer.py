import os
from os import PathLike
from typing import Optional

import pandas as pd
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QDockWidget, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

# file_explorer_stylesheet = """
#     QTreeWidget {
#         border: none; /* Remove border */
#         background-color: #f5f5f5; /* Sidebar background color */
#         padding: 10px; /* Padding around the content */
#         font-size: 14px; /* Font size */
#     }
#
#     QTreeWidget::item {
#         height: 24px; /* Height of each item */
#         padding-left: 10px; /* Base padding */
#         margin-left: 4px; /* Margin for a slight offset */
#     }
#
#     QTreeWidget::item:selected {
#         background-color: #d0e3ff; /* Highlight color for selected item */
#         color: black; /* Text color when selected */
#     }
#
#     QTreeWidget::branch:has-children {
#         padding-left: -8px; /* Additional padding for folder items */
#     }
# """


file_explorer_stylesheet = """
    QTreeWidget {
        border: none; /* Remove border */
        background-color: #f4f4f4; /* Sidebar background color */
        padding: 12px; /* Padding around the content */
        font-size: 14px; /* Font size */
        color: #333333; /* Text color */
    }

    QTreeWidget::item {
        height: 28px; /* Height of each item */
        padding-left: 12px; /* Base padding */
        margin: 2px 0; /* Vertical spacing between items */
    }

    QTreeWidget::item:selected {
        background-color: #e0e0e0; /* Highlight color for selected item */
        color: #000000; /* Text color when selected */
    }

    QTreeWidget::branch:open:has-children {
        image: url('./icons/open_folder_icon.svg'); /* Icon for open folder */
    }

    QTreeWidget::branch:closed:has-children {
        image: url('./icons/closed_folder_icon.svg'); /* Icon for closed folder */
    }

    QTreeWidget::branch:has-children {
        padding-left: 10px; /* Additional padding for folder items */
    }
"""

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
        self.tree_widget.itemClicked.connect(self.on_file_clicked) #type: ignore
        self.tree_widget.setStyleSheet(file_explorer_stylesheet)


        self.file_explorer_layout = QVBoxLayout(self.content_widget)
        self.file_explorer_layout.addWidget(self.tree_widget)
        self.file_explorer_layout.setContentsMargins(0, -50, 5, 20)
        self.setWidget(self.content_widget)

        # self.load_directory(directory)
        self.load_raw_ids_directory(directory)

    def load_raw_ids_directory(self, directory: str | PathLike[str]):
        """ put the raw ids under the directory in the sidebar"""
        try:
            print(f"files directory: {directory}")
            self.raw_ids_directory()
            for root, directories, files in os.walk(directory):
                for file in files:
                    print(f"file: {file}")
                    file_path = os.path.join(root, file)
                    print(f"file Path: {file_path}")
                    if os.path.isfile(file_path):
                        self.add_raw_id_file(file, file_path)
        except PermissionError:
            QMessageBox.warning(self, "Permission Error", f"Permission denied accessing the directory {directory}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Something went wrong: {str(e)}")


    def raw_ids_directory(self):
        """widget for the raw ids directory"""
        raw_id_dir = QTreeWidgetItem(self.tree_widget)

        raw_id_dir_icon = QIcon("./icons/folder_icon.svg")
        raw_id_dir.setIcon(0, raw_id_dir_icon)
        raw_id_dir.setData(0, Qt.ItemDataRole.DisplayRole, "Raw IDs")
        raw_id_dir.setFlags(Qt.ItemFlag.ItemIsEnabled)

        self.tree_widget.addTopLevelItem(raw_id_dir)


        # load files into the directory

    def add_raw_id_file(self, file_name: str, file_path: str | PathLike[str]):
        file_item = QTreeWidgetItem(self.tree_widget)
        file_item.setText(0, file_name)
        file_icon = QIcon("./icons/file_icon.svg")
        file_item.setIcon(0, file_icon)

        file_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
        self.tree_widget.addTopLevelItem(file_item)

    @pyqtSlot(QTreeWidgetItem)
    def on_file_clicked(self, item: QTreeWidgetItem) -> None:


        if item.text(0) == "Raw IDs":
            print("folder clicked!")  # Debug print

            # item.setExpanded(not item.isExpanded())



        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path):
            try:
                print("file clicked!")  # Debug print
                file_data = pd.read_csv(file_path)
                self.current_selected_file = file_path

                self.file_selected.emit(file_path) #type: ignore
                print(f"file select signal emitted: {file_path}")  # Debug print
                print(f"file select signal emitted: {self.file_selected}")  # Debug print

                self.data_loaded.emit(file_data) #type: ignore

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Something went wrong: {str(e)}")

