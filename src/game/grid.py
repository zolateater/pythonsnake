from typing import List
from .enums import CellType
from .position import Position

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

    def getCell(self, pos: Position) -> str:
        return self.cells[pos.y][pos.x]

    def setCell(self, pos: Position, value: str) -> None:
        # TODO: add value check if member of cell type
        self.cells[pos.y][pos.x] = value

    def swap(self, pos1: Position, pos2: Position) -> None:
        tmp = self.getCell(pos1)
        self.setCell(pos1, self.getCell(pos2))
        self.setCell(pos2, tmp)

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
                if not CellType.cellTypeExists(cell):
                    raise ValueError('Cell({i}, {j}) has wrong value: "{cell}"'.format(i=i, j=j, cell=cell))
