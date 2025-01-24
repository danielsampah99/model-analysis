import os
from typing import Optional

import pandas as pd
from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QDockWidget, QMessageBox, QTreeView, QVBoxLayout, QWidget

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

    def __init__(self, directory: str, parent=None):
        super().__init__(parent)

        # widget to hold the layout.
        self.content_widget = QWidget()

        # setup the file system model.
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.csv"])
        self.model.setNameFilterDisables(False)
        self.model.setRootPath(directory)
        self.base_directory = directory

        # Set up the tree view.
        self.tree_view = QTreeView()
        self.tree_view.setAnimated(True)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(directory))

        # only show the file name column
        self.tree_view.setHeaderHidden(True)
        self.tree_view.hideColumn(1)  # Size
        self.tree_view.hideColumn(2)  # Type
        self.tree_view.hideColumn(3)  # Date Modified

        # handle file selection
        self.tree_view.clicked.connect(self._on_file_clicked)

        self.current_selected_file: Optional[str] = None

        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )

        # Create the layout without the parent.

        file_explorer_layout = QVBoxLayout()
        file_explorer_layout.setContentsMargins(0, -50, 5, 20)
        file_explorer_layout.addWidget(self.tree_view)

        # set the layout to the content widget
        self.content_widget.setLayout(file_explorer_layout)
        self.setWidget(self.content_widget)

    @pyqtSlot(QModelIndex)
    def _on_file_clicked(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            try:
                file_data = pd.read_csv(file_path)
                self.file_selected.emit(file_path)
                self.data_loaded.emit(file_data)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load file: {str(e)}")

    def refresh(self):
        """Refresh the file system view"""
        # Force the model to refresh its data
        current_index = self.tree_view.currentIndex()
        self.model.setRootPath("")  # Reset root path
        self.model.setRootPath(self.base_directory)  # Set it back
        self.tree_view.setRootIndex(self.model.index(self.base_directory))
        if current_index.isValid():
            self.tree_view.setCurrentIndex(current_index)
