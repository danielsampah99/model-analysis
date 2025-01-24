# the financial analysts tab.
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

main_button_style = """
            QPushButton {
                background-color: #1f2937;
                border: 1px solid #111827;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 600;
                line-height: 20px;
                color: #f9fafb;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #374151
            }
            QIcon {
                color: white;
            }
        """

new_user_dialog_styles = """
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
            background-color: #f0f0f0;
            color: #333;
            border: 1px solid #888;
            border-radius: 5px;
            padding: 5px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;  /* Background color of the dropdown */
            color: #000000;             /* Text color of the dropdown */
            selection-background-color: #0078d7; /* Selected item background */
            selection-color: #ffffff;   /* Selected item text color */
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

submit_button_styles = "border-radius: 6px; background-color: #4f46e5; padding: 12px 8px; font-size: 14px; font-weight: 600; color: white; "


class Users(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)

        self.heading = Heading()

        layout = QVBoxLayout()
        layout.addWidget(self.heading, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)


class Heading(QWidget):
    # the heading for the financial anaylst page.
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)

        self.init_ui()

    def init_ui(self) -> None:
        # initialize the header.
        layout = QHBoxLayout()

        heading_text = QLabel(text="USERS")
        heading_text.setStyleSheet("font-size: 30px; margin: 10px 0px; line-height: 28px; font-weight: bold; color: #0f172a;")

        # new analyst button
        new_user_icon = QIcon("./icons/new_user_icon.svg")

        new_user_button = QPushButton(text="New User")
        new_user_button.setStyleSheet(main_button_style)
        new_user_button.setIcon(new_user_icon)
        new_user_button.setIconSize(QSize(20, 20))
        new_user_button.setToolTip("Add a new user")
        new_user_button.setMaximumWidth(120)
        new_user_button.clicked.connect(self.on_click)

        layout.addWidget(heading_text)
        layout.addWidget(new_user_button)

        self.setLayout(layout)

    def on_click(self) -> None:
        print("open the form dialog")

        # instantiate a new user form dialog
        self.new_user_dialog = NewUserForm()

        # peform the ff action if the ok button of the dialog was clicked.
        if self.new_user_dialog.exec() == QDialog.DialogCode.Accepted:
            print("New user added successfully")


class NewUserForm(QDialog):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        dialog_window_icon = QIcon("./icons/new_user_icon.svg")

        form_layout = QFormLayout()

        self.setWindowTitle("Add a new user")
        self.setWindowIcon(dialog_window_icon)
        self.setMinimumSize(500, 200)
        self.setStyleSheet(new_user_dialog_styles)

        # first name
        first_name_label = QLabel("First Name")
        first_name_input = QLineEdit()
        first_name_input.setPlaceholderText("John")

        # last name
        last_name_label = QLabel("Last Name")
        last_name_input = QLineEdit()
        last_name_input.setPlaceholderText("Doe")

        # email
        email_label = QLabel("Email Address")
        email_input = QLineEdit()
        email_input.setPlaceholderText("johndoe@gmail.com")

        # user group
        group_label = QLabel("Role", self)
        group_combo = QComboBox(self)
        group_combo.setStyleSheet("border: 1px solid #D1D5DB; border-radius: 6px; background: white; font-size: 14px;")
        group_options = ["Financial Analyst", "Provider Partner"]
        group_combo.addItems(group_options)
        group_combo.setCurrentIndex(0)

        create_user_button = QPushButton("Create user")
        create_user_button.setStyleSheet(submit_button_styles)

        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setVerticalSpacing(25)
        form_layout.setHorizontalSpacing(15)
        form_layout.addRow(first_name_label, first_name_input)
        form_layout.addRow(last_name_label, last_name_input)
        form_layout.addRow(email_label, email_input)
        form_layout.addRow(group_label, group_combo)
        form_layout.addRow(create_user_button)

        self.setLayout(form_layout)
