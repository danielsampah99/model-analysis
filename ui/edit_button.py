from PyQt6.QtCore import QFileSystemWatcher, pyqtSignal, QObject
import os
import subprocess
import platform
import time


class FileWatchHandler(QObject):
	"""Handles external file editing and monitoring."""

	file_changed = pyqtSignal(str)  # Signal emitted when file is modified

	def __init__(self):
		super().__init__()
		self.watcher = QFileSystemWatcher()
		self.watcher.fileChanged.connect(self._handle_file_change)
		self.current_file = None
		self.last_modified = 0

	def open_file_externally(self, file_path):
		"""Opens file with system default application."""
		if self.current_file:
			self.watcher.removePath(self.current_file)

		self.current_file = file_path
		self.last_modified = os.path.getmtime(file_path)
		self.watcher.addPath(file_path)

		# Open with default application based on OS
		if platform.system() == "Darwin":  # macOS
			subprocess.run(["open", file_path])
		elif platform.system() == "Windows":  # Windows
			os.startfile(file_path)
		else:  # Linux
			subprocess.run(["xdg-open", file_path])

	def _handle_file_change(self, file_path):
		"""Handles file modification events."""
		# Some editors may trigger multiple events
		# Wait brief moment and check if truly modified
		time.sleep(0.1)

		try:
			current_mtime = os.path.getmtime(file_path)
			if current_mtime > self.last_modified:
				self.last_modified = current_mtime
				self.file_changed.emit(file_path)

			# Re-add the file to the watcher as some systems remove it
			if not self.watcher.files():
				self.watcher.addPath(file_path)

		except FileNotFoundError:
			# File might be temporarily unavailable during save
			# Wait then try to re-add to watcher
			time.sleep(0.2)
			if os.path.exists(file_path):
				self.watcher.addPath(file_path)
