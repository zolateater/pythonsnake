from typing import List
from .enums import CellType
from .position import Position

class Grid():
    def __init__(self, cells: List[List[str]]):
        self._fail_if_size_invalid(cells)
        self._fail_if_contains_invalid_cells(cells)
        self.cells = cells

    @property
    def width(self) -> int:
        return len(self.cells[0])

    @property
    def height(self) -> int:
        return len(self.cells)

    def get_cell_at(self, pos: Position) -> str:
        return self.cells[pos.y][pos.x]

    def _fail_if_size_invalid(self, cells: List[List[str]]) -> None:
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

    def _fail_if_contains_invalid_cells(self, cells: List[List[str]]) -> None:
        """
        :raises ValueError
        :param cells: 2D list of strings
        :return:
        """
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                if not CellType.exists(cell):
                    raise ValueError('Cell({i}, {j}) has wrong value: "{cell}"'.format(i=i, j=j, cell=cell))
