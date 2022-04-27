from __future__ import annotations
from MatrixSparse import *
from Position import *


spmatrix = dict[Position, float]


class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix

    def __init__(self, zero: float = 0.0):
        # invoking the __init__ of the parent class
        super(MatrixSparseDOK, self).__init__(zero)

        self._items = MatrixSparseDOK._items({})

    def __copy__(self):
        """ """
        return {position: value for position, value in self}

    def __eq__(self, other: MatrixSparseDOK):
        return (self.zero == other.zero) and (self._items == other._items)

    def __iter__(self):
        self._index = -1
        self._items_sorted = sorted(self._items.keys(), key=lambda pos: (pos[0], pos[1]))

    def __next__(self):
        self._index += 1
        if self._index == len(self):
            raise StopIteration
        return self._items_sorted[self._index]

    def __getitem__(self, pos: [Position, position]) -> float:
        try:
            pos = self._check_pos(pos)
        except ValueError:
            raise ValueError("__getitem__() invalid arguments")

        if pos in self._items.keys():
            return self._items[pos]
        else:
            return self.zero

    def __setitem__(self, pos: [Position, position], val: [int, float]):
        try:
            pos = self._check_pos(pos)
        except ValueError:
            raise ValueError("__setitem__() invalid arguments")

        if not isinstance(val, (int, float)):
            raise ValueError("__setitem__() invalid arguments")

        if val == self.zero:
            if pos in self._items.keys():
                del self._items[pos]
        else:
            self._items[pos] = val

    def __len__(self) -> int:
        """ :return the number of the non-zero elements. """
        return len(self._items)

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
        # Implement For
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

    def _check_pos(self, pos):
        """
        Checks whether the position entered by user is valid or not.
        :param pos: Position object or tuple
        :return: Position object if pos is valid, raise exception if not
        """
        if not isinstance(pos, (Position, tuple)):
            raise ValueError("invalid position arguments")
        # now we have either a Position or a position tuple
        if isinstance(pos, tuple):
            if len(pos) == 2:
                pos = Position(pos[0], pos[1])
            else:
                raise ValueError("invalid position arguments")

        return pos
