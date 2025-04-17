import os
import platform
import shutil
import subprocess
from typing import Optional

import pandas as pd
from PyQt6.QtCore import QSize, pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
	QDialog,
	QHBoxLayout,
	QLabel,
	QMenu,
	QMessageBox,
	QPushButton,
	QSizePolicy,
	QSpacerItem,
	QTableView,
	QVBoxLayout,
	QWidget,
)

from ui.file_explorer import FileExplorer

from .blue_shield_id_model import BlueShieldIdModel
from .upload_form_dialog import UploadFormDialog

base_directory = os.getcwd()

dropdown_button_styles = """
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
        """

dropdown_menu_styles = """
            QMenu {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 4px 4px;
                margin-top: 4px;
                width: 107px;
            }
            QMenu::item {
                padding: 8px 32px 8px 8px;
                font-size: 14px;
                color: #374151;
                width: 100%;
            }
            QMenu::item:selected {
                background-color: #F3F4F6;
            }
        """


class SearchTab(QWidget):
	def __init__(self, parent: Optional[QWidget] = None):
		super().__init__(parent)

		self.form_dialog = UploadFormDialog(self)
		self.file_explorer = FileExplorer(directory=os.path.join(os.getcwd(), "providers", "raw-ids"))

		self.current_df: pd.DataFrame = pd.DataFrame()  # the current dataframe that is displayed in the tree view
		self.current_file_path: str = ""
		self._init_ui()

	def _init_ui(self):
		"""Initialize the user interface."""
		search_layout = QVBoxLayout()
		button_layout = QHBoxLayout()

		self.form_dialog.setStyleSheet("background-color: #f8fafc; padding: 20px 16px 16px; border-radius: 6px;")

		# styling the upload button
		raw_upload_button_icon = QIcon("./icons/use-single-id-icon.svg")

		#  CREATING THE UPLOAD DROPDOWN.
		# trigger
		self.single_id_button = QPushButton(text="Upload Single ID")
		self.single_id_button.setStyleSheet(dropdown_button_styles)
		self.single_id_button.setIcon(raw_upload_button_icon)
		self.single_id_button.setIconSize(QSize(20, 20))
		self.single_id_button.clicked.connect(self.on_single_id_trigger)

		# # menu
		# self.upload_dropdown_menu = QMenu(self)
		# self.upload_dropdown_menu.setStyleSheet(dropdown_menu_styles)

		# #  template menu action
		# self.useTemplateMenu = self.upload_dropdown_menu.addAction("Use Template")
		# self.useTemplateMenuIcon = QIcon("./icons/use-template-icon.svg")
		# self.useTemplateMenu.setIcon(self.useTemplateMenuIcon)
		# self.useTemplateMenu.triggered.connect(self.upload_ids_file_slot)

		# # single id menu action
		# self.single_id_menu = self.upload_dropdown_menu.addAction("Single ID")
		# self.single_id_menu_icon = QIcon("./icons/use-single-id-icon.svg")
		# self.single_id_menu.setIcon(self.single_id_menu_icon)
		# self.single_id_menu.triggered.connect(self.on_single_id_trigger)

		# upload_button = QPushButton(icon=raw_upload_button_icon, text="Upload Ids")
		# upload_button.setMinimumHeight(40)
		# upload_button.setMaximumWidth(200)
		# upload_button.setIconSize(QSize(20, 20))
		# upload_button.setStyleSheet("background-color: #3b82f6; padding: 8px 12px; color: white; font-weight: 600; border-radius: 6px; font-size: 14px; line-height: 20px; font-weight: 600;")
		#
		# # Keyboard shortcut for the upload button.
		# upload_button_shortcut = QKeySequence("CTRL+U")
		# upload_button.setShortcut(upload_button_shortcut)

		# Slot for the upload button
		# upload_button.clicked.connect(self.upload_ids_file_slot)

		# Run Query button
		run_query_icon = QIcon("./icons/run_query_icon.svg")
		run_query_button = QPushButton(icon=run_query_icon, text="Run Query")
		run_query_button.setMinimumWidth(20)
		run_query_button.setMaximumWidth(200)
		run_query_button.setIconSize(QSize(20, 20))
		run_query_button.setStyleSheet(
			"border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;"
		)

		# run query button slot
		run_query_button.clicked.connect(
			self.run_query_slot
		)  # TODO: This button will instead connect to the slot that does the main query

		# # EDIT BUTTON
		# edit_icon = QIcon("./icons/edit_file_icon.svg")
		# edit_button = QPushButton(icon=edit_icon, text="Edit")
		# edit_button.setMinimumWidth(20)
		# edit_button.setMaximumWidth(200)
		# edit_button.setIconSize(QSize(20, 20))
		# edit_button.setStyleSheet("border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;")

		# edit_button.clicked.connect(self.on_edit_click)

		# REFRESH BUTTON
		refresh_icon = QIcon("./icons/refresh_file_icon.svg")
		refresh_button = QPushButton(icon=refresh_icon, text="Refresh")
		refresh_button.setMinimumWidth(20)
		refresh_button.setMaximumWidth(200)
		refresh_button.setIconSize(QSize(20, 20))
		refresh_button.setStyleSheet(
			"border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;"
		)

		refresh_button.clicked.connect(self.on_refresh_click)

		# Creating the actions dropdown menu
		# trigger
		self.actions_button = QPushButton(self)
		self.actions_button.setText("Actions")
		self.actions_button.setToolTip("Click here to find more actions")
		self.actions_button.setShortcut("Ctrl+A")
		self.actions_button.setMinimumWidth(20)
		self.actions_button.setMaximumWidth(200)
		self.actions_button.setIcon(QIcon("./icons/more_icon.svg"))
		self.actions_button.setIconSize(QSize(20, 20))
		self.actions_button.setStyleSheet(
			"border-radius: 6px; padding: 8px 12px; color: #111827; border: 0.725 solid #d1d5db; background-color: white; font-size: 14px; line-height: 20px; font-weight: 600;"
		)

		# dropdown
		self.actions_dropdown_menu = QMenu(self)
		self.actions_dropdown_menu.setMinimumWidth(self.actions_button.width())
		self.actions_dropdown_menu.setStyleSheet(dropdown_menu_styles)

		# dropdown actions
		self.edit_button = QAction("Edit", self)
		self.actions_dropdown_menu.addAction(self.edit_button)
		self.edit_button.setIcon(QIcon("./icons/edit_file_icon.svg"))
		self.edit_button.triggered.connect(self.on_save_query)
		self.edit_button.triggered.connect(self.on_edit_click)

		self.save_button = QAction("Save", self)
		self.actions_dropdown_menu.addAction(self.save_button)
		self.save_button.setIcon(QIcon("./icons/save_icon.svg"))
		self.save_button.triggered.connect(self.on_save_query)

		self.delete_button = QAction("Delete", self)
		self.actions_dropdown_menu.addAction(self.delete_button)
		self.delete_button.setIcon(QIcon("./icons/trash_icon.svg"))
		self.delete_button.triggered.connect(self.on_delete_file)

		# connecting the dropdown to the trigger
		self.actions_button.setMenu(self.actions_dropdown_menu)

		# self.upload_dropdown_button.setMenu(self.upload_dropdown_menu)
		button_layout.addWidget(self.single_id_button)

		# button_layout.addWidget(upload_button)
		button_layout.addWidget(run_query_button)
		# button_layout.addWidget(edit_button)
		button_layout.addWidget(refresh_button)
		button_layout.addWidget(self.actions_button)

		heading_text = QLabel("WELCOME...")
		heading_text.setStyleSheet(
			"font-size: 30px; margin: 10px 0px; line-height: 28px; font-weight: bold; color: #0f172a; "
		)

		header_layout = QHBoxLayout()
		header_layout.addWidget(heading_text)
		header_layout.addLayout(button_layout)
		header_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored))

		search_layout.addLayout(header_layout)

		self.table_view = QTableView()
		search_layout.addWidget(self.table_view)

		self.setLayout(search_layout)

		self.load_template_data()

	def load_template_data(self) -> None:
		"""Load the template data into the table view."""
		try:
			template_file = os.path.join(base_directory, "resources", "template_ids.csv")
			dataframe = pd.read_csv(template_file)
			self.update_table_model(dataframe)
		except Exception as e:
			QMessageBox.critical(self, "Error", f"Failed to load template file: {str(e)}")

	def update_table_model(self, dataframe: pd.DataFrame) -> None:
		"""Update the table view with new data."""
		# self.current_df = dataframe
		# model = BlueShieldIdModel(dataframe)
		# self.table_view.setModel(model)

		self.current_df = dataframe  # Store the new dataframe

		try:
			# Check if the model is correctly initialized with the dataframe
			model = BlueShieldIdModel(dataframe)
			self.table_view.setModel(model)

		except Exception as e:
			print(f"Error in updating table model: {e}")

	@pyqtSlot()
	def on_save_query(self) -> None:
		"""Save the results of the query to the file system"""
		# folder = os.path.dirname(self.current_file_path)
		# filename = os.path.basename(self.current_file_path)

		profile_file_name = self.current_file_path.replace("RAW_ID", "PROFILE")
		self.current_df.to_csv(f"{profile_file_name}", index=False)

		QMessageBox.information(self, "Save Successful", f"File saved successfully as {profile_file_name}")

		print(f"File to saved to the file system under the following name {self.current_file_path}")

	@pyqtSlot()
	def download_template_slot(self) -> None:
		"""Download the template file to the user's Downloads folder."""
		template_file = os.path.join(base_directory, "resources", "template_ids.csv")

		if os.path.isfile(template_file):
			destination = os.path.join(os.path.expanduser("~"), "Downloads", "template_ids.csv")
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

	@pyqtSlot()
	def on_single_id_trigger(self) -> None:
		"""open the single id form dialog"""
		from .single_id_upload import SingleIdDialog

		form_dialog = SingleIdDialog(file_explorer=self.file_explorer, parent=self)
		if form_dialog.exec() == QDialog.DialogCode.Accepted:
			pass

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
				QMessageBox.critical(self, "Error", "'data store.csv' must contain 'BS_ID' column.")
				return

			self.process_csv_file(data_store_df)

		except Exception as e:
			QMessageBox.critical(self, "Error", f"Failed to load data store file: {str(e)}")

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
			os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

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
			QMessageBox.critical(self, "Error", f"Failed to process the query, {str(e)}")

	@pyqtSlot()
	def on_delete_file(self) -> None:
		"""delete the file from the file system"""
		file_to_delete = self.current_file_path.replace("RAW_ID", "PROFILE")
		if not os.path.exists(file_to_delete):
			QMessageBox.critical(self, "Error", "Failed to a non profile file")
		else:
			os.remove(file_to_delete)

	def on_edit_click(self) -> None:
		file_to_open = self.form_dialog.saved_file_path

		if not file_to_open:
			QMessageBox.critical(self, "File Not Found Error", "No file to edit...")
			return
		try:
			if platform.system() == "Darwin":
				subprocess.run(["open", file_to_open], check=True)
			elif platform.system() == "Windows":
				os.startfile(file_to_open)  # type: ignore
			else:
				subprocess.run(["xdg-open", file_to_open])

		except Exception as e:
			print("Error", f"Failed to open file: {e}")
			QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

	@pyqtSlot()
	def on_refresh_click(self) -> None:
		"""Slot to update the table when the refresh button is clicked"""

		# Determine which file path to use
		active_file_path = None

		if self.current_file_path:
			active_file_path = self.current_file_path  # Use sidebar file if available
			print(f"Refreshing sidebar file: {active_file_path}")
		elif self.form_dialog.saved_file_path:
			active_file_path = self.form_dialog.saved_file_path  # Use uploaded file if no sidebar file
			print(f"Refreshing uploaded file: {active_file_path}")

		if not active_file_path:
			QMessageBox.critical(self, "Error", "No file available to refresh")
			return

		if not os.path.exists(active_file_path):
			QMessageBox.critical(self, "Error", f"File not found: {active_file_path}")
			return

		# file_path = self.current_file_path or self.form_dialog.saved_file_path
		# if not active_file_path:
		#     QMessageBox.critical(self, "Error", "No updated file to refresh || file's destination may have changed")
		#     return

		try:
			print(f"file from sidebar: {active_file_path}")
			updated_df = pd.read_csv(active_file_path)
			self.form_dialog.data_loaded.emit(updated_df)
			self.update_table_model(updated_df)
			# TODO: toast notification for a successful refresh
		except Exception as e:
			QMessageBox.critical(self, "Error", f"Failed to read file: {e}")

	@pyqtSlot(str)
	def on_load_sidebar_file_to_table(self, file_path: str) -> None:
		"""Load the selected file from FileExplorer sidebar into the table view."""

		try:
			self.current_file_path = file_path
			self.form_dialog.saved_file_path = file_path
			dataframe = pd.read_csv(file_path)

			self.update_table_model(dataframe)
			# QMessageBox.information(self, "File Loaded", f"Loaded data from {file_path}")
		except Exception as e:
			QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
