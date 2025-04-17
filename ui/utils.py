import datetime
import os


class Utils:
	"""utility functions/methods to be used in the application"""

	def __init__(self) -> None:
		self.parent_directory = os.path.join(os.getcwd(), "providers", "raw-ids")

	def get_parent_directory(self) -> str:
		"""return the parent directory up to the raw_ids folder"""
		return self.parent_directory

	def get_current_year_directory(self) -> str | os.PathLike:
		"return the directory with the year: .../raw ids/2025"

		return os.path.join(self.get_parent_directory(), str(self.get_current_year()))

	def get_current_year(self) -> int:
		"""return the current year.
		Eg. 2024
		"""

		return datetime.datetime.now().year

	def format_model_type_name(self, model_type: str) -> str:
		"""Format the value of the model type by capitalizing it and replacing the spaces with underscores"""
		if model_type is None:
			return ""
		return model_type.upper().replace(" ", "_")
