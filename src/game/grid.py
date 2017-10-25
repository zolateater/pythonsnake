from typing import List
from .enums import CellType

class Grid():
    def __init__(self, cells: List[List[str]]):
        self._failIfSizeInvalid(cells)
        self._failIfContainsInvalidCells(cells)
        self.cells = cells

    @property
    def width(self) -> int:
        return len(self.cells[0])

    @property
    def height(self) -> int:
        return len(self.cells)

    def _failIfSizeInvalid(self, cells: List[List[str]]) -> None:
        """
        Checks if all rows have the same length and row count is more than 0.
        Raises ValueError otherwise.
        :raises ValueError
        :param cells: 2D list of strings
        :return:
        """
        if len(cells) == 0:
            raise ValueError('Count of cells must be greater than 0')

        cellsInRowCount = len(cells[0])

        for i, row in enumerate(cells):
            if len(row) != cellsInRowCount:
                raise ValueError('Cells count in row #{} does not match cell count in first row'.format(cellsInRowCount))

    def _failIfContainsInvalidCells(self, cells: List[List[str]]) -> None:
        """
        :raises ValueError
        :param cells: 2D list of strings
        :return:
        """
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                print(ord(cell))

                if not CellType.cellTypeExists(cell):
                    print(list(CellType.__members__))
                    raise ValueError('Cell({i}, {j}) has wrong value: "{cell}"'.format(i=i, j=j, cell=cell))