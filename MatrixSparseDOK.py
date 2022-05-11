from __future__ import annotations

import sys

from MatrixSparse import *
from Position import *


spmatrix = dict[Position, float]


class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix

    def __init__(self, zero: float = 0.0):
        self._items = MatrixSparseDOK._items({})
        # invoking the __init__ of the parent class
        try:
            super(MatrixSparseDOK, self).__init__(zero)
        except ValueError:
            raise ValueError("__init__() invalid arguments")

    @MatrixSparse.zero.setter
    def zero(self, val: float):
        """ Overriding the zero.setter of parent class to delete the new zero valued items. """
        # Invoking parent's zero setter
        super(MatrixSparseDOK, self.__class__).zero.fset(self, val)
        # Deleting the redundant elements that equals new zero value
        self._items = {position:value for position, value in self._items.items() if value != self.zero}

    def __copy__(self):
        replica = MatrixSparseDOK(self.zero)
        for position, value in self._items.items():
            replica[position] = value
        return replica

    def __eq__(self, other: MatrixSparseDOK):
        if not isinstance(other, MatrixSparseDOK):
            return False
        return (self.zero == other.zero) and (self._items == other._items)

    def __iter__(self):
        self._index = -1
        self._items_sorted = sorted(self._items.keys(), key=lambda pos: (pos[0], pos[1]))
        return self

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
        """ Adds a number to sparse matrix."""
        if not isinstance(other, (int, float)):
            raise ValueError("_add_number() invalid arguments")
        number_added_matrix = self.__copy__()
        for pos in number_added_matrix:
            number_added_matrix[pos] += other

        return number_added_matrix

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        """ Adds two matrices."""
        if not isinstance(other, MatrixSparse):
            raise ValueError("_add_matrix() incompatible matrices")

        pos_min_self, pos_max_self = self.dim()
        pos_min_other, pos_max_other = other.dim()
        num_row_self = pos_max_self[0] - pos_min_self[0] + 1
        num_col_self = pos_max_self[1] - pos_min_self[1] + 1
        num_row_other = pos_max_other[0] - pos_min_other[0] + 1
        num_col_other = pos_max_other[1] - pos_min_other[1] + 1

        if self.zero != other.zero or num_row_self != num_row_other or num_col_self != num_col_other:
            raise ValueError("_add_matrix() incompatible matrices")

        matrix_added_matrix = self.__copy__()
        for pos in other:
            if matrix_added_matrix[pos] != matrix_added_matrix.zero:
                matrix_added_matrix[pos] += other[pos]
            else:
                matrix_added_matrix[pos] = other[pos]

        return matrix_added_matrix

    def _mul_number(self, other: [int, float]) -> Matrix:
        """ Multiplies a number and a sparse matrix."""
        if not isinstance(other, (int, float)):
            raise ValueError("_mul_number() invalid arguments")
        number_muled_matrix = self.__copy__()
        for pos in number_muled_matrix:
            number_muled_matrix[pos] *= other

        return number_muled_matrix

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        """ Multiplies two matrices."""
        if not isinstance(other, MatrixSparse):
            raise ValueError("_mul_matrix() incompatible matrices")

        pos_min_self, pos_max_self = self.dim()
        pos_min_other, pos_max_other = other.dim()
        num_col_self = pos_max_self[1] - pos_min_self[1] + 1
        num_row_other = pos_max_other[0] - pos_min_other[0] + 1
        num_col_other = pos_max_other[1] - pos_min_other[1] + 1

        if self.zero != other.zero or num_col_self != num_row_other:
            raise ValueError("_mul_matrix() incompatible matrices")

        matrix_muled_matrix = MatrixSparseDOK()
        for pos in self:
            col = pos[1]-pos_min_self[1]

            for i in range(num_col_other):
                if other[col + pos_min_other[0], i + pos_min_other[1]] != other.zero:
                    matrix_muled_matrix[pos[0], i + pos_min_other[1]] += self[pos]*other[col + pos_min_other[0], i + pos_min_other[1]]

        matrix_muled_matrix.zero = self.zero
        return matrix_muled_matrix

    def dim(self) -> tuple[Position, ...]:
        """ :return dim = Position(min_row, min_col), Position(max_row, max_col)"""
        if len(self) == 0:
            return ()
        min_row, min_col, max_row, max_col = sys.maxsize, sys.maxsize, -1, -1
        for position, value in self._items.items():
            min_row = position[0] if position[0] < min_row else min_row
            min_col = position[1] if position[1] < min_col else min_col
            max_row = position[0] if position[0] > max_row else max_row
            max_col = position[1] if position[1] > max_col else max_col

        return Position(min_row, min_col), Position(max_row, max_col)

    def row(self, row: int) -> Matrix:
        """ Creates a matrix with only given row """
        if not isinstance(row, int):
            raise ValueError("row() invalid arguments")
        rowMatrix = MatrixSparseDOK(self.zero)
        for position, value in self._items.items():
            if position[0] == row:
                rowMatrix[position] = value
        return rowMatrix

    def col(self, col: int) -> Matrix:
        """ Creates a matrix with only given column """
        if not isinstance(col, int):
            raise ValueError("col() invalid arguments")
        colMatrix = MatrixSparseDOK(self.zero)
        for position, value in self._items.items():
            if position[1] == col:
                colMatrix[position] = value
        return colMatrix

    def diagonal(self) -> Matrix:
        """ Returns the diagonal of the matrix. """
        if len(self) == 0:
            raise ValueError("diagonal() matrix not square")
        pos_min, pos_max = self.dim()

        if pos_max[0]-pos_min[0] != pos_max[1]-pos_min[1]:
            raise ValueError("diagonal() matrix not square")
        diagonal = MatrixSparseDOK()
        while pos_max != pos_min:
            diagonal[pos_min] = self[pos_min]
            pos_min = Position(pos_min[0]+1, pos_min[1]+1)

        diagonal[pos_min] = self[pos_min]
        return diagonal

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        if not isinstance(size, int):
            raise ValueError("eye() invalid parameters")
        elif size < 0:
            raise ValueError("eye() invalid parameters")

        if not (isinstance(unitary, (int, float)) and isinstance(zero, (int, float))):
            raise ValueError("eye() invalid parameters")

        eye_matrix = MatrixSparseDOK(zero)
        for i in range(size):
            eye_matrix[i, i] = unitary

        return eye_matrix

    def transpose(self) -> MatrixSparseDOK:
        transpose_matrix = self.__copy__()
        for pos in transpose_matrix:
            temp_value = self[pos]
            transpose_matrix[pos] = self[pos[1], pos[0]]
            transpose_matrix[pos[1], pos[0]] = temp_value

        return transpose_matrix

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
