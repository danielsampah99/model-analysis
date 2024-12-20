# Single id upload
import os
from typing import Optional

from PyQt6.QtGui import QPainter, QColor, QPaintEvent
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox, \
    QDialog
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSlot
import pandas as pd

label_styles = "font-size: 14px; line-height: 24px; font-weight: 500; color: #111827; "
input_styles = "width: 100%; border-radius: 6px; border: 0.725 solid #d1d5db; padding: 6px 0; background-color: white; color: #111827; outline: 1px inset #D1D5DB; font-size: 14px; line-height: 1.5;"


# class DialogBackdrop(QWidget):
#     def __init__(self,  parent: Optional[QWidget] = None) -> None:
#         super().__init__(parent)
#
#         self.setAutoFillBackground(True)
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#         self.opacity: float = 0
#
#     def paintEvent(self, event: QPaintEvent):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#
#         # Creating the semi transparent backdrop
#         color = QColor(107, 114, 128, int(self.opacity * 190))  # gray-500 with opacity
#         painter.fillRect(self.rect(), color)


# Style everything
form_styles = """
            background-color: white;
           #contentPanel {
               background-color: white;
               border-radius: 8px;
               min-width: 320px;
               max-width: 380px;
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

           #dialogButton:hover {
               background-color: #4338CA;  /* indigo-700 */
           }

           #dialogButton:pressed {
               background-color: #3730A3;  /* indigo-800 */
           }
       """

class SingleIdDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.submit_button = None
        self.provider_id_input = None
        self.provider_name_input = None
        self.provider_name_label = None
        self.model_lob_dropdown = None
        self.model_lob_options = None
        self.model_lob_label = None

        self.content = QWidget(self)
        self.submit_button: Optional[QPushButton] = None
        self.backdrop_animation: QPropertyAnimation
        self.content_animation: QPropertyAnimation
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


        #  Model Line Of Business dropdown
        self.model_lob_options: list[str] = ["Commercial", "SHP", "Medicaid"]
        self.model_lob_dropdown = QComboBox(self)
        self.model_lob_dropdown.setStyleSheet(f"{input_styles} QLineEdit::placeholder {{color: #9CA3AF;}} QLineEdit::focus {{border: 2px solid #4F46E5;}}")
        self.model_lob_dropdown.setPlaceholderText("Line of business...")

        self.model_lob_label = QLabel("Model Line Of Business")
        self.model_lob_label.setStyleSheet(label_styles)
        self.model_lob_dropdown.addItems(self.model_lob_options)


        provider_id_label = QLabel(self)
        provider_id_label.setStyleSheet(label_styles)
        provider_id_label.setText("Model Provider's Id")

        self.provider_id_input = QLineEdit(self)
        self.provider_id_input.setStyleSheet(input_styles)
        # submit button
        # Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            "border-radius: 6px; background-color: #4f46e5; padding: 12px 8px; font-size: 14px; font-weight: 600; color: white; ")
        self.submit_button.setObjectName("dialogButton")
        self.submit_button.clicked.connect(self.on_form_submit)

        # add widgets to the form's layout
        form_layout.setSpacing(20)
        form_layout.addRow(self.provider_name_label, self.provider_name_input)
        form_layout.addRow(self.model_lob_label, self.model_lob_dropdown)
        form_layout.addRow(provider_id_label, self.provider_id_input)
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
        """ validate single id form"""
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
        # create a file from the form's data
        destination_path = os.path.join(f"{os.getcwd()}", "providers", "raw-ids", f"{self.provider_name_input.text()}")

        # make the path if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)

        df = pd.DataFrame()
        df.insert(0, 'Blue Shield ID', self.provider_name_input.text())
        df.insert(1, 'Model Name', self.model_lob_dropdown.currentText())
        df.insert(0, 'Model Line of Business', self.provider_id_input.text())

        output_file_path = os.path.join(destination_path, f"{self.provider_name_input.text().upper()}_{self.model_lob_dropdown.currentText().upper()}.csv")

        # save the file to the destination
        df.to_csv(output_file_path, index=False)

