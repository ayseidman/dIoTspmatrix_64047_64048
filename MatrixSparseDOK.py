from __future__ import annotations
from MatrixSparse import *
from Position import *


spmatrix = dict[Position, float]


class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix

    def __init__(self, zero: float = 0.0):
        # invoking the __init__ of the parent class
        super(MatrixSparseDOK,self).__init__(zero)

        self._min_row, self._min_col = -1, -1
        self._max_row, self._max_col = -1, -1

        self._items = MatrixSparseDOK._items({})


    def __copy__(self):
        """ """
        return {position: value for position, value in self}

    def __eq__(self, other: MatrixSparseDOK):
        return (self.zero == other.zero) and (self._items == other._items)

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __getitem__(self, pos: [Position, position]) -> float:
        if not isinstance(pos, (Position, tuple)):
            raise ValueError("__getitem__() invalid arguments")
        #now we have either a Position or a position tuple
        if isinstance(pos, tuple):
            if len(pos) == 2:
                pos = Position(pos[0], pos[1])
            else:
                raise ValueError("__getitem__() invalid arguments")

        if pos in self._items.keys():
            return self._items[pos]
        else:
            return self.zero

    def __setitem__(self, pos: [Position, position], val: [int, float]):
        pass

    def __len__(self) -> int:
        pass

    def _add_number(self, other: [int, float]) -> Matrix:
        pass

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

    def _mul_number(self, other: [int, float]) -> Matrix:
        pass

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

    def dim(self) -> tuple[Position, ...]:
        """ :return dim = Position(min_row, min_col), Position(max_row, max_col)"""
        pass

    def row(self, row: int) -> Matrix:
        pass

    def col(self, col: int) -> Matrix:
        pass

    def diagonal(self) -> Matrix:
        pass

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        pass

    def transpose(self) -> MatrixSparseDOK:
        pass

    def compress(self) -> compressed:
        pass

    @staticmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        pass

    @staticmethod
    def decompress(compressed_vector: compressed) -> MatrixSparse:
        pass
