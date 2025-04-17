from typing import Any, Tuple

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, Qt


class BlueShieldIdModel(QAbstractTableModel):
	def __init__(self, data_frame: pd.DataFrame):
		super().__init__()
		self._data_frame = data_frame

	def rowCount(self, parent=None) -> int:
		return len(self._data_frame)

	def columnCount(self, parent=None) -> int:
		return len(self._data_frame.columns)

	def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> Any:
		if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
			return None
		return str(self._data_frame.iat[index.row(), index.column()])

	def headerData(
		self,
		section: int,
		orientation: Qt.Orientation,
		role=Qt.ItemDataRole.DisplayRole,
	) -> Any:
		if role != Qt.ItemDataRole.DisplayRole:
			return None
		if orientation == Qt.Orientation.Horizontal:
			return str(self._data_frame.columns[section])
		return str(section + 1)

	def get_shape(self) -> Tuple[int, int]:
		"""Return the shape of the data as tuple in the form (row_count, column_count)"""
		return self._data_frame.shape
