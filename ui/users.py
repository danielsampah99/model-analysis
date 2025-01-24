# the financial analysts tab.
from typing import List, Optional

from PyQt6.QtCore import QAbstractTableModel, QSize, Qt, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from database import Database, DatabaseUser

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
validation_error_input_style = "border: 2px solid red; background-color: #FFEEEE;"
validation_error_label_style = "color:red;"


class Users(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.database = Database()
        self.heading = Heading(self.database)

        self.model = AllUsersTable(self.fetch_all_users())
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.heading, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def fetch_all_users(self):
        data = self.database.get_all_users()
        print(data)
        return data


class Heading(QWidget):
    # the heading for the financial anaylst page.
    def __init__(
        self,
        db: Database,
        parent: Optional["QWidget"] = None,
    ) -> None:
        super().__init__(parent)

        self.database = db

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
        self.database = Database()
        self.init_ui()

    def init_ui(self):
        dialog_window_icon = QIcon("./icons/new_user_icon.svg")

        form_layout = QFormLayout()

        self.setWindowTitle("Add a new user")
        self.setWindowIcon(dialog_window_icon)
        self.setMinimumSize(500, 200)
        self.setStyleSheet(new_user_dialog_styles)

        # first name
        self.first_name_label = QLabel("First Name")
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("John")

        # last name
        self.last_name_label = QLabel("Last Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Doe")

        # email
        self.email_label = QLabel("Email Address")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("johndoe@gmail.com")

        # user group
        group_label = QLabel("Role", self)
        self.group_combo = QComboBox(self)
        self.group_combo.setStyleSheet("border: 1px solid #D1D5DB; border-radius: 6px; background: white; font-size: 14px;")
        group_options = ["Financial Analyst", "Provider Partner"]
        self.group_combo.addItems(group_options)
        self.group_combo.setCurrentIndex(0)

        create_user_button = QPushButton("Create user")
        create_user_button.setStyleSheet(submit_button_styles)
        create_user_button.clicked.connect(self.on_form_submit)

        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setVerticalSpacing(25)
        form_layout.setHorizontalSpacing(15)
        form_layout.addRow(self.first_name_label, self.first_name_input)
        form_layout.addRow(self.last_name_label, self.last_name_input)
        form_layout.addRow(self.email_label, self.email_input)
        form_layout.addRow(group_label, self.group_combo)
        form_layout.addRow(create_user_button)

        self.setLayout(form_layout)

    def validate_create_user(self) -> bool:
        """Validate creating a new user"""
        errors: list[str] = []
        email = self.email_input.text()

        if self.first_name_input.text() == "":
            message = "First name is required"
            errors.append(message)
            self.first_name_input.setStyleSheet(validation_error_input_style)
            self.first_name_label.setStyleSheet(validation_error_label_style)
            self.first_name_label.setToolTip(message)
            return False
        else:
            self.first_name_input.setStyleSheet("")
            self.first_name_label.setStyleSheet("")

        if self.last_name_input.text() == "":
            message = "Last name is required"
            errors.append(message)
            self.last_name_input.setStyleSheet(validation_error_input_style)
            self.last_name_label.setStyleSheet(validation_error_label_style)
            self.last_name_label.setToolTip(message)
            return False
        else:
            self.last_name_input.setStyleSheet("")
            self.last_name_label.setStyleSheet("")

        if email == "" or "@" not in email or "." not in email:
            message = "Invalid email address"
            errors.append(message)
            self.email_input.setStyleSheet(validation_error_input_style)
            self.email_label.setStyleSheet(validation_error_label_style)
            self.email_label.setToolTip(message)
            return False
        else:
            self.email_input.setStyleSheet("")
            self.email_label.setStyleSheet("")

        return True

    @pyqtSlot()
    def on_form_submit(self):
        """Slot for creating a new user"""
        if self.validate_create_user():
            # TODO: Add the user to the database and close the dialog
            saved_data = {
                "first_name": self.first_name_input.text().lower(),
                "last_name": self.last_name_input.text().lower(),
                "email": self.email_input.text().lower(),
                "role": self.group_combo.currentText().lower(),
            }
            self.database.create_new_user(
                email=saved_data["email"], first_name=saved_data["first_name"], last_name=saved_data["last_name"], role=saved_data["role"]
            )
            print(f"data going into the database: {saved_data}")
            self.accept()


class AllUsersTable(QAbstractTableModel):
    """show all the users in the database regardless of the role."""

    def __init__(self, users: List[DatabaseUser]) -> None:
        super().__init__()
        self.users = users or []

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            user = self.users[index.row()]

            if index.column() == 0:
                return user.first_name.title()
            elif index.column() == 1:
                return user.last_name.title()
            elif index.column() == 2:
                return user.email
            elif index.column() == 3:
                return user.role.upper()
            elif index.column() == 4:
                return user.created_at

        return None

    def rowCount(self, parent=None) -> int:
        """return the total number of rows in the data"""
        return len(self.users)

    def columnCount(self, parent=None) -> int:
        """return the total number of columns the data could have"""
        return len(self.users[0]) if self.users else 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            headers = ["First Name", "Last Name", "Email Address", "Role", "Created At"]
            return headers[section]

        return super().headerData(section, orientation, role)
