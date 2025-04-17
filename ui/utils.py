import datetime
import os
from typing import List


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

	def get_decade_span(self, current_year: int) -> List[int]:
		"""
		Get a list of years from the current year. Five years before and five years after.
		Say the current year is 2025, we get a list of years starting from 2020 spanning through 2030
		"""

		return list(range(current_year - 5, current_year + 6))

	def format_model_type_name(self, model_type: str) -> str:
		"""Format the value of the model type by capitalizing it and replacing the spaces with underscores"""
		if model_type is None:
			return ""
		return model_type.upper().replace(" ", "_")
